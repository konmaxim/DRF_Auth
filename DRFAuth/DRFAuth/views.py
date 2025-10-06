from django.shortcuts import render
from .forms import RegistrationForm
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.conf import settings
from datetime import datetime, timedelta
from .utils import has_permission
from .models import Role, AccessRoleRule, BusinessElement,CustomUser


def index(request):
    # Пример данных о товарах
    products = [
        {"name": "Ноутбук ", "price": 90000, "in_stock": True},
        {"name": "Смартфон ", "price": 50000, "in_stock": True},
        {"name": "Наушники", "price": 9500, "in_stock": False},
    ]
    return render(request, "index.html", {"products": products})
class RegisterAPI(APIView):
    """
    Пример запроса: 
    {"full_name": "Bykov Andrey Yevgenyevich", "email": "abc123@test.com", "password1": "test1234", "password2": "test1234" }
    
    """
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"detail": "Вы уже авторизованы"}, status=400)
        return Response({"detail": "Отправьте POST с full_name (ФИО) email, password1 и password 2 (повтор пароли)"})
    def post(self, request):
        if request.user.is_authenticated:
            return Response({"detail": "Вы уже авторизованы"}, status=400)
        form = RegistrationForm(request.data)
        if form.is_valid():
            user = form.CreateUser()
            return Response(
                {"message": "Пользователь зарегистрирован успешно", "user_id": user.id},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginAPI(APIView):    
    """
    С тестовыми данными: 
    admin: {"email": "petrov@example.com", "password":"test1234"}
    manager: {"email": "ivanova@example.com", "password":"test1234"}
    user: {"email": "sokolov@example.com", "password":"test1234"}
    guest: {"email":"smirnova@example.com", "password":"test1234"}
    
    """
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"detail": "Вы уже авторизованы"}, status=400)
        return Response({"detail": "Отправьте POST с email и password"})
    def post(self, request):
        if request.user.is_authenticated:
            return Response({"error": "Вы уже авторизованы"}, status=400)
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            access_token = jwt.encode({
                "user_id": user.id,
                "email": user.email,
                "exp": datetime.now() + timedelta(minutes=1)}, "secret", algorithm="HS256")
            refresh_token = jwt.encode({
                "user_id": user.id,
                "exp": datetime.now() + timedelta(days=1)}, "secret", algorithm="HS256")
            response = Response({"access": access_token}) 
            response.set_cookie( key="jwt", value=refresh_token, secure=True, samesite="None", max_age=24 *60 *60 ) 
            return response

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
class LogoutView(APIView):
    """Пост для выхода из системы"""
    def post(self, request):
        if request.user.is_authenticated:
            response = Response({"message": "Logged out"})
            response.delete_cookie("jwt")
            return response
        else:
            return Response({"error": "Войдите в аккаунт"},status=status.HTTP_401_UNAUTHORIZED )

