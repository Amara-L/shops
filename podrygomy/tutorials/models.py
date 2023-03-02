from django.db import models


class City(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30, blank=False, unique=True, null=False)


class Street(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30, blank=False, null=False)
    city_id = models.ForeignKey(City, on_delete=models.RESTRICT, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'city_id'], name='uniqueStreetByCity')
        ]


class Shops(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=10, blank=False, null=False)
    street_id = models.ForeignKey(Street, on_delete=models.RESTRICT, blank=False, null=False, default='0')
    house = models.CharField(max_length=10, default='0')
    open_time = models.TimeField(blank=False, null=False)
    close_time = models.TimeField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'street_id', 'house'], name='uniqueShopByAddress')
        ]
