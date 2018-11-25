# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC route guide server."""

from concurrent import futures
import time

import grpc

import kiosk_pb2
import kiosk_pb2_grpc


class KioskServicer(kiosk_pb2_grpc.KioskServicer):
    """Provides methods that implement functionality of route guide server."""

    def command(self, request, context):
        print(request, context)
        return kiosk_pb2.Response(
            status='success'
        )        


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kiosk_pb2_grpc.add_KioskServicer_to_server(KioskServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
