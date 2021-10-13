#!/bin/bash

helm upgrade --install --create-namespace -n dockwork dockwork ./helm/ -f ./helm/values.yaml