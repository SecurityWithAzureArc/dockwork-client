from python_graphql_client import GraphqlClient
import asyncio
import os

service_endpoint = os.environ['SERVICE_ENDPOINT']
service_endpoint_ws = os.environ['SERVICE_ENDPOINT_WS']
client = GraphqlClient(endpoint=service_endpoint)
deleteImageNotificationClient = GraphqlClient(endpoint=service_endpoint_ws)

deltedImageMutation = """
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
        addImage(imageInput:$image) {
            image {
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
def deleteImageNotificationAsync():
  asyncio.run(deleteImageNotificationClient.subscribe(query=deleteImageSubscription, handle=containerdshim.delete_image(data.name,data.node.namespace)))#proper way to access data?

def deletedNodeImage(image,namespace):
  variables = {"name": image, "imageNodeInput": {"node": image.name, "namespace": namespace.name}}
  data = client.execute(mutation=deltedImageMutation, variables=variables)
  print(data) 

def listImages():
  data = client.execute(query=listImagesQuery)
  images = {}
  for image in data.images:
    images[image.name] = image.nodes
  return images

def addImage(name,node,namespace):
  variables = { "imageInput": { "name": name, "node": { "name": node, "namespace": namespace }}}
  data = client.execute(mutation=addImageMutation, variables=variables)
  print(data)
