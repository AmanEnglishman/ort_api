#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации работы API профиля пользователя
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1/users"

def test_profile_api():
    """Тестирование API профиля пользователя"""
    
    print("🚀 Тестирование API профиля пользователя")
    print("=" * 50)
    
    # 1. Регистрация пользователя
    print("\n1. Регистрация пользователя...")
    register_data = {
        "first_name": "Тест",
        "last_name": "Пользователь",
        "phone_number": "+77779998877",
        "region": 1,
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "terms_accepted": True
    }
    
    response = requests.post(f"{BASE_URL}/register/", json=register_data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code != 201:
        print("❌ Ошибка при регистрации")
        return
    
    # 2. Подтверждение номера телефона
    print("\n2. Подтверждение номера телефона...")
    verify_data = {
        "phone_number": "+77779998877",
        "code": "1111"
    }
    
    response = requests.post(f"{BASE_URL}/verify-phone/", json=verify_data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code != 200:
        print("❌ Ошибка при подтверждении номера")
        return
    
    # 3. Вход в систему
    print("\n3. Вход в систему...")
    login_data = {
        "phone_number": "+77779998877",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/login/", json=login_data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code != 200:
        print("❌ Ошибка при входе в систему")
        return
    
    # Получаем токен для авторизации
    access_token = response.json()['tokens']['access']
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 4. Получение профиля
    print("\n4. Получение профиля пользователя...")
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 5. Обновление профиля
    print("\n5. Обновление профиля...")
    update_data = {
        "first_name": "Обновленное",
        "last_name": "Имя",
        "region": 2
    }
    
    response = requests.patch(f"{BASE_URL}/profile/update/", json=update_data, headers=headers)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 6. Смена пароля
    print("\n6. Смена пароля...")
    password_data = {
        "current_password": "testpassword123",
        "new_password": "newpassword123",
        "new_password_confirm": "newpassword123"
    }
    
    response = requests.post(f"{BASE_URL}/profile/change-password/", json=password_data, headers=headers)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 7. Получение списка регионов
    print("\n7. Получение списка регионов...")
    response = requests.get(f"{BASE_URL}/regions/")
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    print("\n✅ Тестирование завершено!")

if __name__ == "__main__":
    try:
        test_profile_api()
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения. Убедитесь, что сервер Django запущен на localhost:8000")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
