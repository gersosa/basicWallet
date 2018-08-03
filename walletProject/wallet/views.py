# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django_filters import rest_framework
from django.views import generic
from django.shortcuts import render
from rest_framework.decorators import detail_route, list_route
from serializers import *
from models import *



class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class CoinViewSet(viewsets.ModelViewSet):

    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @list_route()
    def havent_user(self, request):
        user_coins = Wallet.objects.filter(user=request.user).values_list('coin', flat=True)
        coins = Coin.objects.exclude(pk__in=user_coins)

        if coins:
            serializer = self.get_serializer(coins, many=True)
            return Response(serializer.data)

        return Response([])


class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = (permissions.IsAuthenticated,)



class WalletViewSet(viewsets.ModelViewSet):

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filter_fields = ('user__username',)

    def get_queryset(self):
        user = self.request.user
        return Wallet.objects.filter(user=user)

    @detail_route(methods=['post'])
    def get_wallet_of_user(self, request, pk=None):
        user = User.objects.get(pk=pk)
        wallets_of = Wallet.objects.filter(
            user=user).filter(coin=request.data['id'])

        if wallets_of:
            serializer = self.get_serializer(wallets_of, many=True)
            return Response(serializer.data)

        return Response(
            {'detail': 'The user has not wallet a of this coin'},
            status=400)


class ClientView(generic.View):
    template_name = "wallet/index.html"

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request, self.template_name, ctx)
