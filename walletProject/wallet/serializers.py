from rest_framework import serializers
from models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserRipio
        fields = ('url', 'username', 'email')


class CoinTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CoinType
        fields = '__all__'


class CoinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coin
        fields = ('type', 'cant')


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
