from django.contrib import admin
from .forms import UsuarioTiendaForm
from . import models

# Register your models here.
admin.site.site_header = 'Wogo Shop'
admin.site.site_title = 'Wogo Shop'
admin.site.index_title = 'Wogo Shop'


@admin.register(models.Tienda)
class TiendaAdmin(admin.ModelAdmin):
    list_display = [
        'nombre'
    ]
    search_fields = [
        'nombre'
    ]


@admin.register(models.UsuarioTienda)
class UsuarioTiendaAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'get_full_name',
        'tienda'
    ]
    search_fields = [
        'tienda',
        'first_name',
        'last_name',
        'username'
    ]
    form = UsuarioTiendaForm


@admin.register(models.Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nombre',
        'tienda',
        'cantidad',
        'descripcion',
        'precio'
    ]
    search_fields = [
        'nombre',
        'tienda__nombre'
    ]


@admin.register(models.Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'tienda',
        'user',
        'fecha',
        'total'
    ]
    search_fields = [
        'tienda__nombre'
    ]


@admin.register(models.ProductoVenta)
class ProductoVentaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'producto',
        'tienda',
        'cantidad',
        'valor_unidad',
        'total'
    ]


