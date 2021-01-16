# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import auto_pb2 as auto__pb2


class AutoControlStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Submit = channel.unary_unary(
        '/autocontrol.AutoControl/Submit',
        request_serializer=auto__pb2.Request.SerializeToString,
        response_deserializer=auto__pb2.Response.FromString,
        )


class AutoControlServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Submit(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AutoControlServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Submit': grpc.unary_unary_rpc_method_handler(
          servicer.Submit,
          request_deserializer=auto__pb2.Request.FromString,
          response_serializer=auto__pb2.Response.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'autocontrol.AutoControl', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
