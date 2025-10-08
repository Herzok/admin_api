from .models import UserProxy

class AnonymousUser:
    is_authenticated = False
    is_anonymous = True

class CustomUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            try:
                request.user = UserProxy.objects.get(id=user_id)
            except UserProxy.DoesNotExist:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        return self.get_response(request)