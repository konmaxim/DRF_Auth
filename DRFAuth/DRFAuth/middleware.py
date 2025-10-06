import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser
from .models import Role
User = get_user_model()

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: self.get_jwt_user(request))
    @staticmethod
    def get_jwt_user(request):
        token = request.COOKIES.get("jwt")
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            user_id = payload.get("user_id")
            user = User.objects.filter(id=user_id).first()
            if user:
                return user
        except Exception as e:
            print("JWT decode error:", e)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

        return AnonymousUser()