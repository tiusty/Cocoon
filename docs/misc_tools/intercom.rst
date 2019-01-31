==========
Intercom
==========

Intercom is the client messaging tool we use. This helps us interact and aid customers who
are using the website

Doc from this site: https://github.com/kencochrane/django-intercom

Documentation
=============
Documentation is also available online at http://django-intercom.readthedocs.org

Installation
============
1. Install django-intercom using easy_setup or pip::

    pip install django-intercom


2. add intercom to your INSTALLED_APPS in your django settings file::

    INSTALLED_APPS = (
        # all
        # other
        # apps
        'django_intercom',
    )

3. Add "INTERCOM_APPID" setting to your django settings file with your intercom application Id.

    in settings.py::

        INTERCOM_APPID = "your appID"

4. Add the template tag code into your base template before the body tag.

    At the top of the page put this::

    {% load intercom %}

    At the bottom of the page before the </body> tag put this::

    {% intercom_tag %}


User Data
=========
By default, django-intercom will send the following user information to intercom.io:

1. user_id (sourced from request.user.id)
2. email (sourced from request.user.email)
3. name (sourced from request.user.username or, and as a fallback, request.user.get_username())
4. created_at (sourced from request.user.date_joined)
5. user_hash (calculated using INTERCOM_SECURE_KEY and user_id, if INTERCOM_SECURE_KEY is set)

You can override any or all of fields 1-4 by creating a Class with a user_data method that accepts a Django User model as an argument. The method should return a dictionary containing any or all of the keys **user_id**, **email**, **name** and **user_created**, and the desired values for each. Note that the user_created key must contain a datetime. Here is an example::

    from django.utils.dateformat import DateFormat

    class IntercomUserData:
        """ User data class located anywhere in your project
            This one is located in thepostman/utils/user_data.py """

        def user_data(self, user):
            """ Required method, same name and only accepts one attribute (django User model) """

            return {
                'name' : user.userprofile.name,
            }

You will need to register your class with django-intercom so that it knows where to find it. You do this by adding the class to the INTERCOM_USER_DATA_CLASS setting.

INTERCOM_USER_DATA_CLASS
---------------------------
Default = None

in settings.py::

    INTERCOM_USER_DATA_CLASS = 'thepostman.utils.user_data.IntercomUserData'

Custom Data
===========
Intercom.io allows you to send them your own custom data, django-intercom makes this easy. All you need to do it create a Class with a custom_data method that accepts a Django User model as an argument and returns a dictionary. Here is an example::

    from thepostman.models import message

    class IntercomCustomData:
        """ Custom data class located anywhere in your project
            This one is located in thepostman/utils/custom_data.py """

        def custom_data(self, user):
            """ Required method, same name and only accepts one attribute (django User model) """

            num_messages = message.objects.filter(user=user).count()
            num_unread = messages.objects.filter(user=user, read=False).count()

            return {
                'num_messages' : num_messages,
                'num_unread' : num_unread,
            }

Once you have your classes built, you will need to register them with django-intercom so that it knows where to find them. You do this by adding the class to the INTERCOM_CUSTOM_DATA_CLASSES setting. It is important to note that if you have the same dict key returned in more then one Custom Data Class the last class that is run (lower in the list) will overwrite the previous ones.

INTERCOM_CUSTOM_DATA_CLASSES
----------------------------
Default = None

in settings.py::

    INTERCOM_CUSTOM_DATA_CLASSES = [
        'thepostman.utils.custom_data.IntercomCustomData',
    ]



