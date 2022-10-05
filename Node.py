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


def lookup(target_id, nodes):
    if predecessor[0] < target_id <= node_id:
        return node_id
    elif predecessor[0] == node_id:
        return node_id
    else:
        for i in range(len(nodes)):
            if nodes[i] > nodes[i+1]:
                if nodes[i] <= target_id or target_id < nodes[i+1]:
                    return nodes[i]
            else:
                if nodes[i] <= target_id < nodes[i+1]:
                    return nodes[i]


def getTargetId(key):
    hash_value = zlib.adler32(key.encode())
    target_id = hash_value % (2 ** m)
    return target_id


def getPopulateFingerTable():
    global node_is_running, predecessor, successor, finger_table_ind

    while node_is_running:
        msg_ = pb2.PopulateFingerTableRequest(id=node_id)
        responses = stub.populate_finger_table(msg_)
        finger_table_ind = []

        for r in responses:
            finger_table_ind.append(r.id)
            finger_table[r.id] = r.address

        predecessor = (finger_table_ind[0], finger_table[finger_table_ind[0]])
        successor = (finger_table_ind[1], finger_table[finger_table_ind[1]])
        if finger_table_ind[0] != finger_table_ind[1]:
            finger_table.pop(finger_table_ind[0])
        del finger_table_ind[0]

        sleep(1)


class NodeSH(pb2_grpc.NodeServiceServicer):
    def get_finger_table(self, request, context):
        for key in finger_table_ind:
            reply = {"id": key, "address": finger_table[key]}
            yield pb2.NodeInfoItem(** reply)

    def save(self, request, context):
        key = request.key
        text = request.text
        target_id = getTargetId(request.key)
        next_node = lookup(target_id, finger_table_ind)

        if next_node == node_id:
            if chord_data[key] in chord_data.keys():
                reply = {"status": False, "message": f"key {key} already exists"}
            else:
                chord_data[key] = text
                reply = {"status": True, "message": f"{key} is saved in node {next_node}"}
        else:
            # Connect to Node
            node_channel = grpc.insecure_channel(finger_table[next_node])
            node_stub = pb2_grpc.NodeServiceStub(node_channel)

            msg_ = pb2.SaveRequest(key=key, text=text)
            reply = node_stub.save(msg_)

        return pb2.NodeActionResponse(**reply)

    def remove(self, request, context):
        key = request.key
        target_id = getTargetId(request.key)
        next_node = lookup(target_id, finger_table_ind)

        if next_node == node_id:
            if chord_data[key] in chord_data.keys():
                chord_data.pop(key)
                reply = {"status": True, "message": f"Node {next_node} it was removed from"}
            else:
                reply = {"status": False, "message": f"key {key} does not exist"}
        else:
            # Connect to Node
            node_channel = grpc.insecure_channel(finger_table[next_node])
            node_stub = pb2_grpc.NodeServiceStub(node_channel)

            msg_ = pb2.FindRemoveRequest(key=key)
            reply = node_stub.remove(msg_)

        return pb2.NodeActionResponse(**reply)

    def find(self, request, context):
        key = request.key
        target_id = getTargetId(request.key)
        next_node = lookup(target_id, finger_table_ind)

        if next_node == node_id:
            if chord_data[key] in chord_data.keys():
                reply = {"status": True,
                         "message": f"{key} is saved in node {next_node}, Address: {finger_table[next_node]}"}
            else:
                reply = {"status": False, "message": f"key {key} does not exist"}
        else:
            # Connect to Node
            node_channel = grpc.insecure_channel(finger_table[next_node])
            node_stub = pb2_grpc.NodeServiceStub(node_channel)

            msg_ = pb2.FindRemoveRequest(key=key)
            reply = node_stub.find(msg_)

        return pb2.NodeActionResponse(**reply)

    def connect(self, request, context):
        reply = {'type': f'node {node_id}'}
        return pb2.ConnectResponse(**reply)


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

        node_server.wait_for_termination()
    except KeyboardInterrupt:
        # Stop getting finger table
        node_is_running = False
        t1.join()

        # Deregister
        if node_id >= 0:
            msg = pb2.DeregisterRequest(id=node_id)
            response = stub.deregister(msg)
            print(f"\n({response.status}, {response.message})")
        sys.exit(0)
