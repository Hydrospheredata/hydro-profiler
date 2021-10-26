# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import profiler.protobuf.monitoring_manager_pb2 as monitoring__manager__pb2


class PluginManagementServiceStub(object):
    """=== END OF contract modeling ===

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterPlugin = channel.unary_unary(
                '/monitoring_manager.PluginManagementService/RegisterPlugin',
                request_serializer=monitoring__manager__pb2.RegisterPluginRequest.SerializeToString,
                response_deserializer=monitoring__manager__pb2.RegisterPluginResponse.FromString,
                )


class PluginManagementServiceServicer(object):
    """=== END OF contract modeling ===

    """

    def RegisterPlugin(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PluginManagementServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterPlugin': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterPlugin,
                    request_deserializer=monitoring__manager__pb2.RegisterPluginRequest.FromString,
                    response_serializer=monitoring__manager__pb2.RegisterPluginResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'monitoring_manager.PluginManagementService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PluginManagementService(object):
    """=== END OF contract modeling ===

    """

    @staticmethod
    def RegisterPlugin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/monitoring_manager.PluginManagementService/RegisterPlugin',
            monitoring__manager__pb2.RegisterPluginRequest.SerializeToString,
            monitoring__manager__pb2.RegisterPluginResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ModelCatalogServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetModelUpdates = channel.unary_stream(
                '/monitoring_manager.ModelCatalogService/GetModelUpdates',
                request_serializer=monitoring__manager__pb2.GetModelUpdatesRequest.SerializeToString,
                response_deserializer=monitoring__manager__pb2.GetModelUpdatesResponse.FromString,
                )


class ModelCatalogServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetModelUpdates(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ModelCatalogServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetModelUpdates': grpc.unary_stream_rpc_method_handler(
                    servicer.GetModelUpdates,
                    request_deserializer=monitoring__manager__pb2.GetModelUpdatesRequest.FromString,
                    response_serializer=monitoring__manager__pb2.GetModelUpdatesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'monitoring_manager.ModelCatalogService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ModelCatalogService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetModelUpdates(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/monitoring_manager.ModelCatalogService/GetModelUpdates',
            monitoring__manager__pb2.GetModelUpdatesRequest.SerializeToString,
            monitoring__manager__pb2.GetModelUpdatesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class DataStorageServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetInferenceDataUpdates = channel.stream_stream(
                '/monitoring_manager.DataStorageService/GetInferenceDataUpdates',
                request_serializer=monitoring__manager__pb2.GetInferenceDataUpdatesRequest.SerializeToString,
                response_deserializer=monitoring__manager__pb2.GetInferenceDataUpdatesResponse.FromString,
                )


class DataStorageServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetInferenceDataUpdates(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataStorageServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetInferenceDataUpdates': grpc.stream_stream_rpc_method_handler(
                    servicer.GetInferenceDataUpdates,
                    request_deserializer=monitoring__manager__pb2.GetInferenceDataUpdatesRequest.FromString,
                    response_serializer=monitoring__manager__pb2.GetInferenceDataUpdatesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'monitoring_manager.DataStorageService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DataStorageService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetInferenceDataUpdates(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/monitoring_manager.DataStorageService/GetInferenceDataUpdates',
            monitoring__manager__pb2.GetInferenceDataUpdatesRequest.SerializeToString,
            monitoring__manager__pb2.GetInferenceDataUpdatesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
