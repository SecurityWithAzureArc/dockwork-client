from containerdshim import containerdshim
from python_graphql_client import GraphqlClient
import asyncio
import os
import threading
from threading import Lock
from osshim import osshim

service_endpoint = os.environ['SERVICE_ENDPOINT']
service_endpoint_ws = os.environ['SERVICE_ENDPOINT_WS']
client = GraphqlClient(endpoint=service_endpoint)
deleteImageNotificationClient = GraphqlClient(endpoint=service_endpoint_ws)

deletedImageMutation = """
    mutation DeletedImage ($name: String!, $node: ImageNodeInput!) {
      deletedNodeImage(imageName:$name, node:$node) {
        name
        deletedAt
      }
    }
"""

deleteImageSubscription = """
    subscription {
        deleteImageNotification {
            id
            name
            nodes {
                name
                namespace
            }
        }
    }
"""

listImagesQuery = """
    query ListImages ($skip: Int!) {
        images(skip: $skip) {
            name
            nodes {
                name
                namespace
            }
        }
    }
"""

# listImagesForNodeQuery = """
#     query ListImages ($node: ImadeNodeInput!) {
#         images (node: $node, deleted: true){
#             name
#             nodes {
#                 name
#                 namespace
#             }
#         }
#     }
# """

addImageMutation = """
    mutation AddImage ($image: ImageInput!) {
      addImage(image:$image) {
        name
        nodes {
          name
          namespace
        }
        createdAt
        deletedAt
      }
    }
"""

addImagesMutation = """
    mutation AddImages ($images: [ImageInput!]) {
      addImages(images:$images) {
        name
      }
    }
"""

# List for a notification and call delete_image with image info
# def deleteImageNotificationAsync():
#   asyncio.run(deleteImageNotificationClient.subscribe(query=deleteImageSubscription, handle=containerdshim.delete_image(data.name,data.node.namespace)))

def deleteImageNotificationAsync():
  asyncio.run(deleteImageNotificationClient.subscribe(query=deleteImageSubscription, handle=handleImageDeletion))

def handleImageDeletion(data):
  try:
    namespaceData = data['data']['deleteImageNotification']['nodes']
    namespace = ''
    hostname=osshim.get_hostname() 
    image = data['data']['deleteImageNotification']['name']
    for dataset in namespaceData:
      if dataset['name'] == hostname:
        namespace = dataset['namespace'].strip()
        break
    if namespace == '':
      print('ignore image deletion request for this node - image:', image)
      return
    containerdshim.delete_image(namespace, image)
    imageToRemove = { "name": image, "node": { "name": hostname, "namespace": namespace }}
    deletedNodeImage(imageToRemove)
    print('deleted image', image, 'in namespace', namespace)
  finally:
    thread = threading.Thread(target=deleteImageNotificationAsync)
    thread.start()

def removeImages(imagesToRemove):
  for image in imagesToRemove:
    deletedNodeImage(image)

def deletedNodeImage(image):
  variables = { 'name': image['name'], 'node': { 'name': image['node']['name'], 'namespace': image['node']['namespace']}}
  data = client.execute(query=deletedImageMutation, variables=variables)
  print(data) 

def listImagesInternal(skip):
  variables = { "skip": skip }
  data = client.execute(query=listImagesQuery, variables=variables)['data']
  images = []
  imageData = data['images']
  if imageData is None:
    return []
  for image in imageData:
    images.append(image)
  return images

def listImages():
  images = []
  skip = 0
  imageChunk = listImagesInternal(skip)
  while len(imageChunk) > 0:
    skip += len(imageChunk)
    images = images + imageChunk
    imageChunk = listImagesInternal(skip)
  print('num of images fetched from DB: ', len(images))
  return images

def addImage(name,node,namespace):
  variables = { "image": { "name": name, "node": { "name": node, "namespace": namespace }}}
  data = client.execute(query=addImageMutation, variables=variables)
  print(data)

def addImages(imagesToAdd):
  variables = { "images": imagesToAdd }
  data = client.execute(query=addImagesMutation, variables=variables)
  print("Added images")
  print(data)

thread = threading.Thread(target=deleteImageNotificationAsync)
thread.start()
