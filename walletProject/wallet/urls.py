from django.conf.urls import url, include
from rest_framework import routers
from wallet import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'cion-types', views.CoinTypeViewSet)
router.register(r'coins', views.CoinViewSet)
router.register(r'wallets', views.WalletViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
