#!/bin/bash

cp version ./helm/version

helm upgrade --install --create-namespace -n dockwork dockwork ./helm/ -f ./helm/values.yaml

rm ./helm/version