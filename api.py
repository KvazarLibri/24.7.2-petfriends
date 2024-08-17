import requests
from settings import EMAIL, PASSWORD

BASE_URL = 'https://petfriends.skillfactory.ru/api'

def get_auth_key():
    """Получить API ключ."""
    response = requests.get(f'{BASE_URL}/key', headers={'email': EMAIL, 'password': PASSWORD})
    response.raise_for_status()
    print("get_auth_key response:", response.json())  # Вывод ответа
    return response.json()['key']

def create_pet_simple(auth_key, name, animal_type, age):
    """Добавить информацию о новом питомце без фото."""
    headers = {'auth_key': auth_key}
    data = {'name': name, 'animal_type': animal_type, 'age': age}
    response = requests.post(f'{BASE_URL}/create_pet_simple', headers=headers, data=data)
    response.raise_for_status()
    print("create_pet_simple response:", response.json())  # Вывод ответа
    return response.json()

def get_pets(auth_key, filter=None):
    """Получить список питомцев."""
    headers = {'auth_key': auth_key}
    params = {'filter': filter} if filter else {}
    response = requests.get(f'{BASE_URL}/pets', headers=headers, params=params)
    response.raise_for_status()
    print("get_pets response:", response.json())  # Вывод ответа
    return response.json()

def add_pet(auth_key, name, animal_type, age, pet_photo=None):
    """Добавить информацию о новом питомце с фото."""
    data = {
        'name': name,
        'animal_type': animal_type,
        'age': age
    }
    headers = {'auth_key': auth_key}

    files = {}
    if pet_photo:
        files = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

    response = requests.post(f'{BASE_URL}/pets', headers=headers, data=data, files=files)
    response.raise_for_status()
    print("add_pet response:", response.json())  # Вывод ответа
    return response.json()

def set_pet_photo(auth_key, pet_id, pet_photo):
    """Добавить фото питомца."""
    headers = {'auth_key': auth_key}
    files = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
    response = requests.post(f'{BASE_URL}/pets/set_photo/{pet_id}', headers=headers, files=files)
    response.raise_for_status()
    print("set_pet_photo response:", response.json())  # Вывод ответа
    return response.json()

def update_pet(auth_key, pet_id, name=None, animal_type=None, age=None):
    """Обновить информацию о питомце."""
    headers = {'auth_key': auth_key}
    data = {'name': name, 'animal_type': animal_type, 'age': age}
    data = {key: value for key, value in data.items() if value is not None}
    response = requests.put(f'{BASE_URL}/pets/{pet_id}', headers=headers, data=data)
    response.raise_for_status()
    print("update_pet response:", response.json())  # Вывод ответа
    return response.json()

def delete_pet(auth_key, pet_id):
    """Удалить питомца."""
    headers = {'auth_key': auth_key}
    response = requests.delete(f'{BASE_URL}/pets/{pet_id}', headers=headers)
    print("delete_pet response status_code:", response.status_code)  # Вывод статус-кода
    print("delete_pet response text:", response.text)  # Вывод текста ответа
    response.raise_for_status()  # Проверка на ошибки HTTP
    return response
