@echo off
title SportSpotServer
cd camerasmicroservice
start python runner.py
cd ../
cd managementbackend
start python appmanagement.py
cd ../
cd userbackend
start python appuserbackend.py
cd ../
cd UserFrontend/sport-spot-project
start npm run serve
cd ../../

