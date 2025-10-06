import jwt
import datetime
from django.conf import settings
from .models import BusinessElement, AccessRoleRule
def generate_jwt(user):
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.datetime.now() + datetime.timedelta(seconds=3600),
        "iat": datetime.datetime.now(),
    }
    token = jwt.encode(payload,"secret", algorithm="HS256")
    return token
def decode_jwt(token):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return payload
    #просроченный токен 
    except jwt.ExpiredSignatureError:
        return None
    #неправильный токен 
    except jwt.InvalidTokenError:
        return None  
def has_permission(user, element_name, action):
    """Check if a user has permission for an action on a business element."""

    element = BusinessElement.objects.get(name=element_name)
    rule = AccessRoleRule.objects.get(role=user.role, element=element)
   

    action_map = {
        "read": rule.read_permission,
        "read_all": rule.read_all_permission,
        "create": rule.create_permission,
        "update": rule.update_permission,
        "update_all": rule.update_all_permission,
        "delete": rule.delete_permission,
        "delete_all": rule.delete_all_permission,
    }

    return action_map.get(action)