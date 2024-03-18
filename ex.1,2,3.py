import sys

import pygame
import requests
from io import BytesIO
from PIL import Image

API_KEY = '48246e0a-edd3-493c-9103-fd746c514c49'
API_MAP_KEY = '04f37f19-a565-4e59-98cf-f55d20c117fa'
# ADDRESS = '1600 Amphitheatre Parkway, Mountain View, CA'  # Example address
ADDRESS = "Kiev, Ukraine, Mulberry, 12"


def get_coordinates(address):
    url = f'https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&format=json&geocode={address}'
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
    url = f'https://static-maps.yandex.ru/v1?lang=ru_RU&ll={longitude},{latitude}&apikey={API_MAP_KEY}&zoom={zoom}&spn={spn1},{spn2}'
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
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                try:
                    spn1 += 1
                    spn2 += 1
                except:
                    pass
            elif event.key == pygame.K_0:
                try:
                    spn1 -= 1
                    spn2 -= 1
                except:
                    pass
            elif event.key == pygame.K_UP:
                latitude -= 0.001
            elif event.key == pygame.K_DOWN:
                latitude += 0.001
            elif event.key == pygame.K_RIGHT:
                longitude += 0.001
            elif event.key == pygame.K_LEFT:
                longitude -= 0.001

            try:
                map_image_data = get_static_map_image(latitude, longitude, size=map_size)
                print(map_image_data)
                img = Image.open(map_image_data)

                img = img.convert('RGBA')
                image = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
                image = pygame.transform.scale(image, (1200, 900))
            except:
                pass

    # Draw the map image on the screen
    screen.blit(image, (0, 0))
    pygame.display.flip()


pygame.quit()