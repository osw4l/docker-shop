import logging
from django.db import models, transaction
from django.contrib.auth.models import User

logger = logging.getLogger('debug')


# Create your models here.

class BaseNombre(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre


class Tienda(BaseNombre):
    class Meta:
        verbose_name = 'Tienda'
        verbose_name_plural = 'Tiendas'


class UsuarioTienda(User):
    tienda = models.ForeignKey(
        Tienda,
        on_delete=models.CASCADE,
        blank=True
    )

    class Meta:
        verbose_name = 'Usuario Tienda'
        verbose_name_plural = 'Usuarios Tiendas'


class Producto(BaseNombre):
    tienda = models.ForeignKey(
        Tienda,
        on_delete=models.CASCADE,
        blank=True
    )
    cantidad = models.PositiveIntegerField(default=0)
    descripcion = models.TextField(
        blank=True,
        null=True
    )
    precio = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    @transaction.atomic
    def descontar(self, cantidad=None):
        self.cantidad -= cantidad
        self.save(update_fields=['cantidad'])

    @transaction.atomic
    def agregar(self, cantidad=None):
        self.cantidad += cantidad
        self.save(update_fields=['cantidad'])


class Venta(models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        blank=True
    )
    fecha = models.DateField(auto_now_add=True)
    tienda = models.ForeignKey(
        Tienda,
        on_delete=models.CASCADE,
        blank=True
    )

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def total(self):
        return sum([
            v.total() for v in self.get_productos()
        ])

    def get_productos(self):
        return ProductoVenta.objects.filter(venta=self)


class ProductoVenta(models.Model):
    tienda = models.ForeignKey(
        Tienda,
        on_delete=models.CASCADE
    )
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='productos'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )
    valor_unidad = models.PositiveIntegerField(default=0)
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Producto Venta'
        verbose_name_plural = 'Productos Ventas'

    def total(self):
        return self.valor_unidad * self.cantidad

