from django.utils.dateformat import DateFormat


class IntercomUserData:
    """ User data class located anywhere in your project
        This one is located in thepostman/utils/user_data.py """

    def user_data(self, user):
        """ Required method, same name and only accepts one attribute (django User model) """

        return {
            'user_id': user.id,
            'name': user.full_name,
            'email': user.email,
            'created_at': user.joined,
        }


class IntercomCustomData:
    """ User data class located anywhere in your project
        This one is located in thepostman/utils/user_data.py """

    def custom_data(self, user):
        """ Required method, same name and only accepts one attribute (django User model) """

        return {
            'phone': user.phone_number,
        }
