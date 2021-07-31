#!/bin/bash

export pwd=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo)
echo $pwd
argocd login localhost:8080 --username admin --password $pwd --grpc-web
