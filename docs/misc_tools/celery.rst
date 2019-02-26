=========
Celery
=========

We use Celery has our periodic task scheduler and asynchronous task scheduler


Development
-------------

In development to start the celery broker and beat run:
Note: Make sure to be at the cocoon project root and have the virtual environment loaded

    ::

        celery -A config worker -l info -B

Production
-------------

In Production the celery broker/beat should be Daemonized, refer to the server documentation
    if you desire to do this.


To install on server:

Make sure file patterns have been followed, i.e

The project lives at:
/home/ubuntu/work/Cocoon

The main user is ubuntu etc

The virtualenv is installed at the correct spot

To Install:

    ::
        # Celery should have already been instead via the requirments file

        # Install RabbitMQ as broker
        sudo apt-get install rabbitmq-server

        sudo ln -s ~/work/Cocoon/config/celery_config/celeryd.service  /etc/systemd/system/celeryd.service
        sudo ln -s ~/work/Cocoon/config/celery_config/celeryd  /etc/default/celeryd

        # Create the logging folders and permissions
        sudo mkdir /var/log/celery /var/run/celery
        sudo chown ubuntu:ubuntu /var/log/celery /var/run/celery

        # Reload systemctl daemon
        sudo systemctl daemon-reload

        # Enable on startup
        sudo systemctl enable celery

        # Start the service
        sudo systemctl start celeryd

If changes are made to the code, to update the celery make sure
sudo systemctl restart celeryd

is run to load new changes