# Управление пользователями
class UserListView(APIView):
    def get(self, request):
        if not has_permission(request.user, "Управление пользователями", "read_all"):
            return Response({"detail": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)

        users = CustomUser.objects.values("id", "full_name", "email", "role__name")
        return Response(list(users))


class UserDetailView(APIView):
    """
    Получение и обновление профиля авторизованного пользователя.
    PUT:
    - Обновить поля профиля:
        - full_name: Полное имя (автоматически обновляет first_name и last_name)
        - email: Email пользователя
        - password: Новый пароль 
    """
    def get(self, request, pk):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Пользователь не авторизован"}, status=status.HTTP_401_UNAUTHORIZED)
        if user.pk == pk:
            target_user = CustomUser.objects.filter(pk=pk).values("id", "full_name", "email", "role__name").first()
            if not target_user:
                return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
            return Response(target_user)
        return Response({"detail": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Пользователь не авторизован"}, status=status.HTTP_401_UNAUTHORIZED)
        if user.pk == pk:
            target_user = CustomUser.objects.filter(pk=pk).first()
            if not target_user:
                return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
            target_user.full_name = request.data.get("full_name", target_user.full_name)
            target_user.email = request.data.get("email", target_user.email)
            new_password = request.data.get("password")
            if new_password:
                target_user.set_password(new_password)
                target_user.save()
            return Response({"detail": "Профиль успешно обновлён"}, status=status.HTTP_200_OK)

        return Response({"detail": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)
class DeleteAccountAPIView(APIView):
    """
    Мягкое удаление аккаунта на post 
    """
    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {"detail": "Ваш аккаунт деактивирован."},
            status=status.HTTP_200_OK
        )
    
#mock data for views  
MOCK_PRODUCTS = [
    {"id": 1, "name": "iPhone", "owner_id": 1},
    {"id": 2, "name": "MacBook", "owner_id": 3},
    {"id": 3, "name": "AirPods", "owner_id": 3},
]

MOCK_STORES = [
    {"id": 1, "name": "Главный магазин", "owner_id": 1},
    {"id": 2, "name": "Филиал №2", "owner_id": 3},
    {"id": 3, "name": "Филиал №2", "owner_id": 2},
]

MOCK_ORDERS = [
    {"id": 1, "name": "Заказ №1", "owner_id": 2},
    {"id": 2, "name": "Заказ №2", "owner_id": 3},
]

class ProductListView(APIView):
    def get(self, request):
        return Response({"products": MOCK_PRODUCTS})
    def post(self, request):
        if not has_permission(request.user, "Товары магазина", "create"):
            return Response({"detail": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"detail": "Товар успешно создан"}, status=status.HTTP_201_CREATED)


class StoreView(APIView):
    """
    Пользователь(user) видит только свои магазины 
    """
    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Пользователь не авторизован"}, status=status.HTTP_401_UNAUTHORIZED)

        if has_permission(request.user, "Магазины", "read_all"):
            return Response({"stores": MOCK_STORES})

        elif has_permission(request.user, "Магазины", "read"):
            user_stores = [s for s in MOCK_STORES if s["owner_id"] == request.user.id]
            return Response({"stores": user_stores})

        return Response({"detail": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)

class OrderView(APIView):
    """
    Пользователь(user) видит только свои заказы 
    """
    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Пользователь не авторизован"}, status=status.HTTP_401_UNAUTHORIZED)

        if has_permission(request.user, "Заказы", "read_all"):
            return Response({"orders": MOCK_ORDERS})

        elif has_permission(request.user, "Заказы", "read"):
            user_orders = [o for o in MOCK_ORDERS if o["owner_id"] == request.user.id]
            return Response({"orders": user_orders})

        return Response({"detail": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        if not has_permission(request.user, "Заказы", "create"):
            return Response({"detail": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"detail": "Заказ успешно создан"}, status=status.HTTP_201_CREATED)

# Управление правилами доступа
class AccessRuleView(APIView):
    """
    Пример пост-а: 
    {"role": "manager", "element": "Магазины", "delete_permission": "True"  }
    """
    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Пользователь не авторизован"}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission(request.user, "Управление правилами доступа", "read_all"):
            return Response({"detail": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)

        rules = AccessRoleRule.objects.select_related("role", "element").values(
            "id",
            "role__name",
            "element__name",
            "read_permission",
            "read_all_permission",
            "create_permission",
            "update_permission",
            "update_all_permission",
            "delete_permission",
            "delete_all_permission",
        )
        return Response(list(rules))
    def post(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "Пользователь не авторизован"}, status=status.HTTP_401_UNAUTHORIZED)

        if not has_permission(request.user, "Управление правилами доступа", "update_all"):
            return Response({"detail": "Доступ запрещён"}, status=status.HTTP_403_FORBIDDEN)

        role_name = request.data.get("role")
        element_name = request.data.get("element")

        if not role_name or not element_name:
            return Response({"detail": "Не указаны роль или элемент"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            role = Role.objects.get(name=role_name)
            element = BusinessElement.objects.get(name=element_name)
        except (Role.DoesNotExist, BusinessElement.DoesNotExist):
            return Response({"detail": "Роль или элемент не найдены"}, status=status.HTTP_404_NOT_FOUND)

        try:
            rule = AccessRoleRule.objects.get(role=role, element=element)
        except AccessRoleRule.DoesNotExist:
            return Response({"detail": "Правило для данной роли и элемента не найдено"}, status=status.HTTP_404_NOT_FOUND)

        updatable_fields = [
            "read_permission",
            "read_all_permission",
            "create_permission",
            "update_permission",
            "update_all_permission",
            "delete_permission",
            "delete_all_permission",
        ]
        for field in updatable_fields:
            if field in request.data:
                setattr(rule, field, request.data[field])

        rule.save()
        return Response({"detail": "Правило успешно обновлено"}, status=status.HTTP_200_OK)



#API Links
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
#все конечные точки API 
@api_view(['GET'])
def api_root(request, format=None):
    if request.user.is_authenticated:
        user_pk = request.user.pk
    else:
        user_pk = 0  
    return Response({
        'register': reverse('register', request=request, format=format),
        'login': reverse('login', request=request, format=format),
        'logout': reverse('logout', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'user-details_edit': reverse('user-details_edit', kwargs={'pk': user_pk}, request=request, format=format),
        'products': reverse('product-list', request=request, format=format),
        'stores': reverse('store-list', request=request, format=format),
        'orders': reverse('order-list', request=request, format=format),
        'access_rules': reverse('access-rule-list', request=request, format=format),
    })