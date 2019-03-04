from __future__ import absolute_import, unicode_literals
from celery import shared_task

from cocoon.houseDatabase.management.commands.pull_all_homes_images import Command


@shared_task()
def pull_all_homes_images():
    home_puller = Command()
    home_puller.handle()
