# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.


class CoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'cant')


class CoinTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created')


class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_coins', 'get_operations')




class UserRipioAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'wallet')


admin.site.register(Coin, CoinAdmin)
admin.site.register(CoinType, CoinTypeAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(UserRipio, UserRipioAdmin)
