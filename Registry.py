import sys
import grpc
import chord_pb2 as pb2
import chord_pb2_grpc as pb2_grpc
from concurrent import futures
import random

registered_nodes: dict
available_ids: list
used_ids: list
max_size: int
m: int
random.seed(0)


class RegistrySH(pb2_grpc.RegistryServiceServicer):
    def register(self, request, context):
        print('Register:')
        len_ids = len(available_ids)
        node_addr = f'{request.ipaddr}:{request.port}'

        if len_ids == 0 or node_addr in registered_nodes.values():
            response = {
                'id': -1,
                'message': 'No available id or ipaddr with port are already registered'
            }
            print('\t', response['message'], end='\n\n')
            return pb2.RegisterResponse(**response)

        new_id = random.randint(0, max_size - 1)
        while new_id in used_ids:
            new_id = random.randint(0, max_size - 1)

        avail_ind = available_ids.index(new_id)
        node_id = available_ids.pop(avail_ind)
        registered_nodes[node_id] = node_addr
        used_ids.append(node_id)
        used_ids.sort()

        response = {
            'id': node_id,
            'message': f'{m}'
        }
        print('\t', response['id'], end='\n\n')
        return pb2.RegisterResponse(**response)

    def deregister(self, request, context):
        print('Deregister:')
        node_id = request.id
        if not (node_id in registered_nodes.keys()):
            response = {
                'status': False,
                'message': 'No such id is registered'
            }
            print('\tId:', node_id, '-', response['message'], end='\n\n')
            return pb2.RegisterResponse(**response)

        del registered_nodes[node_id]
        used_ids.remove(node_id)
        available_ids.append(node_id)

        response = {
            'status': True,
            'message': 'deregister completed successfully'
        }
        print('\tId:', node_id, '-', response['message'], end='\n\n')
        return pb2.DeregisterResponse(**response)

    def populate_finger_table(self, request, context):
        # Find predecessor
        p = request.id
        ind = used_ids.index(p)
        used_l = len(used_ids)
        pred_id = used_ids[ind - 1]
        response = {'id': pred_id, 'address': registered_nodes[pred_id]}
        yield pb2.NodeInfoItem(**response)

        # Generate FT
        prev_node = p
        if used_l > 1:
            ind = (ind + 1) % used_l
            for i in range(0, m):
                val = (p + (2 ** i)) % max_size

                while True:
                    if (val <= used_ids[ind]) or (used_ids[ind] < used_ids[ind - 1] < val):
                        if used_ids[ind] != prev_node:
                            prev_node = used_ids[ind]
                            response = {'id': prev_node, 'address': registered_nodes[prev_node]}
                            yield pb2.NodeInfoItem(**response)
                        break
                    ind = (ind + 1) % used_l
        else:
            yield pb2.NodeInfoItem(**response)


class RegistryClientSH(pb2_grpc.RegistryClientServiceServicer):
    def get_chord_info(self, request, context):
        for node_id in registered_nodes:
            response = {'id': node_id, 'address': registered_nodes[node_id]}
            yield pb2.NodeInfoItem(**response)

    def connect(self, request, context):
        print('Client connect', end='\n\n')
        response = {'type': 'registry'}
        return pb2.ConnectResponse(**response)


if __name__ == '__main__':
    port, m = map(int, sys.argv[1:])
    registered_nodes = {}
    max_size = 2 ** m
    available_ids = [i for i in range(max_size)]
    used_ids = []

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RegistryServiceServicer_to_server(RegistrySH(), server)
    pb2_grpc.add_RegistryClientServiceServicer_to_server(RegistryClientSH(), server)

    server.add_insecure_port(f'127.0.0.1:{port}')
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('\nShutting down')
