from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from backend.apps.app.views import TiendaViewSet, UsuarioTiendaViewSet, ProductoViewSet, VentaViewSet

router = DefaultRouter()
router.register(r'tiendas', TiendaViewSet)
router.register(r'usuarios', UsuarioTiendaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'ventas', VentaViewSet)

schema_view = get_swagger_view(title='Wogo Shop Api')

PREFIX_URL = settings.PREFIX_URL
urlpatterns = [
      url(r'^{}admin/'.format(PREFIX_URL), admin.site.urls),
      url(r'^{}auth/'.format(PREFIX_URL), include('rest_auth.urls')),
      url(r'^{}$'.format(PREFIX_URL), schema_view),
      url(r'^{}api/'.format(PREFIX_URL), include(router.urls))
]

