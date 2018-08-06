from rest_framework import serializers
from django.contrib.auth.models import User
from models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'email')


class CoinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coin
        fields = ('id', 'name')


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    user = UserSerializer(required=False)
    coin = CoinSerializer(required=False)

    def create(self, validated_data):
        print validated_data, 'acaaaa'
        print validated_data['cant'], validated_data['user']['username'], validated_dat.user, 'estoooooooooooooooooooooooooooooooooo'
        user = User.objects.get(username=validated_data['user']['username'])
        amount = validated_data['cant']
        coin = Coin.objects.get(name=validated_data['coin']['name'])

        return Wallet.objects.create(coin=coin, user=user, cant=amount)

    class Meta:
        model = Wallet
        fields = '__all__'


class OperationSerializer(serializers.ModelSerializer):
    from_wallet = WalletSerializer(many=False)
    to_wallet = WalletSerializer(many=False)

    def create(self, validated_data):
        from_wallet = Wallet.objects.get(
            pk=validated_data['from_wallet']['id'])
        to_wallet = Wallet.objects.get(pk=validated_data['to_wallet']['id'])
        amount = validated_data['amount']
        operation = Operation(
            to_wallet=to_wallet,
            from_wallet=from_wallet,
            mount=amount
        )
        search_error = operation.save()
        try:
            search_error = search_error.get('error', None)
        except:
            return operation
        else:
            if search_error:
                raise serializers.ValidationError({'detail': search_error})

    class Meta:
        model = Operation
        fields = '__all__'
