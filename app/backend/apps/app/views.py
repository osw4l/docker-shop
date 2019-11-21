import logging
from rest_framework import viewsets, serializers
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_202_ACCEPTED
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .utils import get_object_or_none, BigPagination
from .permissions import IsTiendaUser
from .serializers import TiendaSerializer, UsuarioTiendaSerializer, VentaSerializer, ProductoSerializer
from .models import Tienda, UsuarioTienda, Producto, Venta
from rest_framework import filters
from .constants import PRODUCTO_INEXISTENTE, PRODUCTO_AJENO
logger = logging.getLogger('django')


class TiendaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
    permission_classes = [AllowAny]


class FilterTiendaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated & IsTiendaUser]
    pagination_class = BigPagination
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self.request.user, 'usuariotienda'):
            qs = qs.filter(tienda=self.request.user.usuariotienda.tienda)
        return qs

    def destroy(self, request, *args, **kwargs):
        return Response({'error': "you can't delete anything"}, status=HTTP_403_FORBIDDEN)

    def handle_error(self, message):
        raise serializers.ValidationError({'error': message})


class UsuarioTiendaViewSet(FilterTiendaViewSet):
    queryset = UsuarioTienda.objects.all()
    serializer_class = UsuarioTiendaSerializer
    search_fields = ('$first_name', '$email', '$last_name', '$username')


class ProductoViewSet(FilterTiendaViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    search_fields = ('$nombre', '$id')

    @action(detail=True, methods=['PUT'])
    def actualizar_cantidad(self, request, pk=None):
        tienda = self.request.user.usuariotienda.tienda
        producto = get_object_or_none(Producto, id=pk)
        if producto:
            if tienda == producto.tienda:
                cantidad = request.data['cantidad']
                producto.agregar(cantidad=cantidad)
            else:
                super().handle_error(message=PRODUCTO_AJENO)
        else:
            super().handle_error(message=PRODUCTO_INEXISTENTE)
        return Response({'success': True}, status=HTTP_202_ACCEPTED)


class VentaViewSet(FilterTiendaViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    search_fields = ('$id', '$user__first_name', '$user__last_name', '$user__username')

