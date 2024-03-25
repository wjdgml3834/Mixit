#!/bin/bash 

#note, please install:
# az cli
# teraform/hascorp

#login into azure-only when running localy
az login
#az account set --subscription "b041359c-4888-49f2-ae7a-0ffe9a3af1bd"
az account set --subscription "7421d281-52e1-4c64-b11d-12ee02151732"
#create dir and copy files
uuidgenvar=$(uuidgen)
dirname=$(echo "deployment-$uuidgenvar")
mkdir ./$dirname
cp ./tf-files/* ./$dirname
#cd $dirname

#initilaising and deploying terraform
terraform -chdir=./$dirname init 
terraform -chdir=./$dirname validate
terraform -chdir=./$dirname plan
terraform -chdir=./$dirname apply -auto-approve

#deploying the flask website
cd /Flask.App
zip -r Flask-App.zip ./*
echo "going to sleep for 5 seconds to let everything load"
sleep 5s
az webapp deployment source config-zip --name "website-740144f4" --resource-group "mixit-740144f4" --src Flask-App.zip

