import sys
import grpc
import chord_pb2 as pb2
import chord_pb2_grpc as pb2_grpc
from concurrent import futures
from random import randrange as rand

registered_nodes: dict
available_ids: list
used_ids: list
max_size: int
m: int
is_debug: bool


class RegistrySH(pb2_grpc.RegistryServiceServicer):
    def register(self, request, context):
        len_ids = len(available_ids)
        node_addr = f'{request.ipaddr}:{request.port}'

        if len_ids == 0 or node_addr in registered_nodes.values():
            response = {
                'id': -1,
                'message': 'No available id or ipaddr with port are already registered'
            }
            return pb2.RegisterResponse(**response)

        node_id = available_ids.pop(rand(len_ids))
        registered_nodes[node_id] = node_addr
        used_ids.append(node_id)
        used_ids.sort()

        if is_debug:
            print('Registered nodes:', registered_nodes)
            print('Available IDs:', available_ids)
            print('Used IDs:', used_ids)

        response = {
            'id': node_id,
            'message': f'{m}'
        }
        return pb2.RegisterResponse(**response)

    def deregister(self, request, context):
        node_id = request.id
        if not (node_id in registered_nodes.keys()):
            response = {
                'status': False,
                'message': 'No such id is registered'
            }
            return pb2.RegisterResponse(**response)

        del registered_nodes[node_id]
        used_ids.remove(node_id)
        available_ids.append(node_id)

        if is_debug:
            print('Registered nodes:', registered_nodes)
            print('Available IDs:', available_ids)
            print('Used IDs:', used_ids)

        response = {
            'status': True,
            'message': 'deregister completed successfully'
        }
        return pb2.DeregisterResponse(**response)

    def populate_finger_table(self, request, context):
        # Find predecessor
        ind = used_ids.index(request.id)
        pred_id = used_ids[ind-1]
        response = {'id': pred_id, 'address': registered_nodes[pred_id]}
        yield pb2.NodeInfoItem(**response)

        # Generate
        # if len(available_ids) > 0:
        #     for i in range(m):
        #         response = {'id': i + 1, 'address': '127.0.0.0:5555'}
        #         yield pb2.NodeInfoItem(**response)


class RegistryClientSH(pb2_grpc.RegistryClientServiceServicer):
    def get_chord_info(self, request, context):
        for i in range(2):
            response = {'id': i + 1, 'address': '127.0.0.0:5555'}
            yield pb2.NodeInfoItem(**response)


if __name__ == '__main__':
    port, m = map(int, sys.argv[1:])
    registered_nodes = {}
    max_size = 2 ** m
    available_ids = [i for i in range(max_size)]
    used_ids = []
    is_debug = True

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RegistryServiceServicer_to_server(RegistrySH(), server)
    pb2_grpc.add_RegistryClientServiceServicer_to_server(RegistryClientSH(), server)

    server.add_insecure_port(f'127.0.0.1:{port}')
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('\nShutting down')
