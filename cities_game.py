import random
from os.path import isfile


class CitiesGame():
    __cities = dict()
    __filename = None
    __letter = None
    __used = list()

    def __init__(self, filename):
        self.__filename = filename
        self.read_cities()

    def get_letter(self):
        return self.__letter


    def has_city(self, city: str):
        if not isinstance(city, str) or len(city) < 1:
            return False
        first_letter = city.strip()[0].lower()
        if (first_letter in self.__cities.keys()) and (
                city.capitalize() in self.__cities[first_letter]):
                return True
        else:
            return False

    def is_used(self, city):
        if city.capitalize() in self.__used:
            return True
        else:
            return False

    def get(self, letter: str):
        #  @ToDo: бывают буквы, на которые не могут начинаться слова
        if self.__cities is None:
            return None

        letter = letter[0].lower()
        if letter not in self.__cities.keys():
            return None
        result_city = random.choice(self.__cities[letter])
        self.delete(result_city)
        self.__letter = result_city[-1]
        return result_city

    def delete(self, city: str):
        city_key = city[0].lower()
        if city_key not in self.__cities.keys():
            return False
        city = city.capitalize()
        self.__used.append(city)
        self.__cities[city_key].remove(city)
        if len(self.__cities[city_key]) == 0:
            del self.__cities[city_key]
        return True

    def read_cities(self, filename=None):
        self.__cities = dict()
        if filename is None:
            filename = self.__filename
        if not isfile(filename):
            return False
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.readlines()
        data = [x.strip() for x in data]
        for item in data:
            city_key = item[0].lower()
            if city_key not in self.__cities.keys():
                self.__cities.setdefault(city_key, list())
            self.__cities[city_key].append(item.capitalize())
        self.__letter = None
