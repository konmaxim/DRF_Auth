
from DRFAuth.models import Role, BusinessElement, AccessRoleRule, CustomUser

def populate_db():
    roles = ["admin", "manager", "user", "guest"]
    role_objs = {}
    for r in roles:
        obj, _ = Role.objects.get_or_create(name=r)
        role_objs[r] = obj

    elements = [
        "Управление пользователями",
        "Товары магазина",
        "Магазины",
        "Заказы",
        "Управление правилами доступа"
    ]
    element_objs = {}
    for e in elements:
        obj, _ = BusinessElement.objects.get_or_create(name=e)
        element_objs[e] = obj


    rules_data = [
        # role_name, element_name, read, read_all, create, update, update_all, delete, delete_all
        ("admin", "Управление пользователями", True, True, True, True, True, True, True),
        ("manager", "Управление пользователями", True, True, False, True, True, False, False),
        ("user", "Управление пользователями", True, False, False, True, False, True, False),
        ("guest", "Управление пользователями", False, False, False, False, False, False, False),

        ("admin", "Товары магазина", True, True, True, True, True, True, True),
        ("manager", "Товары магазина", True, True, True, True, True, True, True),
        ("user", "Товары магазина", True, True, False, False, False, False, False),
        ("guest", "Товары магазина", True, True, False, False, False, False, False),

        ("admin", "Магазины", True, True, True, True, True, True, True),
        ("manager", "Магазины", True, True, True, False, False, False, False),
        ("user", "Магазины", True, False, False, False, False, False, False),
        ("guest", "Магазины", False, False, False, False, False, False, False),

        ("admin", "Заказы", True, True, True, True, True, True, True),
        ("manager", "Заказы", True, True, True, True, True, True, True),
        ("user", "Заказы", True, False, True, True, False, False, False),
        ("guest", "Заказы", False, False, False, False, False, False, False),

        ("admin", "Управление правилами доступа", True, True, True, True, True, True, True),
        ("manager", "Управление правилами доступа", False, False, False, False, False, False, False),
        ("user", "Управление правилами доступа", False, False, False, False, False, False, False),
        ("guest", "Управление правилами доступа", False, False, False, False, False, False, False),
    ]

    for role_name, element_name, *perms in rules_data:
        role = Role.objects.get(name=role_name)
        element = BusinessElement.objects.get(name=element_name)
        AccessRoleRule.objects.update_or_create(
            role=role,
            element=element,
            defaults={
                "read_permission": perms[0],
                "read_all_permission": perms[1],
                "create_permission": perms[2],
                "update_permission": perms[3],
                "update_all_permission": perms[4],
                "delete_permission": perms[5],
                "delete_all_permission": perms[6],
            }
        )

    def new_user(full_name, email, role_name):
        user = CustomUser(
        email=email,
        full_name=full_name,
        role=Role.objects.get(name=role_name)
        )
        user.set_password('test1234')  
        user.save()
    new_user("Петров Иван Сергеевич", "petrov@example.com", "admin")
    new_user("Иванова Мария Александровна", "ivanova@example.com", "manager")
    new_user("Соколов Дмитрий Андреевич", "sokolov@example.com", "user")
    new_user("Смирнова Анна Владимировна", "smirnova@example.com", "guest")

