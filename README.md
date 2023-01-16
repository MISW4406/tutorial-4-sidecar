# Tutorial 4 - Sidecar, Adaptadores y Embajadores

Repositorio con código base para el desarrollo de sidecars, adaptadores y embajadores. En este repositorio se presenta como crear un adaptador gRPC para que sistenas externos se puedan comunicar con un sistema legado con API REST. Para conocer más acerca de gRPC en Python puede consultar el siguiente [link](https://grpc.io/docs/languages/python/quickstart/).

Este repositorio está basado en el repositorio de [arquitectura hexagonal](https://github.com/MISW4406/tutorial-3-arquitectura-hexagonal) visto en el tutorial 3 del curso. Por tal motivo, puede usar ese mismo repositorio para entender algunos detalles que este README no cubre.

## Estructura del proyecto

Este repositorio sigue en general la misma estructura del repositorio de origen. Sin embargo, hay un par de adiciones importante mencionar:

- **src/sidecar**: En este directorio encuentra el código para el adaptador gRPC de AeroAlpes. En este directorio podrá encontrar en el módulo `aeroalpes` la definición de los servicios gRPC y mensajes Protobuf en el directorio `protos`. Por otra parte, el módulo `servicios` implementa las interfaces definidas en los archivos proto anteriomente descritos. Finalmente el módulo `pb2py` aloja los archivos compilados .proto en Python (para ver como compilarlos lea la siguiente sección). El archivo `main.py` corre el servidor y `cliente.py` un cliente que crea una reserva usando el mensaje en JSON definido en el directorio `mensajes`.

### AeroAlpes
## Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/aeroalpes/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/aeroalpes/api --debug run
```

## Ejecutar pruebas

```bash
coverage run -m pytest
```

# Ver reporte de covertura
```bash
coverage report
```

### Sidecar/Adaptador

## Instalar librerías

En el mundo real es probable que ambos proyectos estén en repositorios separados, pero por motivos pedagógicos y de simpleza, 
estamos dejando ambos proyectos en un mismo repositorio. Sin embargo, usted puede encontrar un archivo `sidecar-requirements.txt`, 
el cual puede usar para instalar las dependencias de Python para el servidor y cliente gRPC.

```bash
pip install -r sidecar-requirements.txt
```

## Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/sidecar/main.py 
```

## Ejecutar Cliente

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/sidecar/cliente.py 
```

## Compilación gRPC

Desde el directorio `src/sidecar` ejecute el siguiente comando.

```bash
python -m grpc_tools.protoc -Iprotos --python_out=./pb2py --pyi_out=./pb2py --grpc_python_out=./pb2py protos/vuelos.proto
```