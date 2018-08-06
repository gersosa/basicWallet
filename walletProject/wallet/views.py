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
        user = User.objects.get(pk=request.data['id'])
        wallets_of = Wallet.objects.filter(user=user)

        if wallets_of:
            serializer = self.get_serializer(wallets_of, many=True)
            return Response(serializer.data)

        return Response(
            {'detail': 'The user has not wallet a of this coin'},
            status=400)


    @list_route()
    def havent_user(self, request):
        user_coins = Wallet.objects.exclude(user=request.user)

        if user_coins:
            serializer = self.get_serializer(user_coins, many=True)
            return Response(serializer.data)

        return Response([])

    @list_route()
    def calculator(self, request):
        coin = Coin.objects.get(name=request.GET['coin'])
        user = User.objects.get(username=request.GET['user'])
        wallet_coins = Wallet.objects.filter(user=user, coin=coin)
        ctx = {}
        ctx['balance'] = 0
        for w in wallet_coins:
            ctx['balance'] = ctx['balance'] + w.cant
        return Response(ctx)


class ClientView(generic.View):
    template_name = "wallet/index.html"

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request, self.template_name, ctx)
