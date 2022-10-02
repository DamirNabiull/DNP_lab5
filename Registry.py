import sys
import grpc
import chord_pb2 as pb2
import chord_pb2_grpc as pb2_grpc
from concurrent import futures


class RegistrySH(pb2_grpc.RegistryServiceServicer):
    def register(self, request, context):
        response = {'id': 1, 'm': 1}
        return pb2.RegisterResponse(**response)

    def deregister(self, request, context):
        response = {'status': True, 'message': 'No error'}
        return pb2.DeregisterResponse(**response)

    def populate_finger_table(self, request, context):
        for i in range(2):
            response = {'id': i+1, 'address': '127.0.0.0:5555'}
            yield pb2.NodeInfoItem(**response)


class RegistryClientSH(pb2_grpc.RegistryClientServiceServicer):
    def get_chord_info(self, request, context):
        for i in range(2):
            response = {'id': i + 1, 'address': '127.0.0.0:5555'}
            yield pb2.NodeInfoItem(**response)


if __name__ == '__main__':
    port, m = sys.argv[1:]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RegistryServiceServicer_to_server(RegistrySH(), server)
    pb2_grpc.add_RegistryClientServiceServicer_to_server(RegistryClientSH(), server)

    server.add_insecure_port(f'127.0.0.1:{port}')
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('\nShutting down')
