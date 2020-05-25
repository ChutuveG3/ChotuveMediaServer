[![Build Status](https://www.travis-ci.org/ChutuveG3/ChotuveMediaServer.svg?branch=master)](https://www.travis-ci.org/ChutuveG3/ChotuveMediaServer)

# ChotuveMediaServer

## Levantar el servidor con Docker  
Dependencias: Docker.  

### Bulidear la imagen:  
` docker build -t chotuve-media-server .`
### Levantamos el contenedor
`docker run -d -p 5000:7654 -e PORT=7654 -e MONGO_URI=<mongo_uri> -e DB_NAME=<db_name> chotuve-media-server:latest `  

Podremos acceder desde `localhost:5000`.

### Correr tests
Correr el siguiente comando dentro de docker:  
`$ docker exec <app_name> nose2`

## Local dev

## Dependencias

Si queremos levantar el servidor de manera local, debemos instalar las dependencias:  
`$ pip install -r requirements.txt`

### Levantar servidor

Debemos ejecutar el siguiente comando:  
`$ gunicorn -b 0.0.0.0:5050 src.wsgi`

Podremos acceder desde `localhost:5050`

### Correr tests

`$ nose2`

## Logging

Los mensajes de logs se mostrarán por salida estándar, con el formato
`NIVEL <día/fecha> - <mensaje>`.

Más info: [logging-doc](https://docs.python.org/3/howto/logging.html)
