import random
from os.path import isfile


class CitiesGame():
    _cities = dict()
    _filename = None
    _last_letter = None
    _used = list()

    _dead_end_letters = [
        'ё',
        'й',
        'ъ',
        'ы',
        'ь'
    ]

    def __init__(self, filename):
        self._filename = filename
        self.read_cities()

    def get_last_letter(self):
        return self._last_letter


    def has_city(self, city: str):
        if not isinstance(city, str) or len(city) < 1:
            return False
        first_letter = city.strip()[0].lower()
        if (first_letter in self._cities.keys()) and (
                city.capitalize() in self._cities[first_letter]):
                return True
        else:
            return False

    def is_used(self, city):
        if city.capitalize() in self._used:
            return True
        else:
            return False

    def last_letter(self, city: str):
        for i in range(len(city)-1, 0, -1):
            last_letter = city[i].lower()
            if last_letter not in self._dead_end_letters:
                return last_letter
        return False

    def get(self, city: str):
        if self._cities is None:
            return None

        letter = self.last_letter(city)
        if letter not in self._cities.keys():
            return None
        result_city = random.choice(self._cities[letter])
        self.delete(result_city)
        self._last_letter = self.last_letter(result_city)
        return result_city

    def delete(self, city: str):
        city_key = city[0].lower()
        if city_key not in self._cities.keys():
            return False
        city = city.capitalize()
        self._used.append(city)
        self._cities[city_key].remove(city)
        if len(self._cities[city_key]) == 0:
            del self._cities[city_key]
        return True

    def read_cities(self, filename=None):
        self._cities = dict()
        if filename is None:
            filename = self._filename
        if not isfile(filename):
            return False
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.readlines()
        data = [x.strip() for x in data]
        for item in data:
            city_key = item[0].lower()
            if city_key not in self._cities.keys():
                self._cities.setdefault(city_key, list())
            self._cities[city_key].append(item.capitalize())
        self.__letter = None
