# ChotuveMediaServer

## Instalación de dependencias
`$ pip install -r requirements.txt`

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