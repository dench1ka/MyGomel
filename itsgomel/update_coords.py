import requests
import time
from main.models import Mural  # Замени main на имя своего приложения


def prepare_address(address):
    address = address.strip()
    # Заменяем разные варианты слова "улица" на "ул."
    address = address.replace("улице", "ул.")
    address = address.replace("улица", "ул.")
    address = address.replace("проспект", "пр-т")
    # Добавляем город, если его нет
    if "гомель" not in address.lower():
        address = "Гомель, " + address
    # Добавляем страну, если её нет
    if "беларусь" not in address.lower():
        address += ", Беларусь"
    return address


def get_coords_from_address(address):
    try:
        address = prepare_address(address)
        print(f"Геокодируем адрес: {address}")
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'q': address,
            'format': 'json',
            'limit': 1,
            'addressdetails': 0,
        }
        headers = {'User-Agent': 'MyMuralApp/1.0 (myemail@example.com)'}
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        print("Ответ сервера:", data)
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
    except Exception as e:
        print(f"Ошибка геокодирования адреса '{address}': {e}")
    return None, None


def update_murals_coords():
    murals_without_coords = Mural.objects.filter(latitude__isnull=True, longitude__isnull=True)
    total = murals_without_coords.count()
    print(f"Найдено мурaлов без координат: {total}")

    for idx, mural in enumerate(murals_without_coords, 1):
        lat, lon = get_coords_from_address(mural.address)
        if lat is not None and lon is not None:
            mural.latitude = lat
            mural.longitude = lon
            mural.save()
            print(f"{idx}/{total}. Обновлено: '{mural.title}' -> {lat}, {lon}")
        else:
            print(f"{idx}/{total}. Координаты не найдены для '{mural.title}'")

        time.sleep(1)  # Пауза между запросами, чтобы не перегружать сервер


if __name__ == "__main__":
    update_murals_coords()
