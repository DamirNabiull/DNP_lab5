from concurrent import futures
from time import sleep
import chord_pb2_grpc as pb2_grpc
import chord_pb2 as pb2
import threading
import grpc
import zlib
import sys

node_is_running = True
chord_data: dict
finger_table_ind: list
finger_table: dict
node_id: int
m: int
predecessor: (int, str)
successor: (int, str)
populate_block = False


def lookup(target_id, nodes):
    if predecessor[0] < target_id <= node_id:
        return node_id
    elif predecessor[0] > node_id and (predecessor[0] < target_id or target_id <= node_id):
        return node_id
    elif predecessor[0] == node_id:
        return node_id
    elif node_id < target_id <= nodes[0]:
        return nodes[0]
    elif node_id > nodes[0] and (node_id < target_id or target_id <= nodes[0]):
        return nodes[0]
    else:
        for i in range(1, len(nodes)):
            if nodes[i - 1] > nodes[i]:
                if nodes[i - 1] < target_id or target_id <= nodes[i]:
                    return nodes[i]
            elif nodes[i - 1] < target_id < nodes[i]:
                return nodes[i]
        return nodes[-1]


def getTargetId(key):
    hash_value = zlib.adler32(key.encode())
    target_id = hash_value % (2 ** m)
    return target_id


def getPopulateFingerTable():
    global node_is_running, predecessor, successor, finger_table_ind, populate_block

    while node_is_running:
        if not populate_block:
            msg_ = pb2.PopulateFingerTableRequest(id=node_id)
            responses = stub.populate_finger_table(msg_)
            table_ind = []

            for r in responses:
                table_ind.append(r.id)
                finger_table[r.id] = r.address

            predecessor = (table_ind[0], finger_table[table_ind[0]])
            successor = (table_ind[1], finger_table[table_ind[1]])
            if table_ind[0] != table_ind[1] and table_ind.count(table_ind[0]) == 1:
                finger_table.pop(table_ind[0])
            del table_ind[0]

            finger_table_ind = table_ind

        sleep(1)


class NodeSH(pb2_grpc.NodeServiceServicer):
    def get_finger_table(self, request, context):
        global populate_block
        populate_block = True
        for key in finger_table_ind:
            reply = {"id": key, "address": finger_table[key]}
            yield pb2.NodeInfoItem(** reply)
        populate_block = False

    def save(self, request, context):
        global populate_block
        populate_block = True
        key = request.key
        text = request.text
        target_id = getTargetId(key)
        next_node = lookup(target_id, finger_table_ind)

        if next_node == node_id:
            if key in chord_data.keys():
                reply = {"status": False, "message": f"key {key} already exists"}
            else:
                chord_data[key] = text
                reply = {"status": True, "message": f"{key} {next_node}"}
        else:
            # Connect to Node
            node_channel = grpc.insecure_channel(finger_table[next_node])
            node_stub = pb2_grpc.NodeServiceStub(node_channel)

            msg_ = pb2.SaveRequest(key=key, text=text)
            reply = node_stub.save(msg_)
            reply = {"status": reply.status, "message": reply.message}

        populate_block = False
        return pb2.NodeActionResponse(**reply)

    def remove(self, request, context):
        global populate_block
        populate_block = True
        key = request.key
        target_id = getTargetId(key)
        next_node = lookup(target_id, finger_table_ind)

        if next_node == node_id:
            if key in chord_data.keys():
                chord_data.pop(key)
                reply = {"status": True, "message": f"{next_node}"}
            else:
                reply = {"status": False, "message": f"{key} doesn't exist"}
        else:
            # Connect to Node
            node_channel = grpc.insecure_channel(finger_table[next_node])
            node_stub = pb2_grpc.NodeServiceStub(node_channel)

            msg_ = pb2.FindRemoveRequest(key=key)
            reply = node_stub.remove(msg_)
            reply = {"status": reply.status, "message": reply.message}

        populate_block = False
        return pb2.NodeActionResponse(**reply)

    def find(self, request, context):
        global populate_block
        populate_block = True
        key = request.key
        target_id = getTargetId(key)
        next_node = lookup(target_id, finger_table_ind)

        if next_node == node_id:
            if key in chord_data.keys():
                reply = {"status": True,
                         "message": f"{next_node}"}
            else:
                reply = {"status": False, "message": f"{key} doesn't exist"}
        else:
            # Connect to Node
            node_channel = grpc.insecure_channel(finger_table[next_node])
            node_stub = pb2_grpc.NodeServiceStub(node_channel)

            msg_ = pb2.FindRemoveRequest(key=key)
            reply = node_stub.find(msg_)
            reply = {"status": reply.status, "message": reply.message}

        populate_block = False
        return pb2.NodeActionResponse(**reply)

    def connect(self, request, context):
        reply = {'type': f'node {node_id}'}
        return pb2.ConnectResponse(**reply)

    def request_key_value(self, request, context):
        id_pred = request.id
        for k in chord_data.keys():
            if getTargetId(k) <= id_pred:
                reply = {"key": k, "text": chord_data[k]}
                chord_data.pop(k)
                yield pb2.KeyValueResponse(** reply)


if __name__ == "__main__":
    chord_data = {}
    finger_table = {}
    node_id = -1
    m = 0
    predecessor = ()
    successor = ()

    t1 = threading.Thread(target=getPopulateFingerTable)

    # Start NodeServer
    ip, port = sys.argv[2].split(":")

    node_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_NodeServiceServicer_to_server(NodeSH(), node_server)
    node_server.add_insecure_port(ip+":"+port)
    node_server.start()

    # Connect Registry
    registry_channel = grpc.insecure_channel(sys.argv[1])
    stub = pb2_grpc.RegistryServiceStub(registry_channel)

    try:
        # Register
        msg = pb2.RegisterRequest(ipaddr=ip, port=int(port))
        response = stub.register(msg)

        if response.id >= 0:
            node_id = response.id
            m = int(response.message)
        else:
            print(response.message)
            sys.exit(0)

        t1.start()

        sleep(1)
        if successor[0] != node_id:
            node_channel1 = grpc.insecure_channel(successor[1])
            node_stub1 = pb2_grpc.NodeServiceStub(node_channel1)

            msg1_ = pb2.KeyValueRequest(id=node_id)
            responses = node_stub1.request_key_value(msg1_)
            for r in responses:
                chord_data[r.key] = r.text

        node_server.wait_for_termination()
    except KeyboardInterrupt:
        # Stop getting finger table
        node_is_running = False
        t1.join()

        # Deregister
        if node_id >= 0:
            msg = pb2.DeregisterRequest(id=node_id)
            response = stub.deregister(msg)
            print(f"\n{response.status}, {response.message}")

        sleep(1)
        if node_id != successor[0]:
            node_channel1 = grpc.insecure_channel(successor[1])
            node_stub1 = pb2_grpc.NodeServiceStub(node_channel1)

            for k in chord_data.keys():
                msg1_ = pb2.SaveRequest(key=k, text=chord_data[k])
                response = node_stub1.save(msg1_)
                print(response)

        sys.exit(0)
