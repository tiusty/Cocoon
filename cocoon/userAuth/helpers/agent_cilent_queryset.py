from cocoon.userAuth.models import MyUser


def get_agent_client_queryset(user_profile):
    if user_profile.user.is_broker:
        # Retrieve all the clients that were referred to them
        referred_profile_clients = user_profile.user.referred_clients.all()
        referred_clients = MyUser.objects.filter(userProfile__in=referred_profile_clients)

        # Retrieve all the clients that have an active itinerary with this agent
        itinerary_clients = user_profile.user.scheduled_tours.all().filter(finished=False)
        aquired_clients = MyUser.objects.filter(my_tours=itinerary_clients)

        # Get the union of the querysets
        agent_queryset = aquired_clients.union(referred_clients)

        # Return the union of the querysets
        return agent_queryset
    else:
        return None
