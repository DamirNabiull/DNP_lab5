from concurrent import futures
import chord_pb2_grpc as pb2_grpc
import chord_pb2 as pb2
import grpc
import zlib
import sys

chord_data: dict
finger_table: list
node_id: int
m: int


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
        msg = ""
        reply = {"status": f, "message": msg}
        return pb2.NodeActionResponse(**reply)

    def remove(self, request, context):
        f = True
        msg = ""
        reply = {"status": f, "message": msg}
        return pb2.NodeActionResponse(**reply)

    def find(self, request, context):
        f = True
        msg = ""
        reply = {"status": f, "message": msg}
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

        if response.id > 0:
            node_id = response.id
            m = int(response.message)
            print(node_id, m)
        else:
            print(response.message)
            sys.exit(0)

    except KeyboardInterrupt:
        # Deregister
        if node_id > 0:
            msg = pb2.DeregisterRequest(id=node_id)
            response = stub.deregister(msg)
            print(response)
        sys.exit(0)
