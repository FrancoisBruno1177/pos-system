from accounts.models import Client


def total_clients():

    return Client.objects.count()
    