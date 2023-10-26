#!/bin/bash

kubectl apply \
	-f ./app-namespace.yml \
	-f ./pg-data-pv-pvc.yml \
	-f ./app-config.yml \
	-f ./pg-service.yml \
	-f ./pg-deployment.yml \
	-f ./app-service.yml \
	-f ./app-deployment.yml
