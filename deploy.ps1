#!/bin/pwsh

Copy-Item version ./helm/version

& helm upgrade --install --create-namespace -n dockwork dockwork ./helm/ -f ./helm/values.yaml

Remove-Item ./helm/version