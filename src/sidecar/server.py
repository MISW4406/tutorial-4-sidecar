from concurrent import futures
import logging

import grpc
import vuelos_pb2
import vuelos_pb2_grpc
import requests
import json
import os
import datetime

from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp


TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

class Vuelos(vuelos_pb2_grpc.VuelosServicer):
    def CrearReserva(self, request, context):
        dict_obj = MessageToDict(request, preserving_proto_field_name=True)

        r = requests.post('http://localhost:5000/vuelos/reserva', json=dict_obj)
        if r.status_code == 200:
            respuesta = json.loads(r.text)

            fecha_creacion_dt = datetime.datetime.strptime(respuesta['fecha_creacion'], TIMESTAMP_FORMAT)
            fecha_creacion = Timestamp()
            fecha_creacion.FromDatetime(fecha_creacion_dt)

            fecha_actualizacion_dt = datetime.datetime.strptime(respuesta['fecha_actualizacion'], TIMESTAMP_FORMAT)
            fecha_actualizacion = Timestamp()
            fecha_actualizacion.FromDatetime(fecha_actualizacion_dt)

            reserva =  vuelos_pb2.Reserva(id=respuesta.get('id'), 
                itinerarios=respuesta.get('itinerarios',[]), 
                fecha_actualizacion=fecha_actualizacion, 
                fecha_creacion=fecha_creacion)

            return vuelos_pb2.RespuestaReserva(mensaje='OK', reserva=reserva)
        else:
            return vuelos_pb2.RespuestaReserva(mensaje=f'Error: {r.status_code}')

    def ConsultarReserva(self, request, context):
        pass
    

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    vuelos_pb2_grpc.add_VuelosServicer_to_server(Vuelos(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()


