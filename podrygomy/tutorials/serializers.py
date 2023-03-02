import datetime

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import *
import logging

_logger = logging.getLogger(__name__)


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
        _logger.debug("Start creating Street object")

        # Извлекаем полученные данные для города
        city_data = validated_data.pop('city_id')
        _logger.debug("City data: %s", city_data)

        # Ищем в базе по названию
        city = City.objects.filter(name=city_data.get("name"))

        # Если в базе такого объекта нет - создаем
        if not city:
            _logger.debug("City by name %s not found in data base. Start creating", city_data.get("name"))
            City.objects.get_or_create(**city_data)

        # Получаем объект из базы
        city = get_object_or_404(City, name=city_data.get("name"))
        _logger.debug("Object data City from table: %s", city)

        street = Street.objects.create(city_id=city, **validated_data)
        return street


class ShopsSerializer(serializers.ModelSerializer):
    # Здесь описываем как читать поля из extra_kwargs (их типы данных и источник)
    street_id = serializers.CharField(source='street_id.name')
    # Добавляем вывод названия города в Json, в source указывам откуда брать значение.
    # Флаг read_only=True, т.к. при записи используется другое поле и при записи ругается на источник (source)
    city_name = serializers.CharField(source='street_id.city_id.name', read_only=True)
    # Указываем поля только для записи (при получении json объекта они отображаться не должны)
    city = serializers.CharField(write_only=True)
    open_time = serializers.TimeField(write_only=True)
    close_time = serializers.TimeField(write_only=True)

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
        _logger.debug("Start creating Shop object")

        # Извлекаем полученные данные для города
        city_data = validated_data.pop('city')
        _logger.debug("City data: %s", city_data)
        city_data = dict.fromkeys({'name'}, city_data)
        _logger.debug("Added to dict: %s", city_data)

        # Ищем в базе по названию
        city = City.objects.filter(name=city_data.get("name"))

        # Если в базе такого объекта нет - создаем
        if not city:
            _logger.debug("City by name %s not found in data base. Start creating", city_data.get("name"))
            City.objects.get_or_create(**city_data)

        # Получаем объект из базы
        city = get_object_or_404(City, name=city_data.get("name"))
        _logger.debug("Object data City from table: %s", city)

        # Извлекаем полученные данные для улицы
        street_data = validated_data.pop('street_id')
        _logger.debug("Street data: %s", street_data)

        # Ищем в базе по названию и идентификатору города
        street = Street.objects.filter(name=street_data.get("name"), city_id=city.id)
        _logger.debug("Object data Street from table: %s", street)

        # Если в базе такого объекта нет - создаем
        if not street:
            _logger.debug("Street by name %s and city_id %s not found in data base. Start creating. "
                          + "\nStreet data before add city_id: %s",
                          street_data.get("name"), str(city.id), street_data)
            street_data['city_id'] = city
            Street.objects.get_or_create(**street_data)

        # Получаем объект из базы
        street = get_object_or_404(Street, name=street_data.get("name"), city_id=city.id)

        shop = Shops.objects.create(street_id=street, **validated_data)
        return shop

    # # Метод определят значение для флага open
    @staticmethod
    def set_open(obj):
        open_time = obj.open_time
        close_time = obj.close_time
        now = datetime.datetime.now().time()
        if open_time < now < close_time:
            return 1
        else:
            return 0
