from accounts.models import Client

class TenantMiddleware:
    """
    Middleware to detect tenant by domain
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        host = request.get_host().split(":")[0]

        try:
            tenant = Client.objects.get(domain=host)
            request.tenant = tenant
        except Client.DoesNotExist:
            request.tenant = None

        response = self.get_response(request)

        return response
        