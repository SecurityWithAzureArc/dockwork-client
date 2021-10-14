#!/usr/bin/env python3

from containerdshim import containerdshim
from graphqlclient import graphqlclient
from data import image
import threading
from datetime import datetime
import time
import os

def main():
  service_endpoint = os.environ['SERVICE_ENDPOINT']
  service_endpoint_ws = os.environ['SERVICE_ENDPOINT_WS']
  print('using backend endpoint:', service_endpoint)
  print('using backend websocket endpoint:', service_endpoint_ws)
  running_images = containerdshim.list_running_images()  
  print('Number of currently running images:', len(running_images))
  #print_image_data(running_images)
  print('================================')

  update_image_data()

  while True:
    time.sleep(300)

def update_image_data():
  imageData = containerdshim.list_all_images()

  print('starting image update process')
  currentTime = datetime.now()
  print('started at time:', currentTime.strftime('%H:%M:%S'))

  print('schedule next iteration in 30 seconds')
  timer = threading.Timer(30.0, update_image_data)
  timer.start()

  print('processing', len(imageData), 'images')
  
  #print_image_data(imageData)

  imagesInDb = graphqlclient.listImages()
  process_images(imagesInDb, imageData)
  # for imageObject in imageData:
  #   process_image(imagesInDb, imageObject)
  
  currentTime = datetime.now()
  print('ended at time:', currentTime.strftime('%H:%M:%S'))
  print('')
  print('===========================================')
  print('')

def print_image_data(imageData):
  print('')
  for imageObject in imageData:
    print('name: ', imageObject.name)
    print('digest: ', imageObject.digest)
    print('namespace: ', imageObject.namespace)
    print('node: ', imageObject.node)
    print('')

def process_images(imagesInDb, imageData):
  imagesToAdd = []
  for imageObject in imageData:
    if imageObject.name not in imagesInDb:
      imageToAdd = { "name": imageObject.name, "nodes": { "name": imageObject, "namespace": imageObject.namespace }}
      imagesToAdd.append(imageToAdd)
  graphqlclient.addImages(imagesToAdd)

def add_image(imagesInDb, imageObject):
  # if image is not in list of images returned from DB then add
  if imageObject.name not in imagesInDb:
    graphqlclient.addImage(imageObject.name, imageObject, imageObject.namespace)

def delete_image(imageObject):
  # execute graphql mutation for deleting the image from DB
  graphqlclient.deletedImageClient(imageObject.name, imageObject.namespace)


if __name__ == '__main__':
  main()