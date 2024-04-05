from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import requests

MAP_FILENAME = 'map.png'
types = ['Схема', 'Спутник', 'Гибрид']
types_map = {'Схема': 'map', 'Спутник': 'sat', 'Гибрид': 'sat,skl'}


def get_lonlat(search: str, postal_code: bool = True):
    geocoder_apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
    url = f'https://geocode-maps.yandex.ru/1.x?geocode={search}&apikey={geocoder_apikey}&format=json'
    response = requests.get(url)
    json = response.json()
    pos = json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    lon, lat = [float(el) for el in pos.split()]
    full_address = json['response']['GeoObjectCollection']['featureMember'][
        0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
    if postal_code == 'on':
        code = json['response']['GeoObjectCollection']['featureMember'][
            0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        full_address += ' ' + code
    return lon, lat, full_address


def download_image(lon: float, lat: float, point_lon: float, point_lat: float, spn: float, type: str):
    map_url = f'http://static-maps.yandex.ru/1.x/?ll={lon},{lat}&spn={spn},{spn}&l={type}'
    if point_lon is not None and point_lat is not None:
        map_url += f'&pt={point_lon},{point_lat},round'
    response = requests.get(map_url)
    with open(MAP_FILENAME, 'wb') as file:
        file.write(response.content)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./main.ui', self)
        self.spn = 0.02
        self.point_lon, self.point_lat, full_address = get_lonlat(
            'Москва')
        # self.set_full_address(full_address)
        self.lon, self.lat = self.point_lon, self.point_lat
        # self.search_text = 'Москва'

        self.type_box.clear()
        self.type_box.addItems(types)
        self.type_box.setCurrentIndex(0)
        self.type_box.currentTextChanged.connect(self.type_changed)

        self.update_map()

    def update_map(self):
        type_name = self.type_box.currentText()
        type = types_map.get(type_name, 'map')
        download_image(self.lon, self.lat, self.point_lon,
                       self.point_lat, self.spn, type)
        pixmap = QPixmap(MAP_FILENAME)
        self.image_label.setPixmap(pixmap)



    def mousePressEvent(self, event):
        self.remove_focus()

    def type_changed(self, event):
        self.update_map()
