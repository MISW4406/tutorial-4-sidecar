# Tutorial 4 - Sidecar, Adaptadores y Embajadores
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&repo=MISW4406/tutorial-4-sidecar) 

Repositorio con código base para el desarrollo de sidecars, adaptadores y embajadores. En este repositorio se presenta como crear un adaptador gRPC para que sistemas externos se puedan comunicar con un sistema legado usando un API REST. Para conocer más acerca de gRPC en Python puede consultar el siguiente [link](https://grpc.io/docs/languages/python/quickstart/).

Este repositorio está basado en el repositorio de [arquitectura hexagonal](https://github.com/MISW4406/tutorial-3-arquitectura-hexagonal) visto en el tutorial 3 del curso. Por tal motivo, puede usar ese mismo repositorio para entender algunos detalles que este README no cubre.

## Arquitectura

[![](https://img.plantuml.biz/plantuml/svg/ZLHDRzim3BtxLn2vR0E67VOB6dGRUYo6OjU2aHX7ZIog-iWI3Fdle-JOYTCOY2wMzIZfyV693p5XIBcppIVuO-G7D877zqo98gmmeaOW1nZUiqcaKWu86zfZomvjqtXKMsm95Z6e1VnhGCQuXXGOhQSu85FKcmLW1FcEeED444oxIS3h2LB6JwSz6vSYFBsyF0FjVQQOECBE8Foo6BVVndXokfxMVBnOiLkRjjxTJsUklmBBUAnBee4ox4IW0w1I51aGB1QvgEYdKKZTHONUgFEMOoKp_CpG-G3tXBHfkLpQ5IsaE0Vm8PDGAOkIWYAV-2uo7UiyS3dDB-esbT0QSeaMjz6Dd6-bwhTHBzwPnGA9il5L6uUTKRDnEzeOLSdEu9c6JFhf67QSKVUKyEIu7zmP9tIAaevQ5cfWf0RKIVAehwAZ64DKqGnaGMfXB9zV2dn6RusgllawsQRxIu30k7N0KiHSdzcNkueMYVHV3jkQw_0pa-C7k8pbgjX6ZOREGjner5HUHvTbSH8kdG4YUmu9NV7yPMEuGRYNVDeMej6aCFIC-_chtxOtUyIvWqZm63qkp_dJhxxxmmBcJCQfc6C6ZXHsfhZmOl_nnciX5_5jS7aVS2NtERTn-rAZBzO9qFv-VgngLfN56cFCwN59GzWd2evhcuAbvBmiEVSgZmeVcmUPImV_3m00)](https://editor.plantuml.com/uml/ZLHDRzim3BtxLn2vR0E67VOB6dGRUYo6OjU2aHX7ZIog-iWI3Fdle-JOYTCOY2wMzIZfyV693p5XIBcppIVuO-G7D877zqo98gmmeaOW1nZUiqcaKWu86zfZomvjqtXKMsm95Z6e1VnhGCQuXXGOhQSu85FKcmLW1FcEeED444oxIS3h2LB6JwSz6vSYFBsyF0FjVQQOECBE8Foo6BVVndXokfxMVBnOiLkRjjxTJsUklmBBUAnBee4ox4IW0w1I51aGB1QvgEYdKKZTHONUgFEMOoKp_CpG-G3tXBHfkLpQ5IsaE0Vm8PDGAOkIWYAV-2uo7UiyS3dDB-esbT0QSeaMjz6Dd6-bwhTHBzwPnGA9il5L6uUTKRDnEzeOLSdEu9c6JFhf67QSKVUKyEIu7zmP9tIAaevQ5cfWf0RKIVAehwAZ64DKqGnaGMfXB9zV2dn6RusgllawsQRxIu30k7N0KiHSdzcNkueMYVHV3jkQw_0pa-C7k8pbgjX6ZOREGjner5HUHvTbSH8kdG4YUmu9NV7yPMEuGRYNVDeMej6aCFIC-_chtxOtUyIvWqZm63qkp_dJhxxxmmBcJCQfc6C6ZXHsfhZmOl_nnciX5_5jS7aVS2NtERTn-rAZBzO9qFv-VgngLfN56cFCwN59GzWd2evhcuAbvBmiEVSgZmeVcmUPImV_3m00)

## Estructura del proyecto

Este repositorio sigue en general la misma estructura del repositorio de origen. Sin embargo, hay un par de adiciones importantes a mencionar:

- **src/sidecar**: En este directorio encuentra el código para el adaptador gRPC de AeroAlpes. En el, podrá encontrar el módulo `aeroalpes`, el cual cuenta con la definición de los servicios gRPC y mensajes Protobuf en el directorio `protos`. Por otra parte, el módulo `servicios` implementa las interfaces definidas en los archivos proto anteriomente descritos. Finalmente el módulo `pb2py` aloja los archivos compilados `.proto` en Python (para ver como compilarlos lea la siguientes secciones). El archivo `main.py` corre el servidor y `cliente.py` un cliente que crea una reserva usando un mensaje en JSON definido en el directorio `mensajes`.
- **.Dockerfile**: Cada servicio cuenta con un Dockerfile para la creación de la imagen y futura ejecución de la misma. El archivo `adaptador.Dockerfile` es el encargado de instalar las dependencias de nuestro servicio en gRPC y los comandos de ejecución. Mientras que el archivo `aeroalpes.Dockerfile` es el encargado de definir nuestro backend.
- **docker-compose.yml**: Este archivo nos define la forma de componer nuestros servicios. En este caso usted puede ver como creamos el Sidecar/adaptador por medio del uso de una red común para la comunicación entre contenedoras. En el caso de desplegar esta topología en un orquestador de contenedoras, el concepto va a ser similar.
- **sidecar-aeroalpes.yml**: Este es un archivo template para el despliegue de las contenedoras en mismo Pod en Kubernetes. Podrá observar que solo se expone el puerto del servicio gRPC, el cual sirve como adaptador con la contenedora del backend de AeroAlpes. Puede modificar y extender este template para desplegarlo en su cluster personal.

## AeroAlpes
### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/aeroalpes/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/aeroalpes/api --debug run
```

### Ejecutar pruebas

```bash
coverage run -m pytest
```

### Ver reporte de covertura
```bash
coverage report
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f aeroalpes.Dockerfile -t aeroalpes/flask
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 5000:5000 aeroalpes/flask
```

## Sidecar/Adaptador

### Instalar librerías

En el mundo real es probable que ambos proyectos estén en repositorios separados, pero por motivos pedagógicos y de simpleza, 
estamos dejando ambos proyectos en un mismo repositorio. Sin embargo, usted puede encontrar un archivo `sidecar-requirements.txt`, 
el cual puede usar para instalar las dependencias de Python para el servidor y cliente gRPC.

```bash
pip install -r sidecar-requirements.txt
```

### Ejecutar Servidor

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/sidecar/main.py 
```

### Ejecutar Cliente

Desde el directorio principal ejecute el siguiente comando.

```bash
python src/sidecar/cliente.py 
```

### Compilación gRPC

Desde el directorio `src/sidecar/aeroalpes` ejecute el siguiente comando.

```bash
python -m grpc_tools.protoc -Iprotos --python_out=./pb2py --pyi_out=./pb2py --grpc_python_out=./pb2py protos/vuelos.proto
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f adaptador.Dockerfile -t aeroalpes/adaptador
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 50051:50051 aeroalpes/adaptador
```

## Docker-compose

Para desplegar toda la arquitectura en un solo comando, usamos `docker-compose`. Para ello, desde el directorio principal, ejecute el siguiente comando:

```bash
docker-compose up
```

Si desea detener el ambiente ejecute:

```bash
docker-compose stop
```

En caso de querer desplegar dicha topología en el background puede usar el parametro `-d`.

```bash
docker-compose up -d
```

## Comandos útiles

### Listar contenedoras en ejecución
```bash
docker ps
```

### Listar todas las contenedoras
```bash
docker ps -a
```

### Parar contenedora
```bash
docker stop <id_contenedora>
```

### Eliminar contenedora
```bash
docker rm <id_contenedora>
```

### Listar imágenes
```bash
docker images
```

### Eliminar imágenes
```bash
docker images rm <id_imagen>
```

### Acceder a una contendora
```bash
docker exec -it <id_contenedora> sh
```

