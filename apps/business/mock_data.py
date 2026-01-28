# Mock данные для бизнес-объектов
# В реальном приложении это были бы записи из БД

PRODUCTS = [
    {'id': 1, 'name': 'Ноутбук', 'price': 50000, 'owner_id': None},
    {'id': 2, 'name': 'Телефон', 'price': 30000, 'owner_id': None},
    {'id': 3, 'name': 'Планшет', 'price': 25000, 'owner_id': None},
]

ORDERS = [
    {'id': 1, 'product_id': 1, 'quantity': 2, 'status': 'new', 'owner_id': 'user1'},
    {'id': 2, 'product_id': 2, 'quantity': 1, 'status': 'processing', 'owner_id': 'user2'},
    {'id': 3, 'product_id': 3, 'quantity': 3, 'status': 'completed', 'owner_id': 'user1'},
]

REPORTS = [
    {'id': 1, 'name': 'Отчет за январь', 'type': 'monthly', 'owner_id': 'admin'},
    {'id': 2, 'name': 'Отчет за февраль', 'type': 'monthly', 'owner_id': 'admin'},
]
