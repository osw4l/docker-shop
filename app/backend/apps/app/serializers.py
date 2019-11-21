import logging
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .tasks import revertir_venta
from .utils import get_object_or_none
from .models import Tienda, UsuarioTienda, Producto, Venta, ProductoVenta
from .constants import UNIDADES_INSUFICIENTES, PRODUCTOS_AJENOS, PRODUCTOS_INEXISTENTE
logger = logging.getLogger('django')


class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = '__all__'


class UsuarioTiendaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsuarioTienda
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'tienda',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        data = self.context['request'].data
        if hasattr(user, 'usuariotienda'):
            validated_data['password'] = make_password(data['password'])
            validated_data['tienda'] = user.usuariotienda.tienda
            return super().create(validated_data)
        raise serializers.ValidationError({'error': 'Invalid role.'})


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    def create(self, validated_data):
        validated_data['tienda'] = self.context['request'].user.usuariotienda.tienda
        return super().create(validated_data)


class ProductoVentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True, many=False)
    valor_total = serializers.ReadOnlyField(source='total')

    class Meta:
        model = ProductoVenta
        fields = '__all__'


class VentaSerializer(serializers.ModelSerializer):
    productos = ProductoVentaSerializer(many=True, read_only=True)
    user = UsuarioTiendaSerializer(many=False, read_only=True)
    valor_total = serializers.ReadOnlyField(source='total')

    class Meta:
        model = Venta
        fields = '__all__'

    def create(self, validated_data):
        tienda = self.context['request'].user.usuariotienda.tienda
        validated_data['tienda'] = tienda
        validated_data['user'] = self.context['request'].user
        venta = super().create(validated_data)
        data = self.context['request'].data.copy()
        productos = data['productos']

        for producto in productos:
            p = get_object_or_none(Producto, id=producto['id'])
            if p:
                if p.tienda == tienda:
                    if producto['cantidad'] <= p.cantidad:
                        ProductoVenta.objects.create(
                            tienda=tienda,
                            venta=venta,
                            producto=p,
                            valor_unidad=p.precio,
                            cantidad=producto['cantidad']
                        )
                        p.descontar(cantidad=producto['cantidad'])
                    else:
                        self.cancelar_venta(venta_id=venta.id, message=UNIDADES_INSUFICIENTES)
                else:
                    self.cancelar_venta(venta_id=venta.id, message=PRODUCTOS_AJENOS)
            else:
                self.cancelar_venta(venta_id=venta.id, message=PRODUCTOS_INEXISTENTE)
        return venta

    @staticmethod
    def cancelar_venta(venta_id, message):
        revertir_venta.delay(venta_id=venta_id)
        raise serializers.ValidationError({'error': message})
