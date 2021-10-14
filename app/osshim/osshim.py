#!/usr/bin/env python3

def get_hostname():
  with open("/hostdata/hostname", "r") as hostnamefile:
    hostname = hostnamefile.readline()
    return hostname