import grpc
import service_pb2
import service_pb2_grpc

def say_hello(name):
    channel = grpc.insecure_channel('grpc-server:50051')
    stub = service_pb2_grpc.MyServiceStub(channel)
    response = stub.SayHello(service_pb2.HelloRequest(name=name))
    return response.message
