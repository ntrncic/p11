from __future__ import unicode_literals

from django.conf import settings
from django.db import connection
from django.db.models import F, Sum
from celery.utils.log import get_task_logger
from TradingPlatform.celery import app
from TradingPlatform.mixins import Quotes


logger = get_task_logger(__name__)


@app.task
def slice_task():
    '''
    Start a task once slice has been entered.
    '''

    # get quote
    Quotes.



