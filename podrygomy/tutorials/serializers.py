import datetime

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import *


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id',
                  'name',)


class StreetSerializer(serializers.ModelSerializer):
    city_id = serializers.CharField(source='city_id.name')
    class Meta:
        model = Street
        fields = ('id',
                  'name',
                  'city_id',)

    def create(self, validated_data):
        print("Start creating Street object")

        # Извлекаем полученные данные для города
        print('City data:')
        city_data = validated_data.pop('city_id')
        print(city_data)

        # Ищем в базе по названию
        city = City.objects.filter(name=city_data.get("name"))

        # Если в базе такого объекта нет - создаем
        if not city:
            print("City by name " + city_data.get("name") + " not found in data base. Start creating")
            City.objects.get_or_create(**city_data)

        # Получаем объект из базы
        print('Object data City from table:')
        city = get_object_or_404(City, name=city_data.get("name"))
        print(city)

        print('Object Street:')
        street = Street.objects.create(city_id=city, **validated_data)
        print(street)
        return street


class ShopsSerializer(serializers.ModelSerializer):
    # Здесь описываем как читать поля из extra_kwargs (их типы данных и источник)
    street_id = serializers.CharField(source='street_id.name')
    # Добавляем вывод названия города в Json, в source указывам откуда брать значение.
    # Флаг read_only=True, т.к. при записи используется другое поле и при записи ругается на источник (source)
    city_name = serializers.CharField(source='street_id.city_id.name', read_only=True)
    # Указываем поля только для записи (при получении json объекта они отображаться не должны)
    city = serializers.CharField(write_only=True)
    open_time = serializers.IntegerField(write_only=True)
    close_time = serializers.IntegerField(write_only=True)

    # Флаг открытия/закрытия магазина
    # Значение определяется в методе set_open
    # Так же можно указать определение в модели:
    # https://stackoverflow.com/questions/24233988/django-serializer-method-field
    open = serializers.SerializerMethodField('set_open', read_only=True)

    class Meta:
        model = Shops
        fields = ('id',
                  'name',
                  'street_id',
                  'house',
                  'open_time',
                  'close_time',
                  'city',
                  'city_name',
                  'open',)
        # Здесь указываем изменения в поле street_id и дополнительное поле city
        extra_kwargs = {
            'street_id': {'write_only': True, 'source': 'street.name'},
            'city': {'write_only': True},
            'open': {'read_only': True},
        }

    def create(self, validated_data):
        print("Start creating Shop object")

        # Извлекаем полученные данные для города
        print('City data:')
        city_data = validated_data.pop('city')
        print(city_data)
        print('Add to dict:')
        city_data = dict.fromkeys({'name'}, city_data)
        print(city_data)

        # Ищем в базе по названию
        city = City.objects.filter(name=city_data.get("name"))

        # Если в базе такого объекта нет - создаем
        if not city:
            print("City by name " + city_data.get("name") + " not found in data base. Start creating")
            City.objects.get_or_create(**city_data)

        # Получаем объект из базы
        print('Object data City from table:')
        city = get_object_or_404(City, name=city_data.get("name"))
        print(city)

        # Извлекаем полученные данные для улицы
        print('Street data:')
        street_data = validated_data.pop('street_id')
        print(street_data)

        # Ищем в базе по названию и идентификатору города
        street = Street.objects.filter(name=street_data.get("name"), city_id=city.id)
        print('Object data Street from table:')
        print(street)

        # Если в базе такого объекта нет - создаем
        if not street:
            print("Street by name " + street_data.get("name") + " and city_id "
                  + str(city.id) + " not found in data base. Start creating. \nStreet data before add city_id:")
            print(street_data)
            street_data['city_id'] = city
            print("Street data after add city_id:")
            print(street_data)
            Street.objects.get_or_create(**street_data)

        # Получаем объект из базы
        print('Object data Street from table:')
        street = get_object_or_404(Street, name=street_data.get("name"), city_id=city.id)
        print(street)

        print('Object Shop:')
        shop = Shops.objects.create(street_id=street, **validated_data)
        print(shop)
        return shop

    # # Метод определят значение для флага open
    def set_open(self, obj):
        open_time = obj.open_time
        close_time = obj.close_time
        now = datetime.datetime.now().hour
        open = 0
        if int(open_time) <= now < int(close_time):
            open = 1
        else:
            open = 0
        return open
