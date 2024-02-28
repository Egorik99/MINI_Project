import requests
from io import BytesIO
import pygame
from PIL import Image


ADDRESS = "Kremlin, Moscow, Russia"




def get_coordinates(address):
    url = f'https://geocode-maps.yandex.ru/1.x/?apikey=48246e0a-edd3-493c-9103-fd746c514c49&format=json&geocode={address}'
    response = requests.get(url)
    print(f"get coordinates response {response.status_code}", response.content)
    json_data = response.json()
    try:
        coordinates_str = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        longitude, latitude = map(float, coordinates_str.split())
        return latitude, longitude
    except (KeyError, IndexError, ValueError):
        return None, None

spn1 = 0.016457
spn2 = 0.00619

def get_static_map_image(latitude, longitude, zoom=12, size=(1200, 900)):
    url = f'https://static-maps.yandex.ru/v1?lang=ru_RU&ll={longitude},{latitude}&apikey=04f37f19-a565-4e59-98cf-f55d20c117fa&zoom={zoom}&spn={spn1},{spn2}'
    response = requests.get(url)
    print(f"Get image by given coordinates resposne {response.status_code}", response.content)
    return BytesIO(response.content)


pygame.init()

# Set up the display
map_size = (1200, 900)
screen = pygame.display.set_mode(map_size)
pygame.display.set_caption('Yandex Map')

# Get coordinates
latitude, longitude = get_coordinates(ADDRESS)
if latitude is not None and longitude is not None:
    map_image_data = get_static_map_image(latitude, longitude, size=map_size, zoom=20)
    print(map_image_data)

    img = Image.open(map_image_data)
    img = img.convert('RGBA')
    image = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
    image = pygame.transform.scale(image, (1200, 900))
else:
    print('Coordinates not found.')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.blit(image, (0, 0))
    pygame.display.flip()
