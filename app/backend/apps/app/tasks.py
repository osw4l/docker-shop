import logging, os, requests, time
from datetime import datetime
from celery import shared_task
from .models import Venta, Producto
from .utils import get_object_or_none as exist

logger = logging.getLogger('django')


@shared_task
def revertir_venta(venta_id):
    venta = exist(Venta, id=venta_id)
    time.sleep(10)
    if venta:
        for producto_venta in venta.get_productos():
            producto_venta.agregar(cantidad=producto_venta['cantidad'])
        venta.delete()

