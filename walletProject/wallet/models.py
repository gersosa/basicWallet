# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.db import models
from django.conf import settings


# Create your models here.


class Coin(models.Model):
    name = models.CharField(_('Nombre'), max_length=255)

    def __str__(self):
        return self.name


class Wallet(models.Model):
    coin = models.ForeignKey(Coin, verbose_name=_('Moneda'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Propietario'))
    cant = models.FloatField(_('Cantidad actual'), default=0)


    def __str__(self):
        return str(self.cant) + '->' + self.user.username

    def same_coin(self, wallet):
        return wallet.coin == self.coin

    def can_send(self, amount):
        return (self.cant - amount) >= 0

    def add(self, amount):
        self.cant += amount
        return self.save()

    def remove(self, amount):
        self.cant -= amount
        return self.save()


class Operation(models.Model):
    mount = models.FloatField(_('Monto de la operación'))
    created = models.DateTimeField(_('Creada'), auto_now_add=True)
    from_wallet = models.ForeignKey(Wallet, verbose_name=_('Billetera origen'), related_name='operation_origin')
    to_wallet = models.ForeignKey(Wallet, verbose_name=_('Billetera destino'))

    def __str__(self):
        return self.from_wallet.user.username + '->' + self.to_wallet.user.username

    def save(self, *args, **kwargs):
        same_coin = self.from_wallet.same_coin(self.to_wallet)
        has_money = self.from_wallet.can_send(self.mount)
        print 'llegaaaaaaaaaaaa 1'

        if not same_coin:
            return {'error': 'Wallets must have the same coin'}
        elif not has_money:
            return {
                'error': 'Owner wallet must have enought money'
            }
        elif self.mount <= 0:
            return {
                'error': 'Amount must be positive',
            }
        else:
            self.from_wallet.remove(self.mount)
            self.to_wallet.add(self.mount)
            print 'llegaaaaaaaaaaaa 5'
            return super(Operation, self).save(*args, **kwargs)
