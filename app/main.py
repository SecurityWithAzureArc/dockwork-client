#!/usr/bin/env python3

from containerdshim import containerdshim
from graphqlclient import graphqlclient
from data import image
import threading
from datetime import datetime
import time

def main():
  update_image_data()

  while True:
    time.sleep(300)

def update_image_data():
  imageData = containerdshim.list_images()

  print('starting image update process')
  currentTime = datetime.now()
  print('started at time:', currentTime.strftime('%H:%M:%S'))

  print('schedule next iteration in 30 seconds')
  timer = threading.Timer(30.0, update_image_data)
  timer.start()

  print('processing', len(imageData), 'images')
  
  print_image_data(imageData)

  #imagesInDb = graphql.listImagesQuery
  #for imageObject in imageData:
    #process_image(imagesInDb, imageObject)
  
  currentTime = datetime.now()
  print('ended at time:', currentTime.strftime('%H:%M:%S'))
  print('')
  print('===========================================')
  print('')

def print_image_data(imageData):
  print('')
  for imageObject in imageData:
    print('image to process - name: ', imageObject.name)
    print('                 - digest: ', imageObject.digest)
    print('                 - namespace: ', imageObject.namespace)
    print('                 - node: ', imageObject.node)
    print('')

def process_image(imagesInDb, imageObject):
  # if image is not in list of images returned from DB then add
  if imageObject.name not in imagesInDb:
    graphqlclient.addImage(imageObject.name, imageObject, imageObject.namespace)

def delete_image(imageObject):
  # execute graphql mutation for deleting the image from DB
  graphqlclient.deletedImageClient(imageObject.name, imageObject.namespace)


if __name__ == '__main__':
  main()