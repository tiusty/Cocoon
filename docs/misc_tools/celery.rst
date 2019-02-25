=========
Celery
=========

We use Celery has our periodic task scheduler and asynchronous task scheduler


Development
-------------

In development to start the celery broker and beat run:
Note: Make sure to be at the cocoon project root

    ::

        celery -A config worker -l info -B

Production
-------------

In Production the celery broker/beat should be Daemonized, refer to the server documentation
    if you desire to do this