from django.core.management.base import BaseCommand
from apps.users.models import User
from apps.users.services import UserService
from apps.permissions.models import Role, Resource, Permission, UserRole


class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Создание ролей...')
        roles = self.create_roles()

        self.stdout.write('Создание ресурсов...')
        resources = self.create_resources()

        self.stdout.write('Создание правил доступа...')
        self.create_permissions(roles, resources)

        self.stdout.write('Создание тестовых пользователей...')
        self.create_users(roles)

        self.stdout.write(self.style.SUCCESS('Готово!'))

    def create_roles(self):
        roles_data = [
            {'name': 'admin', 'description': 'Администратор с полным доступом'},
            {'name': 'manager', 'description': 'Менеджер с расширенным доступом'},
            {'name': 'user', 'description': 'Обычный пользователь'},
        ]
        roles = {}
        for data in roles_data:
            role, _ = Role.objects.get_or_create(name=data['name'], defaults=data)
            roles[role.name] = role
        return roles

    def create_resources(self):
        resources_data = [
            {'code': 'products', 'name': 'Товары', 'description': 'Каталог товаров'},
            {'code': 'orders', 'name': 'Заказы', 'description': 'Заказы пользователей'},
            {'code': 'reports', 'name': 'Отчеты', 'description': 'Отчеты системы'},
        ]
        resources = {}
        for data in resources_data:
            res, _ = Resource.objects.get_or_create(code=data['code'], defaults=data)
            resources[res.code] = res
        return resources

    def create_permissions(self, roles, resources):
        # Admin - полный доступ ко всему
        for res in resources.values():
            Permission.objects.get_or_create(
                role=roles['admin'],
                resource=res,
                defaults={
                    'can_read': True, 'can_read_all': True,
                    'can_create': True,
                    'can_update': True, 'can_update_all': True,
                    'can_delete': True, 'can_delete_all': True,
                }
            )

        # Manager - чтение всего, создание, обновление своего
        for res in resources.values():
            Permission.objects.get_or_create(
                role=roles['manager'],
                resource=res,
                defaults={
                    'can_read': True, 'can_read_all': True,
                    'can_create': True,
                    'can_update': True, 'can_update_all': False,
                    'can_delete': False, 'can_delete_all': False,
                }
            )

        # User - только чтение и работа со своими заказами
        Permission.objects.get_or_create(
            role=roles['user'],
            resource=resources['products'],
            defaults={
                'can_read': True, 'can_read_all': True,
                'can_create': False,
                'can_update': False, 'can_update_all': False,
                'can_delete': False, 'can_delete_all': False,
            }
        )
        Permission.objects.get_or_create(
            role=roles['user'],
            resource=resources['orders'],
            defaults={
                'can_read': True, 'can_read_all': False,
                'can_create': True,
                'can_update': True, 'can_update_all': False,
                'can_delete': True, 'can_delete_all': False,
            }
        )

    def create_users(self, roles):
        users_data = [
            {
                'email': 'admin@test.com',
                'password': 'admin123',
                'first_name': 'Админ',
                'last_name': 'Админов',
                'role': 'admin'
            },
            {
                'email': 'manager@test.com',
                'password': 'manager123',
                'first_name': 'Менеджер',
                'last_name': 'Менеджеров',
                'role': 'manager'
            },
            {
                'email': 'user@test.com',
                'password': 'user123',
                'first_name': 'Пользователь',
                'last_name': 'Пользователев',
                'role': 'user'
            },
        ]

        for data in users_data:
            if not User.objects.filter(email=data['email']).exists():
                user = UserService.create_user(
                    email=data['email'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['last_name']
                )
                # Удаляем дефолтную роль user и назначаем нужную
                UserRole.objects.filter(user=user).delete()
                UserRole.objects.create(user=user, role=roles[data['role']])
                self.stdout.write(f"  Создан: {data['email']} ({data['role']})")
