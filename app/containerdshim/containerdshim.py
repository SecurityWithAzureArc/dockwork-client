#!/usr/bin/env python3

import grpc
from containerd.services.images.v1 import images_pb2_grpc, images_pb2
from containerd.services.namespaces.v1 import namespace_pb2_grpc, namespace_pb2
from containerd.services.containers.v1 import containers_pb2_grpc, containers_pb2
from data import image

def list_all_namespaces_internal(channel):
  namespacev1 = namespace_pb2_grpc.NamespacesStub(channel)
  namespaces = namespacev1.List(namespace_pb2.ListNamespacesRequest()).namespaces
  namespaceData = []
  for namespace in namespaces:
    namespaceData.append(namespace.name)
  return namespaceData

def list_all_images():
  with grpc.insecure_channel('unix:///var/run/containerd/containerd.sock') as channel:
    all_namespaces=list_all_namespaces_internal(channel)
    imageData = []
    imagev1 = images_pb2_grpc.ImagesStub(channel)
    for namespace in all_namespaces:
      images = imagev1.List(images_pb2.ListImagesRequest(), metadata=(('containerd-namespace', namespace),)).images
      for foundImage in images:
        imageData.append(image.image(foundImage.name, namespace, foundImage.target.digest))
    return imageData

def get_image_internal(channel, name, namespace):
  imagev1 = images_pb2_grpc.ImagesStub(channel)
  try:
    return imagev1.Get(images_pb2.GetImageRequest(name=name), metadata=(('containerd-namespace', namespace),)).image
  except grpc._channel._InactiveRpcError as err:
    if err._state.code != grpc.StatusCode.NOT_FOUND:
      raise err
    else:
      return None

def list_running_images():
  with grpc.insecure_channel('unix:///var/run/containerd/containerd.sock') as channel:
    all_namespaces=list_all_namespaces_internal(channel)
    imageData = []
    containerv1 = containers_pb2_grpc.ContainersStub(channel)
    for namespace in all_namespaces:
      containers = containerv1.List(containers_pb2.ListContainersRequest(), metadata=(('containerd-namespace', namespace),)).containers
      for foundContainer in containers:
        imageDetails=get_image_internal(channel, foundContainer.image, namespace)
        imageDigest = '' if imageDetails is None else imageDetails.target.digest
        imageData.append(image.image(foundContainer.image, namespace, imageDigest))
    return imageData

def delete_image(namespace, image):
  with grpc.insecure_channel('unix:///var/run/containerd/containerd.sock') as channel:
    imagev1 = images_pb2_grpc.ImagesStub(channel)
    # namespace example: 'k8s.io'
    # image example: 'registry.hub.docker.com/disi33/image-cleanup-worker:0.0.9'
    imagev1.Delete(images_pb2.DeleteImageRequest(name=image, sync=True), metadata=(('containerd-namespace', namespace),))