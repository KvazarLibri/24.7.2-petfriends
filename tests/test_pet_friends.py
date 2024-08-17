import pytest
import os
import requests
from api import get_auth_key, create_pet_simple, get_pets, add_pet, set_pet_photo, update_pet, delete_pet

@pytest.fixture
def auth_key():
    """Фикстура для получения API ключа перед каждым тестом."""
    return get_auth_key()

def test_get_auth_key():
    """Тест получения API ключа."""
    key = get_auth_key()
    print("test_get_auth_key:", key)  # Вывод ответа
    assert key is not None
    assert isinstance(key, str)

def test_create_pet_simple(auth_key):
    """Тест создания питомца без фото."""
    result = create_pet_simple(auth_key, "Мурзик", "Кот", "4")
    print("test_create_pet_simple:", result)  # Вывод ответа
    assert result['name'] == "Мурзик"
    assert result['animal_type'] == "Кот"
    assert result['age'] == "4"

def test_get_pets(auth_key):
    """Тест получения списка питомцев."""
    result = get_pets(auth_key)
    print("test_get_pets:", result)  # Вывод ответа
    assert 'pets' in result
    assert isinstance(result['pets'], list)

def test_add_pet(auth_key):
    """Тест создания питомца с фото."""
    pet_photo_path = 'D:/Other/petfriends/tests/images/images.jpeg'
    if not os.path.isfile(pet_photo_path):
        pytest.fail(f"Файл не найден по пути {pet_photo_path}")

    try:
        result = add_pet(auth_key, "Барсик", "Кот", "3", pet_photo=pet_photo_path)
        print("test_add_pet:", result)  # Вывод ответа
        assert result['name'] == "Барсик"
        assert result['animal_type'] == "Кот"
        assert result['age'] == "3"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTP error occurred: {e}")

def test_set_pet_photo(auth_key):
    """Тест добавления фото к существующему питомцу."""
    pet_id = "e75dbae9-c042-4462-8f1f-4349e763eb05"
    pet_photo_path = 'D:/Other/petfriends/tests/images/images.jpeg'
    if not os.path.isfile(pet_photo_path):
        pytest.fail(f"Файл не найден по пути {pet_photo_path}")

    try:
        result = set_pet_photo(auth_key, pet_id, pet_photo_path)
        print("test_set_pet_photo:", result)  # Вывод ответа
        assert 'pet_photo' in result
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTP error occurred: {e}")

def test_update_pet(auth_key):
    """Тест обновления информации о питомце."""
    pet_id = "e75dbae9-c042-4462-8f1f-4349e763eb05"
    try:
        result = update_pet(auth_key, pet_id, name="Барсик2", animal_type="Кот", age="5")
        print("test_update_pet:", result)  # Вывод ответа
        assert result['name'] == "Барсик2"
        assert result['animal_type'] == "Кот"
        assert result['age'] == "5"
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTP error occurred: {e}")

def test_delete_pet(auth_key):
    """Тест удаления питомца."""
    pet_id = "e75dbae9-c042-4462-8f1f-4349e763eb05"

    # Удаление питомца
    try:
        response = delete_pet(auth_key, pet_id)
        print("test_delete_pet status_code:", response.status_code)  # Вывод статус-кода
        print("test_delete_pet text:", response.text)  # Вывод текста ответа

        # Проверка, что питомец действительно удален
        pets_list = get_pets(auth_key)
        pet_ids = [pet['id'] for pet in pets_list['pets']]
        assert pet_id not in pet_ids  # Проверка, что питомец больше не в списке
    except requests.exceptions.HTTPError as e:
        pytest.fail(f"HTTP error occurred: {e}")
    except requests.exceptions.JSONDecodeError as e:
        pytest.fail(f"JSON decode error occurred: {e}")
