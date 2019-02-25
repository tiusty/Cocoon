from __future__ import absolute_import, unicode_literals
from celery import task, shared_task

@task()
def task_number_one():
    print('task3')

@shared_task
def add(x, y):
    return x + y
