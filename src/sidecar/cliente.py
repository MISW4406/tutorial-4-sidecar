from __future__ import print_function

from google.protobuf.timestamp_pb2 import Timestamp
from aeroalpes.pb2py import vuelos_pb2
from aeroalpes.pb2py import vuelos_pb2_grpc

import logging
import grpc
import datetime
import os
import json


def importar_comando_reserva(json_file):
    json_dict = json.load(json_file)

    # Transformamos en 
    legs = json_dict['itinerarios'][0]['odos'][0]['segmentos'][0]['legs']

    TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    for leg in legs:
        leg['fecha_salida'] = datetime.datetime.strptime(leg['fecha_salida'], TIMESTAMP_FORMAT)
        leg['fecha_llegada'] = datetime.datetime.now()

    return json_dict

def dict_a_proto_locacion(dict_locacion):
    return vuelos_pb2.Locacion(codigo=dict_locacion['codigo'], nombre=dict_locacion['nombre'])

def dict_a_proto_reserva(dict_reserva):
    itinerarios = list()
    for itin in dict_reserva.get('itinerarios', []):
        odos = list()
        for odo in itin.get('odos', []):
            segmentos = list()
            for seg in odo.get('segmentos', []):
                legs = list()
                for leg in seg.get('legs', []):
                    origen = dict_a_proto_locacion(leg['origen'])
                    destino = dict_a_proto_locacion(leg['destino'])

                    fecha_llegada = Timestamp()
                    fecha_llegada.FromSeconds(int(leg['fecha_llegada'].timestamp()))

                    fecha_salida = Timestamp()
                    fecha_salida.FromSeconds(int(leg['fecha_salida'].timestamp()))

                    
                    legs.append(vuelos_pb2.Leg(fecha_llegada=fecha_llegada, fecha_salida=fecha_salida, origen=origen, destino=destino))
                
                segmentos.append(vuelos_pb2.Segmento(legs=legs))
            odos.append(vuelos_pb2.Odo(segmentos=segmentos))
        itinerarios.append(vuelos_pb2.Itinerario(odos=odos))

    return vuelos_pb2.Reserva(id=dict_reserva.get('id'), itinerarios=itinerarios)


def run():

    print("Crear una reserva")
    with grpc.insecure_channel('localhost:50051') as channel:
        json_file = open(f'{os.path.dirname(__file__)}/mensajes/crear_reserva.json')
        json_dict = importar_comando_reserva(json_file)
        reserva = dict_a_proto_reserva(json_dict)


        stub = vuelos_pb2_grpc.VuelosStub(channel)
        response = stub.CrearReserva(reserva)
    print("Greeter client received: " + response.mensaje)
    print(f'Reserva: {response.reserva}')


if __name__ == '__main__':
    logging.basicConfig()
    run()