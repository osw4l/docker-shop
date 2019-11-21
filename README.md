# Prueba tecnica backend developer

el codigo del backend de encuentra dentro de la carpeta **app**

requisitos tecnicos para poder correr el backend
- tener docker instalado en la maquina donde se va a ejecutar el proyecto
- configurar las variables de entorno
- ejecutar los comandos de migracion y creacion de super usuario en orden

### Configurar el entorno por primera vez
en la raiz del proyecto existe un archivo llamado** env.template** 
este archivo contiene nuestras variables de entorno con valores por defectos
usted puede cambiarlos por los valores que quiera

**nota: no recomiendo cambiar el host de postgres si vamos a ejecutar nuestro ambiente de manera local**

#### contenido del env.template
```bash
LANG=C.UTF-8
LC_ALL=C.UTF-8
PROJECT_NAME=backend
SECRET_KEY=SECRET
POSTGRES_DB=oswal
POSTGRES_USER=oswal
POSTGRES_PASSWORD=test
POSTGRES_HOST=postgres
```

para que el backend pueda funcionar debe usted hacer una copia del archivo con el siguiente comando:

`cp env.template .env`

una vez copiado se puede iniciar con la construccion de la imagen de docker y posteriormente la puesta en marcha de esta misma, para hacerlo puede utilizar el siguiente comando:

`docker-compose up -d --build`

despues de ejecutar ese comando nos saldra algo similar a esto:

    Starting docker-shop-api_redis_1    ... done
    Starting docker-shop-api_postgres_1 ... done
    Starting docker-shop-api_app_1      ... done
    Starting docker-shop-api_worker_1   ... done
    Starting docker-shop-api_beat_1     ... done
    Starting docker-shop-api_websockets_worker_1 ... done
    Starting docker-shop-api_nginx_1             ... done
    Starting docker-shop-api_daphne_1            ... done

si todo sale done podremos ir al [http://0.0.0.0:3002/](http://0.0.0.0:3002/ "http://0.0.0.0:3002/") donde vive nuestra app y podremos ver la documentación de la api.

lo siguiente que debemos hacer es seguir estos comandos para aplicar las migraciones y crear un usuario en nuestro administrador:
- `docker-compose exec app python manage.py makemigrations`
- `docker-compose exec app python manage.py migrate`

para crear un super usuario en nuestro administrador debemos ejecutar el siguiente comando:
`docker-compose exec app python manage.py createsuperuser`

para poder hacer uso de nuestro backend debemos crear las tiendas en el admin y usuarios de las tiendas, luego debemos logearnos en nuestra aplicación de angular y podemos ver funcionando la aplicación conectada al backend.

si queremos detener nuestra imagen podemos hacerlo con este comando:

`docker-compose stop`

si queremos volver a levantar nuestra nuevamente:
`docker-compose up -d`