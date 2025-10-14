# API Документация - Система регистрации и авторизации

## Базовый URL
```
http://localhost:8000/api/v1/users/
```

## Эндпоинты

### 1. Регистрация пользователя
**POST** `/register/`

**Описание:** Регистрация нового пользователя с подтверждением номера телефона

**Тело запроса:**
```json
{
    "first_name": "Иван",
    "last_name": "Иванов", 
    "phone_number": "+77771234567",
    "region": 1,
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "terms_accepted": true
}
```

**Успешный ответ (201):**
```json
{
    "success": true,
    "message": "Регистрация прошла успешно. Код подтверждения отправлен на ваш номер телефона.",
    "phone_number": "+77771234567"
}
```

### 2. Подтверждение номера телефона
**POST** `/verify-phone/`

**Описание:** Подтверждение номера телефона с помощью SMS кода

**Тело запроса:**
```json
{
    "phone_number": "+77771234567",
    "code": "1111"
}
```

**Успешный ответ (200):**
```json
{
    "success": true,
    "message": "Регистрация прошла успешно"
}
```

**Примечание:** Временная заглушка - только код `1111` считается правильным

### 3. Вход в систему
**POST** `/login/`

**Описание:** Авторизация пользователя

**Тело запроса:**
```json
{
    "phone_number": "+77771234567",
    "password": "securepassword123"
}
```

**Успешный ответ (200):**
```json
{
    "success": true,
    "message": "Вход выполнен успешно",
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    },
    "user": {
        "id": 1,
        "first_name": "Иван",
        "last_name": "Иванов",
        "phone_number": "+77771234567"
    }
}
```

### 4. Запрос сброса пароля
**POST** `/password-reset/`

**Описание:** Запрос сброса пароля с отправкой кода подтверждения

**Тело запроса:**
```json
{
    "phone_number": "+77771234567"
}
```

**Успешный ответ (200):**
```json
{
    "success": true,
    "message": "Код подтверждения отправлен на ваш номер телефона"
}
```

### 5. Подтверждение сброса пароля
**POST** `/password-reset-confirm/`

**Описание:** Подтверждение сброса пароля с новым паролем

**Тело запроса:**
```json
{
    "phone_number": "+77771234567",
    "code": "1111",
    "new_password": "newpassword123",
    "new_password_confirm": "newpassword123"
}
```

**Успешный ответ (200):**
```json
{
    "success": true,
    "message": "Пароль успешно сброшен"
}
```

### 6. Получение списка регионов
**GET** `/regions/`

**Описание:** Получение списка доступных регионов

**Успешный ответ (200):**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Алматы",
            "code": "ALM"
        },
        {
            "id": 2,
            "name": "Астана", 
            "code": "AST"
        }
    ]
}
```

### 7. Получение профиля пользователя
**GET** `/profile/`

**Описание:** Получение данных профиля текущего пользователя

**Заголовки:** `Authorization: Bearer <access_token>`

**Успешный ответ (200):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "first_name": "Иван",
        "last_name": "Иванов",
        "phone_number": "+77771234567",
        "region": 1,
        "region_name": "Алматы",
        "is_phone_verified": true,
        "date_joined": "2025-10-14T16:13:08Z"
    }
}
```

### 8. Обновление профиля пользователя
**PUT/PATCH** `/profile/update/`

**Описание:** Обновление данных профиля пользователя (имя, фамилия, регион)

**Заголовки:** `Authorization: Bearer <access_token>`

**Тело запроса:**
```json
{
    "first_name": "Петр",
    "last_name": "Петров",
    "region": 2
}
```

**Успешный ответ (200):**
```json
{
    "success": true,
    "message": "Профиль успешно обновлен",
    "data": {
        "first_name": "Петр",
        "last_name": "Петров",
        "region": 2,
        "region_name": "Астана"
    }
}
```

### 9. Смена пароля
**POST** `/profile/change-password/`

**Описание:** Смена пароля пользователя

**Заголовки:** `Authorization: Bearer <access_token>`

**Тело запроса:**
```json
{
    "current_password": "oldpassword123",
    "new_password": "newpassword123",
    "new_password_confirm": "newpassword123"
}
```

**Успешный ответ (200):**
```json
{
    "success": true,
    "message": "Пароль успешно изменен"
}
```

## Коды ошибок

### 400 Bad Request
```json
{
    "success": false,
    "message": "Ошибка при регистрации",
    "errors": {
        "phone_number": ["Пользователь с таким номером телефона уже существует"],
        "password_confirm": ["Пароли не совпадают"]
    }
}
```

### 401 Unauthorized
```json
{
    "success": false,
    "message": "Неверный номер телефона или пароль",
    "errors": {
        "non_field_errors": ["Неверный номер телефона или пароль"]
    }
}
```

## Особенности реализации

1. **Временная заглушка SMS:** Только код `1111` считается правильным для подтверждения
2. **JWT токены:** Используется для аутентификации после входа
3. **Валидация паролей:** Применяются стандартные валидаторы Django
4. **Уникальность номера:** Номер телефона должен быть уникальным
5. **Согласие с условиями:** Обязательное поле при регистрации

## Тестирование

Для тестирования API можно использовать:
- Postman
- curl
- Swagger UI: `http://localhost:8000/api/swagger/`
- ReDoc: `http://localhost:8000/api/redoc/`

## Примеры curl запросов

### Регистрация
```bash
curl -X POST http://localhost:8000/api/v1/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Иван",
    "last_name": "Иванов",
    "phone_number": "+77771234567", 
    "region": 1,
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "terms_accepted": true
  }'
```

### Подтверждение номера
```bash
curl -X POST http://localhost:8000/api/v1/users/verify-phone/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+77771234567",
    "code": "1111"
  }'
```

### Вход в систему
```bash
curl -X POST http://localhost:8000/api/v1/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+77771234567",
    "password": "securepassword123"
  }'
```

### Получение профиля
```bash
curl -X GET http://localhost:8000/api/v1/users/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Обновление профиля
```bash
curl -X PATCH http://localhost:8000/api/v1/users/profile/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "first_name": "Петр",
    "last_name": "Петров",
    "region": 2
  }'
```

### Смена пароля
```bash
curl -X POST http://localhost:8000/api/v1/users/profile/change-password/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "current_password": "oldpassword123",
    "new_password": "newpassword123",
    "new_password_confirm": "newpassword123"
  }'
```
