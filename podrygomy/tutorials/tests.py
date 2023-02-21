from unittest import mock

from django.test import TestCase

from .models import *
from .views import *


# Created by https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing


class CityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        City.objects.create(name='Ulanovsk')
        City.objects.create(name='Samara')

    def test_name_label(self):
        city = City.objects.get(name='Ulanovsk')
        field_label = city._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        city = City.objects.get(name='Ulanovsk')
        max_length = city._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_object_name_first(self):
        city = City.objects.get(name='Ulanovsk')
        expected_object_name = f'{city.name}'
        self.assertEqual(str(city.name), expected_object_name)

    def test_object_name_second(self):
        city = City.objects.get(name='Samara')
        expected_object_name = f'{city.name}'
        self.assertEqual(str(city.name), expected_object_name)

    def test_get_all_cities(self):
        cities = City.objects.all()
        self.assertEqual(len(cities), 2)


class CityViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_cities = 10

        for city_id in range(number_of_cities):
            City.objects.create(
                name=f'City {city_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/city')
        self.assertEqual(response.status_code, 200)

    def test_lists_all_cities(self):
        response = self.client.get('/api/city')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 10)

    def test_create_new_city(self):
        response = self.client.post('/api/city', {'name': 'New City'})
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/city')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 11)


class StreetModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        City.objects.create(name='Ulanovsk')
        city = City.objects.get(name='Ulanovsk')
        Street.objects.create(name='Street 1', city_id=city)
        Street.objects.create(name='Street 2', city_id=city)

    def test_name_label(self):
        street = Street.objects.get(name='Street 1')
        field_label_name = street._meta.get_field('name').verbose_name
        field_label_city = street._meta.get_field('city_id').verbose_name
        self.assertEqual(field_label_name, 'name')
        self.assertEqual(field_label_city, 'city id')

    def test_name_max_length(self):
        street = Street.objects.get(name='Street 1')
        max_length = street._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_object_name_first(self):
        street = Street.objects.get(name='Street 1')
        expected_object_name = f'{street.name}'
        self.assertEqual(str(street.name), expected_object_name)

    def test_object_name_second(self):
        street = Street.objects.get(name='Street 2')
        expected_object_name = f'{street.name}'
        self.assertEqual(str(street.name), expected_object_name)

    def test_get_all_streets(self):
        streets = Street.objects.all()
        self.assertEqual(len(streets), 2)


class StreetViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        City.objects.create(name='Ulanovsk')
        city = City.objects.get(name='Ulanovsk')
        Street.objects.create(name='Street 1', city_id=city)
        Street.objects.create(name='Street 2', city_id=city)
        City.objects.create(name='Samara')
        city = City.objects.get(name='Samara')
        Street.objects.create(name='Street 1', city_id=city)
        Street.objects.create(name='Street 2', city_id=city)

    def test_view_url_expect_error(self):
        response = self.client.get('/api/street')
        self.assertEqual(response.status_code, 400)

    def test_view_url_get_streets_by_city_id_first(self):
        city = City.objects.get(name='Ulanovsk')
        response = self.client.get('/api/street?city_id=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_view_url_get_streets_by_city_id_second(self):
        city = City.objects.get(name='Samara')
        response = self.client.get('/api/street?city_id=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_view_url_get_streets_by_not_exist_city_id(self):
        response = self.client.get('/api/street?city_id=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_create_new_street_with_exist_city(self):
        response = self.client.post('/api/street', {'name': 'New Street', 'city_id': 'Samara'})
        self.assertEqual(response.status_code, 201)
        city = City.objects.get(name='Samara')
        response = self.client.get('/api/street?city_id=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        city = City.objects.all()
        self.assertEqual(len(city), 2)

    def test_create_new_street_with_not_exist_city(self):
        response = self.client.post('/api/street', {'name': 'New Street', 'city_id': 'New City'})
        self.assertEqual(response.status_code, 201)
        city = City.objects.get(name='New City')
        response = self.client.get('/api/street?city_id=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        city = City.objects.all()
        self.assertEqual(len(city), 3)


class ShopsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        City.objects.create(name='Ulanovsk')
        city = City.objects.get(name='Ulanovsk')
        Street.objects.create(name='Street 1', city_id=city)
        Street.objects.create(name='Street 2', city_id=city)
        street = Street.objects.get(name='Street 1')
        Shops.objects.create(name='Shop 1', street_id=street, house="1A", open_time=8, close_time=22)
        Shops.objects.create(name='Shop 2', street_id=street, house="58", open_time=8, close_time=22)
        street = Street.objects.get(name='Street 2')
        Shops.objects.create(name='Shop 3', street_id=street, house="17", open_time=0, close_time=13)
        City.objects.create(name='Samara')
        city = City.objects.get(name='Samara')
        Street.objects.create(name='Street 3', city_id=city)
        Street.objects.create(name='Street 4', city_id=city)
        street = Street.objects.get(name='Street 3')
        Shops.objects.create(name='Shop 4', street_id=street, house="5", open_time=9, close_time=23)
        Shops.objects.create(name='Shop 5', street_id=street, house="63", open_time=7, close_time=20)
        street = Street.objects.get(name='Street 4')
        Shops.objects.create(name='Shop 6', street_id=street, house="21", open_time=0, close_time=24)

    def test_name_label(self):
        shop = Shops.objects.get(name='Shop 1')
        field_label_name = shop._meta.get_field('name').verbose_name
        field_label_street_id = shop._meta.get_field('street_id').verbose_name
        field_label_house = shop._meta.get_field('house').verbose_name
        field_label_open_time = shop._meta.get_field('open_time').verbose_name
        field_label_close_time = shop._meta.get_field('close_time').verbose_name
        self.assertEqual(field_label_name, 'name')
        self.assertEqual(field_label_street_id, 'street id')
        self.assertEqual(field_label_house, 'house')
        self.assertEqual(field_label_open_time, 'open time')
        self.assertEqual(field_label_close_time, 'close time')

    def test_name_max_length(self):
        shop = Shops.objects.get(name='Shop 1')
        max_length_name = shop._meta.get_field('name').max_length
        max_length_house = shop._meta.get_field('house').max_length
        self.assertEqual(max_length_name, 10)
        self.assertEqual(max_length_house, 10)

    def test_object_name_first(self):
        shop = Shops.objects.get(name='Shop 1')
        expected_object_name = f'{shop.name}'
        expected_object_house = f'{shop.house}'
        self.assertEqual(str(shop.name), expected_object_name)
        self.assertEqual(str(shop.house), expected_object_house)

    def test_get_all_shops(self):
        shops = Shops.objects.all()
        self.assertEqual(len(shops), 6)



class ShopsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        City.objects.create(name='Ulanovsk')
        city = City.objects.get(name='Ulanovsk')
        Street.objects.create(name='Street 1', city_id=city)
        Street.objects.create(name='Street 2', city_id=city)
        street = Street.objects.get(name='Street 1')
        Shops.objects.create(name='Shop 1', street_id=street, house="1A", open_time=8, close_time=22)
        Shops.objects.create(name='Shop 2', street_id=street, house="58", open_time=8, close_time=22)
        street = Street.objects.get(name='Street 2')
        Shops.objects.create(name='Shop 3', street_id=street, house="17", open_time=0, close_time=13)
        City.objects.create(name='Samara')
        city = City.objects.get(name='Samara')
        Street.objects.create(name='Street 3', city_id=city)
        Street.objects.create(name='Street 4', city_id=city)
        street = Street.objects.get(name='Street 3')
        Shops.objects.create(name='Shop 4', street_id=street, house="5", open_time=9, close_time=23)
        Shops.objects.create(name='Shop 5', street_id=street, house="63", open_time=7, close_time=20)
        street = Street.objects.get(name='Street 4')
        Shops.objects.create(name='Shop 6', street_id=street, house="21", open_time=0, close_time=24)

    def test_view_url_expect_error(self):
        response = self.client.get('/api/shop')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)

    def test_view_url_get_shops_by_city_id(self):
        city = City.objects.get(name='Ulanovsk')
        response = self.client.get('/api/shop?city=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_view_url_get_shops_by_street_id(self):
        street = Street.objects.get(name='Street 1')
        response = self.client.get('/api/shop?street=' + str(street.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    # https://stackoverflow.com/questions/44744061/django-test-mock-datetime-now
    @mock.patch('datetime.datetime')
    def test_view_url_get_shops_by_open_1_with_now_9_h(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime.time(9, 0, 0)

        response = self.client.get('/api/shop?open=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)

    @mock.patch('datetime.datetime')
    def test_view_url_get_shops_by_open_1_with_now_7_h(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime.time(7, 0, 0)

        response = self.client.get('/api/shop?open=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    @mock.patch('datetime.datetime')
    def test_view_url_get_shops_by_open_1_with_now_5_h(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime.time(5, 0, 0)

        response = self.client.get('/api/shop?open=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    @mock.patch('datetime.datetime')
    def test_view_url_get_shops_by_open_1_with_now_23_h(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime.time(23, 0, 0)

        response = self.client.get('/api/shop?open=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    @mock.patch('datetime.datetime')
    def test_view_url_get_shops_by_open_0_with_now_8_h(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime.time(8, 0, 0)

        response = self.client.get('/api/shop?open=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    @mock.patch('datetime.datetime')
    def test_view_url_get_shops_by_open_0_with_now_5_h(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime.time(5, 0, 0)

        response = self.client.get('/api/shop?open=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    @mock.patch('datetime.datetime')
    def test_view_url_get_shops_by_open_0_with_now_22_h(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime.time(22, 0, 0)

        response = self.client.get('/api/shop?open=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    @mock.patch('datetime.datetime')
    def test_view_url_get_shops_by_open_1_and_city_id_with_now_7_h(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime.time(7, 0, 0)

        city = City.objects.get(name='Ulanovsk')
        response = self.client.get('/api/shop?open=1&city=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    @mock.patch('datetime.datetime')
    def test_view_url_get_shops_by_open_0_and_city_id_with_now_7_h(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime.time(7, 0, 0)

        city = City.objects.get(name='Ulanovsk')
        response = self.client.get('/api/shop?open=0&city=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_create_new_street_with_exist_city_and_Street(self):
        response = self.client.post('/api/shop', {'name': 'New Shop', 'street_id': 'Street 4', 'city': 'Samara',
                                                  'house': '5B', 'open_time': '8', 'close_time': '22'})
        self.assertEqual(response.status_code, 201)
        city = City.objects.get(name='Samara')
        response = self.client.get('/api/shop?city=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
        city = City.objects.all()
        self.assertEqual(len(city), 2)
        street = Street.objects.all()
        self.assertEqual(len(street), 4)

    def test_create_new_street_with_exist_city_and_not_exist_Street(self):
        response = self.client.post('/api/shop', {'name': 'New Shop', 'street_id': 'New Street', 'city': 'Samara',
                                                  'house': '5B', 'open_time': '8', 'close_time': '22'})
        self.assertEqual(response.status_code, 201)
        city = City.objects.get(name='Samara')
        response = self.client.get('/api/shop?city=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
        city = City.objects.all()
        self.assertEqual(len(city), 2)
        street = Street.objects.all()
        self.assertEqual(len(street), 5)

    def test_create_new_street_with_not_exist_city_and_Street(self):
        response = self.client.post('/api/shop', {'name': 'New Shop', 'street_id': 'New Street', 'city': 'New City',
                                                  'house': '5B', 'open_time': '8', 'close_time': '22'})
        self.assertEqual(response.status_code, 201)
        city = City.objects.get(name='New City')
        response = self.client.get('/api/shop?city=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        city = City.objects.all()
        self.assertEqual(len(city), 3)
        street = Street.objects.all()
        self.assertEqual(len(street), 5)
