from python_graphql_client import GraphqlClient
import asyncio
import os

service_endpoint = os.environ['SERVICE_ENDPOINT']
service_endpoint_ws = os.environ['SERVICE_ENDPOINT_WS']
client = GraphqlClient(endpoint=service_endpoint)
deleteImageNotificationClient = GraphqlClient(endpoint=service_endpoint_ws)

deletedImageMutation = """
    mutation DeltedImage ($name: String!, $node: ImageNodeInput!) {
      deletedNodeImage(name:$name, imageNodeInput:$node) {
        image {
          name
          deletedAt
        }
      }
    }
"""

deleteImageSubscription = """
    subscription {
        deleteImageNotification {
            id
            name
            nodes
        }
    }
"""

listImagesQuery = """
    query ListImages {
        images {
            name
            nodes {
                name
                namespace
            }
        }
    }
"""

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

# List for a notification and call delete_image with image info
# def deleteImageNotificationAsync():
#   asyncio.run(deleteImageNotificationClient.subscribe(query=deleteImageSubscription, handle=containerdshim.delete_image(data.name,data.node.namespace)))#proper way to access data?

def deleteImageNotificationAsync():
  asyncio.run(deleteImageNotificationClient.subscribe(query=deleteImageSubscription, handle=handleImageDeletion))

def handleImageDeletion(data):
  print('deletion handler called')
  print(data)

# def deletedNodeImage(image,namespace):
#   variables = {"name": image, "imageNodeInput": {"node": image.name, "namespace": namespace.name}}
#   data = client.execute(query=deletedImageMutation, variables=variables)
#   print(data) 

def listImages():
  data = client.execute(query=listImagesQuery)['data']
  images = []
  imageData = data['images']
  if imageData is None:
    return []
  for image in imageData:
    images.append(image)
  return images

def addImage(name,node,namespace):
  variables = { "image": { "name": name, "node": { "name": node, "namespace": namespace }}}
  data = client.execute(query=addImageMutation, variables=variables)
  print(data)
