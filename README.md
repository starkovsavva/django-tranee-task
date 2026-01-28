# Система аутентификации и авторизации

Backend-приложение с собственной системой аутентификации и авторизации на Django + DRF + PostgreSQL.

## Схема разграничения прав доступа

Система построена на ролевой модели доступа (RBAC).

### Таблицы БД

1. **users** - пользователи системы
   - id, email, password_hash, first_name, last_name, patronymic
   - is_active - флаг для мягкого удаления

2. **sessions** - сессии пользователей
   - id, user_id, token, expires_at, is_active
   - Хранит JWT токены для возможности инвалидации

3. **roles** - роли (admin, manager, user)
   - id, name, description

4. **user_roles** - связь пользователей и ролей
   - user_id, role_id
   - Пользователь может иметь несколько ролей

5. **resources** - ресурсы системы (products, orders, reports)
   - id, code, name, description

6. **permissions** - правила доступа
   - role_id, resource_id
   - can_read - чтение своих объектов
   - can_read_all - чтение всех объектов
   - can_create - создание
   - can_update - обновление своих
   - can_update_all - обновление всех
   - can_delete - удаление своих
   - can_delete_all - удаление всех

### Логика проверки прав

1. При запросе middleware извлекает JWT токен из заголовка Authorization
2. Проверяется валидность токена и активность сессии в БД
3. Определяются роли пользователя
4. Для каждой роли проверяются права на запрашиваемый ресурс и действие
5. Если право есть хотя бы у одной роли - доступ разрешен

### Тестовые роли

- **admin** - полный доступ ко всем ресурсам
- **manager** - чтение всего, создание, обновление своего
- **user** - чтение товаров, работа со своими заказами

## Запуск

```bash
docker-compose up --build
```

Приложение будет доступно на http://localhost:8000

## Тестовые пользователи

| Email | Пароль | Роль |
|-------|--------|------|
| admin@test.com | admin123 | admin |
| manager@test.com | manager123 | manager |
| user@test.com | user123 | user |

## API

### Аутентификация

```
POST /api/auth/login/          - вход (email, password)
POST /api/auth/logout/         - выход
```

### Пользователи

```
POST /api/users/register/      - регистрация
GET /api/users/profile/        - получить профиль
PATCH /api/users/profile/      - обновить профиль
DELETE /api/users/profile/     - мягкое удаление
```

### Права доступа (только admin)

```
GET /api/permissions/roles/           - список ролей
GET /api/permissions/resources/       - список ресурсов
GET /api/permissions/rules/           - список правил
PATCH /api/permissions/rules/{id}/    - изменить правило
GET /api/permissions/user-roles/      - назначения ролей
POST /api/permissions/user-roles/     - назначить роль
DELETE /api/permissions/user-roles/{id}/ - убрать роль
GET /api/permissions/my/              - мои права
```

### Бизнес-объекты (mock)

```
GET/POST /api/business/products/
GET/PATCH/DELETE /api/business/products/{id}/
GET/POST /api/business/orders/
GET/PATCH/DELETE /api/business/orders/{id}/
GET /api/business/reports/
```

## Примеры запросов

Вход:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@test.com", "password": "admin123"}'
```

Запрос с токеном:
```bash
curl http://localhost:8000/api/business/products/ \
  -H "Authorization: Bearer <token>"
```

## Коды ответов

- 200 - успех
- 201 - создано
- 400 - ошибка валидации
- 401 - не аутентифицирован
- 403 - доступ запрещен
- 404 - не найдено
