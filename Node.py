from concurrent import futures
import chord_pb2_grpc as pb2_grpc
import chord_pb2 as pb2
import grpc
import zlib
import sys

chord_data: dict
finger_table: dict
node_id: int
m: int
pred: int


def lookup(target_id, nodes):
    if pred < target_id <= node_id:
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
    target_id = hash_value % 2 ** m
    return target_id


class NodeSH(pb2_grpc.NodeServiceServicer):
    def get_finger_table(self, request, context):
        reply = {}
        return pb2.NodeInfoItem(** reply)

    def save(self, request, context):
        f = True
        msg1 = ""
        target_id = getTargetId(request.key)

        reply = {"status": f, "message": msg1}
        return pb2.NodeActionResponse(**reply)

    def remove(self, request, context):
        f = True
        msg2 = ""
        target_id = getTargetId(request.key)

        reply = {"status": f, "message": msg2}
        return pb2.NodeActionResponse(**reply)

    def find(self, request, context):
        f = True
        msg3 = ""
        target_id = getTargetId(request.key)

        reply = {"status": f, "message": msg3}
        return pb2.NodeActionResponse(**reply)


if __name__ == "__main__":
    chord_data = {}
    finger_table = []
    node_id = -1
    m = 0

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
            print(node_id, m)
        else:
            print(response.message)
            sys.exit(0)

        msg = pb2.PopulateFingerTableRequest(id=node_id)
        responses = stub.populate_finger_table(msg)
        for r in responses:
            print(r)

        while True:
            x = 1

    except KeyboardInterrupt:
        # Deregister
        if node_id >= 0:
            msg = pb2.DeregisterRequest(id=node_id)
            response = stub.deregister(msg)
            print(f"\n({response.status}, {response.message})")
        sys.exit(0)
