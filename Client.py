import sys
import grpc
import chord_pb2 as pb2
import chord_pb2_grpc as pb2_grpc

registry: pb2_grpc.RegistryClientServiceStub
node: pb2_grpc.NodeServiceStub
connection_type = 0  # 0 - No connection, 1 - registry, 2 - node
conn_timeout = 1


def get_command_with_args(text: str):
    arr = text.split(' ', 1)
    if len(arr) == 1:
        return arr[0], None
    command, arguments = arr[0], arr[1]
    return command, arguments


def create_connection(host: str):
    global registry, node, connection_type

    try:
        channel = grpc.insecure_channel(host)
        print(grpc.channel_ready_future(channel).result(timeout=conn_timeout))
        registry = pb2_grpc.RegistryClientServiceStub(channel)
        connection_type = 1
        print('Connected to Registry')
    except Exception as e:
        print(e)
        pass

    if connection_type == 0:
        try:
            channel = grpc.insecure_channel(host)
            print(grpc.channel_ready_future(channel).result(timeout=conn_timeout))
            node = pb2_grpc.NodeServiceStub(channel)
            connection_type = 2
            print('Connected to Node')
        except Exception as e:
            print(e)
            print('There is no Registry/Node on this address')


if __name__ == '__main__':
    while True:
        line = input('> ')
        cmd, args = get_command_with_args(line)

        if cmd == 'connect':
            connection_type = 0
            create_connection(args)
        elif cmd == 'get_info':
            if connection_type == 1:
                responses = registry.get_chord_info(pb2.Empty())
                for response in responses:
                    print(response)
            elif connection_type == 2:
                responses = node.get_finger_table(pb2.Empty())
                for response in responses:
                    print(response)
            else:
                print('Nothing is connected')
        elif cmd == 'save':
            if connection_type == 2:
                key, text = args.split(' ', 1)
                msg = pb2.SaveRequest(key=key, text=text)
                response = node.save(msg)
                print(response)
            else:
                print('Node is not connected')
        elif cmd == 'remove':
            if connection_type == 2:
                msg = pb2.FindRemoveRequest(key=args)
                response = node.remove(msg)
                print(response)
            else:
                print('Node is not connected')
        elif cmd == 'find':
            if connection_type == 2:
                msg = pb2.FindRemoveRequest(key=args)
                response = node.find(msg)
                print(response)
            else:
                print('Node is not connected')
        elif cmd == 'quit':
            print('Shutting down')
            break
        else:
            print('Unacceptable command')
