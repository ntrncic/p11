# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from strategies.models import ParentOrder, SliceLiftHit, SlicePrice, Slice, SliceDelay, Strategy, Exchange, Security


class SliceAdmin(admin.TabularInline):
    model = Slice
    # list_display = (
    #     'intervention',
    #     'types',
    #     'signed_date'
    # )
    # search_fields = ('intervention', )
    # list_filter = (
    #     'intervention',
    #     'types'
    # )
    fields = (
        "parent_order",
        "sequence",
        "volume",
        "delay",
        "reference_data_point",
        "offset_type",
        "offset_num",
        "lift_hit_active",
        "lift_hit_reference_data_point",
        "lift_hit_offset_type",
        "lift_hit_offset_num",
        "lift_hit_delay"
    )


class ParentOrderAdmin(admin.ModelAdmin):
    model = ParentOrder
    # list_display = (
    #     'intervention',
    #     'types',
    #     'signed_date'
    # )
    # search_fields = ('intervention', )
    # list_filter = (
    #     'intervention',
    #     'types'
    # )
    fields = (
        "strategy",
        "action",
        "volume",
        "security",
        "exchange",
        "limit_price",
        "bias",
        "bias_net",
        "num_slices"
    )
    inlines = [
        SliceAdmin,
    ]


class SlicePriceAdmin(admin.TabularInline):
    model = SlicePrice


admin.site.register(ParentOrder, ParentOrderAdmin)
admin.site.register(SliceLiftHit)
admin.site.register(SlicePrice)
admin.site.register(SliceDelay)
admin.site.register(Security)
admin.site.register(Strategy)
admin.site.register(Exchange)