# ChotuveMediaServer

## Levantar el servidor con Docker  
Dependencias: Docker.  

### Bulidear la imagen:  
` docker build -t chotuve-media-server .`
### Levantamos el contenedor
`docker run -d -p 5000:7654 -e PORT=7654 -e MONGO_URI=<mongo_uri> -e DB_NAME=<db_name> chotuve-media-server:latest `  

Podremos acceder desde `localhost:5000`.

## Correr tests
Correr el siguiente comando:  
`$ node2`

## Logging

Los mensajes de logs se mostrarán por salida estándar, con el formato
`NIVEL <día/fecha> - <mensaje>`.

|Level | When it’s used |
| ----- | ---- |
| DEBUG | Detailed information, typically of interest only when diagnosing problems. |  | 
| INFO | Confirmation that things are working as expected. |
| WARNING | An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected. |   |
| ERROR |  Due to a more serious problem, the software has not been able to perform some function. |
| CRITICAL |  A serious error, indicating that the program itself may be unable to continue running. |

Más info: [logging-doc](https://docs.python.org/3/howto/logging.html)