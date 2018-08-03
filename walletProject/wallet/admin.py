# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from models import *

# Register your models here.


class CoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'mount', 'created', 'from_wallet', 'to_wallet')


class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'coin', 'cant')


admin.site.register(Coin, CoinAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Wallet, WalletAdmin)
