import random
from os.path import isfile


class CitiesGame():
    __cities = dict()
    __filename = None
    __letter = None

    def __init__(self, filename):
        self.__filename = filename
        self.read_cities()

    def get_letter(self):
        return self.__letter

    def get(self, first_letter: str):
        if self.__cities is None:
            return None

        if len(first_letter) != 1 and first_letter not in self.__cities.keys():
            return False

        self.__letter = first_letter
        print('first_letter=' + str(first_letter))
        print('data_keys=' + str(self.__cities.keys()))
        city = random.choice(self.__cities[first_letter])
        self.delete(city)
        return city

    def delete(self, city: str):
        city_key = city[0].lower()
        if city_key not in self.__cities.keys():
            return False
        self.__cities[city_key].remove(city)
        if len(self.__cities[city_key]) == 0:
            del self.__cities.pop[city_key]
        return True

    def read_cities(self, filename=None):
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
            self.__cities[city_key].append(item)
        self.__letter = None
        print(str(self.__cities))
