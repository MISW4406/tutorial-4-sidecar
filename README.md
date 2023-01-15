# Tutorial 4 - Sidecar, Adaptadores y Embajadores

Repositorio con código base para el desarrollo de sidecars, embajadores y embajadores.

Este repositorio está basado en el repositorio de [arquitectura hexagonal](https://github.com/MISW4406/tutorial-3-arquitectura-hexagonal) visto en el tutorial 3 del curso. Por tal motivo, puede usar ese mismo repositorio para entender algunos detalles que este README no cubre.

## Estructura del proyecto

Este repositorio sigue en general la misma estructura del repositorio de origen. Sin embargo, hay un par de adiciones importante mencionar:

El repositorio en su raíz está estructurado de la siguiente forma:



- **.github**: Directorio donde se localizan templates para Github y los CI/CD workflows 
- **src**: En este directorio encuentra el código fuente para AeroAlpes. En la siguiente sección se explica un poco mejor la estructura del mismo ([link](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure%3E) para más información)
- **tests**: Directorio con todos los archivos de prueba, tanto unitarios como de integración. Sigue el estándar [recomendado por pytest](https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html) y usado por [boto](https://github.com/boto/boto).
- **.gitignore**: Archivo con la definición de archivos que se deben ignorar en el repositorio GIT
- **.gitpod.yml**: Archivo que define las tareas/pasos a ejecutar para configurar su workspace en Gitpod
- **README.md**: El archivo que está leyendo :)
- **requirements.txt**: Archivo con los requerimientos para el correcto funcionamiento del proyecto (librerias Python)


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


https://grpc.io/docs/languages/python/quickstart/


 pyenv virtualenv 3.10.7 sidecar
 pyenv activate sidecar

 pip install grpcio

 python -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. protos/helloworld.proto
 python -m grpc_tools.protoc -Iprotos --python_out=. --pyi_out=. --grpc_python_out=. protos/vuelos.proto