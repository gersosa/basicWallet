# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class ConiType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')

    def __str__(self):
        return self.name


class Coin(models.Model):
    type = models.OneToOneField(ConiType, on_delete=models.CASCADE, verbose_name='Tipo')
    cant = models.FloatField(verbose_name='Cantidad')

    def __str__(self):
        return u'%s%s%s' % (self.type, '->', self.cant)


class Operation(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creada')

    def __str__(self):
        return str(self.created)


class Wallet(models.Model):
    coins = models.ManyToManyField(Coin, verbose_name='Monedas', null=True)
    operations = models.ManyToManyField(Operation, verbose_name='Transacciones', null=True)

    def get_coins(self):
        return "\n".join([c.__str__() for c in self.coins.all()])

    def get_operations(self):
        return "\n".join([c.__str__() for c in self.operations.all()])


class UserRipio(User):
    wallet = models.OneToOneField(Wallet, verbose_name='Billetera')
