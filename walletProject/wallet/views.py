# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from serializers import *
from models import *


class UserViewSet(viewsets.ModelViewSet):

    queryset = UserRipio.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = request.POST['email']
            name = request.POST['username']
            wallet = Wallet.objects.create()
            user = UserRipio.objects.create(
                username=name,
                email=email,
                wallet=wallet
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers={"Access-Control-Allow-Origin": "http://127.0.0.1:8000/users/"})
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST, headers={"Access-Control-Allow-Origin": "http://127.0.0.1:8000/users/"})


class CoinTypeViewSet(viewsets.ModelViewSet):

    queryset = CoinType.objects.all()
    serializer_class = CoinTypeSerializer


class CoinViewSet(viewsets.ModelViewSet):

    queryset = Coin.objects.all()
    serializer_class = CoinSerializer


class WalletViewSet(viewsets.ModelViewSet):

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
