#!/usr/bin/env python3

import grpc
from containerd.services.images.v1 import images_pb2_grpc, images_pb2
from containerd.services.namespaces.v1 import namespace_pb2_grpc, namespace_pb2

def list_images():
  with grpc.insecure_channel('unix:///var/run/containerd/containerd.sock') as channel:
    namespacev1 = namespace_pb2_grpc.NamespacesStub(channel)
    namespaces = namespacev1.List(namespace_pb2.ListNamespacesRequest()).namespaces
    for namespace in namespaces:
      imagev1 = images_pb2_grpc.ImagesStub(channel)
      images = imagev1.List(images_pb2.ListImagesRequest(), metadata=(('containerd-namespace', namespace.name),)).images
      for image in images:
        print('namespace:', namespace.name , 'name:', image.name, 'digest:', image.target.digest)

def delete_image(namespace, image):
  with grpc.insecure_channel('unix:///var/run/containerd/containerd.sock') as channel:
    imagev1 = images_pb2_grpc.ImagesStub(channel)
    # namespace example: 'k8s.io'
    # image example: 'registry.hub.docker.com/disi33/image-cleanup-worker:0.0.9'
    imagev1.Delete(images_pb2.DeleteImageRequest(name=image, sync=True), metadata=(('containerd-namespace', namespace),))
