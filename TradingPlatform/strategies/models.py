# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from random import randint
from django.db import models


class Strategy(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "{}".format(
            self.name
        )


class Exchange(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __unicode__(self):
        return "{}".format(
            self.name
        )


class Security(models.Model):
    name = models.CharField(max_length=100)  # remove
    symbol = models.CharField(max_length=10)

    def __unicode__(self):
        return "{}".format(
            self.code
        )


class ParentOrder(models.Model):
    ACTION_TYPES = (
        ('Buy', u'Buy'),
        ('Sell', u'Sell'),
        ('Short', u'Short'),
    )

    BIAS_TYPES = (
        ('Long', u'Long'),  # 0 < price < bias_net
        ('Short', u'Short'), # bias_net < price < 0
        ('Neutral', u'Neutral'), # -bias_net < price < +bias_net
    )

    strategy = models.ForeignKey(Strategy, related_name='parent_orders')
    exchange = models.ForeignKey(Exchange, related_name='parent_orders')
    symbol = models.CharField(max_length=50)
    action = models.CharField(choices=ACTION_TYPES, max_length=10)
    bias = models.CharField(choices=BIAS_TYPES, max_length=10)
    bias_net = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maximum Bias Net Position")
    # positions manager volume cannot exceed BuyVol or SellVol
    volume = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Parent Volume")
    limit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Parent Limit Price")
    num_slices = models.IntegerField(verbose_name="Number of Unique Slices")
    pl = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __unicode__(self):
        return "{} - {} - {}".format(
            self.strategy.name, self.exchange.code, self.security
        )


class SlicePrice(models.Model):
    REFERENCE_TYPES = (
        ('BEST BID', 'BEST BID'),
        ('BEST OFFER', 'BEST OFFER'),
        ('LAST', 'LAST'),
        ('OPEN', 'OPEN'),
        ('DAILY HIGH', 'DAILY HIGH'),
        ('DAILY LOW', 'DAILY LOW'),
        ('DAILY NET PRICE', 'DAILY NET PRICE'),
        ('MTD NET PRICE', 'MTD NET PRICE'),
        ('NUMBER', 'NUMBER')
    )

    OFFSET_TYPES = (
        ('P', '%'),
        ('C', 'cents')
    )

    reference_data_point = models.CharField(choices=REFERENCE_TYPES, max_length=20)
    offset_type = models.CharField(choices=OFFSET_TYPES, max_length=10)
    offset_num = models.DecimalField(max_digits=12, decimal_places=4)

    @property
    def price(self, market_data=None):
        pass

    def __unicode__(self):
        return "{} {} {}".format(
            self.reference_data_point, self.offset_type, self.offset_num
        )


class SliceDelay(models.Model):
    unfilled_lower = models.DecimalField(max_digits=10, decimal_places=2)
    unfilled_upper = models.DecimalField(max_digits=10, decimal_places=2)
    filled_lower = models.DecimalField(max_digits=10, decimal_places=2)
    filled_upper = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return "Delay {} {}".format(
            self.id, self.unfilled if self.unfilled else self.filled
        )

    @property
    def delay_filled(self):
        return randint(self.filled_lower, self.filled_upper)

    @property
    def delay_unfilled(self):
        return randint(self.unfilled_lower, self.unfilled_upper)


class SliceLiftHit(models.Model):
    activate = models.BooleanField(default=False)
    lh_price = models.ForeignKey(SlicePrice, related_name='lift_hits')
    delay = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return "{} - {}".format(
            self.lh_price, self.activate
        )


class Slice(models.Model):
    REFERENCE_TYPES = (
        ('BEST BID', 'BEST BID'),
        ('BEST OFFER', 'BEST OFFER'),
        ('LAST', 'LAST'),
        ('OPEN', 'OPEN'),
        ('DAILY HIGH', 'DAILY HIGH'),
        ('DAILY LOW', 'DAILY LOW'),
        ('DAILY NET PRICE', 'DAILY NET PRICE'),
        ('MTD NET PRICE', 'MTD NET PRICE'),
        ('NUMBER', 'NUMBER')
    )

    OFFSET_TYPES = (
        ('P', '%'),
        ('C', 'cents')
    )

    parent_order = models.ForeignKey(ParentOrder, related_name='slices')
    sequence = models.IntegerField(default=0)
    reference_data_point = models.CharField(choices=REFERENCE_TYPES, max_length=20)
    offset_type = models.CharField(choices=OFFSET_TYPES, max_length=10)
    offset_num = models.DecimalField(max_digits=12, decimal_places=4, verbose_name="Offset from Data point")
    delay = models.ForeignKey(SliceDelay, related_name='+', verbose_name="Slice Order Delay (Filled/Unfilled)")
    volume = models.IntegerField(verbose_name="Slice Order Volume")
    lift_hit_active = models.BooleanField(default=False)
    lift_hit_reference_data_point = models.CharField(choices=REFERENCE_TYPES, max_length=20)
    lift_hit_offset_type = models.CharField(choices=OFFSET_TYPES, max_length=10)
    lift_hit_offset_num = models.DecimalField(max_digits=12, decimal_places=4, verbose_name="Lift Hit Offset from Data point")
    lift_hit_delay = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return "{} - {}".format(
            self.parent_order, self.sequence
        )

    # def save(self, **kwargs):
        # if not self.pk:
        #     self.save()
        # Order.objects.create(status='Active', slice=self)
        # return super(Slice, self).save(**kwargs)


class Order(models.Model):
    STATUS = (
        ('Active', 'Active'),
        ('Stopped', 'Stopped')
    )

    status = models.CharField(choices=STATUS, max_length=20)
    slice = models.ForeignKey(Slice)
    outstanding = models.BooleanField(default=False)

    def __init__(self, momentum, *args, **kwargs):
        self.position = 0
        self.delay = self.slice.delay
        self.volume = self.slice.volume
        self.price = self.slice.price
        self.momentum = momentum  # 31
        self.units = 100000  # 32

    def create_order(self, side, units):
        # TODO MAKE CONNECTION TO ITS
        # order =
        # .create_order(config['oanda']['account_id'],
        #                            instrument='EUR_USD', units=units, side=side,
        #                            type='market')
        # print('\n', order)
        pass
