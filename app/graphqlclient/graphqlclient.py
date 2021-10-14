from containerdshim import containerdshim
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
            nodes {
                name
                namespace
            }
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
    mutation AddImage ($images: ImageInput!) {
      addImage(images:$images) {
        images{
          name
          nodes {
            name
            namespace
          }
          createdAt
          deletedAt
        }
      }
    }
"""

# List for a notification and call delete_image with image info
# def deleteImageNotificationAsync():
#   asyncio.run(deleteImageNotificationClient.subscribe(query=deleteImageSubscription, handle=containerdshim.delete_image(data.name,data.node.namespace)))
event_loop = asyncio.new_event_loop()
def deleteImageNotificationAsync():
  asyncio.set_event_loop(event_loop)
  event_loop.run_forever()
  asyncio.create_task(deleteImageNotificationClient.subscribe(query=deleteImageSubscription, handle=handleImageDeletion))

def handleImageDeletion(data):
  lock = Lock()
  lock.acquire() # will block if lock is already held
  print("something")
  print('deletion handler called')
  lock.release()
  
  namespace = data['data']['nodes']['namespace']
  image = data['data']['name']
  containerdshim.delete_image(namespace, image)
  print(data)

# def deletedNodeImage(image,namespace):
#   variables = {"name": image, "imageNodeInput": {"node": image.name, "namespace": namespace.name}}
#   data = client.execute(query=deletedImageMutation, variables=variables)
#   print(data) 

def listImages():
  # variables = { "node": {"node": name, "namespace": namespace }, "deleted": True }
  data = client.execute(query=listImagesQuery)['data']
  images = []
  imageData = data['images']
  if imageData is None:
    return []
  for image in imageData:
    # containerdshim.delete_iamge(image['nodes']['namespace'], image['name'])
    images.append(image)
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
