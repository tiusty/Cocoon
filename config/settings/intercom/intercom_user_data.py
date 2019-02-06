class IntercomUserData:
    """ Allows intercom to inject user information to the intercom conversation """

    def user_data(self, user):
        """ Required method, same name and only accepts one attribute (django User model) """

        return {
            'user_id': user.id,
            'name': user.full_name,
            'email': user.email,
            'created_at': user.joined,
        }


class IntercomCustomData:
    """ Allows intercom to inject custom information to the intercom conversation """

    def custom_data(self, user):
        """ Required method, same name and only accepts one attribute (django User model) """

        return {
            'phone': user.phone_number,
        }
