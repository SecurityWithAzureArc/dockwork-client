#!/usr/bin/env python3

from osshim import osshim

class image:  

  def __init__(self, name, namespace, digest):      
    self.name=name                 
    self.namespace=namespace  
    self.digest=digest   
    self.node=osshim.get_hostname() 