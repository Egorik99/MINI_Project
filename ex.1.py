import requests
from io import BytesIO
import pygame


def get_coord():
    r = requests.get("https://geocode-maps.yandex.ru/1.x/?apikey=48246e0a-edd3-493c-9103-fd746c514c49&format=json&geocode=Kremlin, Moscow, Russia")
    a = r.json().get('response').get('GeoObjectCollection').get('featureMember')[0].get('GeoObject').get("Point").get('pos')
    b = list(map(float, a.split(' ')))
    return b

def get_image(lat, long, zoom=12, size=(600, 400)):
    d = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey=48246e0a-edd3-493c-9103-fd746c514c49&format=json&geocode={long},{lat}')
    return BytesIO(d.content)


s = get_coord()
z = get_image(s[0], s[1])
print(z)

pygame.init()

wind = pygame.display.set_mode((600, 400))

pygame.display.set_caption('Yandex Map')

f = pygame.image.load('lion.jpg')
f = pygame.transform.scale(f, (600, 400))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.flip()
    wind.blit(f, (0, 0))
