from cocoon.userAuth.models import MyUser


def get_agent_client_queryset(user_profile):
    if user_profile.user.is_broker:
        referred_profile_clients = user_profile.user.referred_clients.all()
        referred_clients = MyUser.objects.filter(userProfile__in=referred_profile_clients)
        itinerary_clients = user_profile.user.scheduled_tours.all().filter(finished=False)
        aquired_clients = MyUser.objects.filter(my_tours=itinerary_clients)
        agent_queryset = aquired_clients | referred_clients
        return agent_queryset
    else:
        return None
