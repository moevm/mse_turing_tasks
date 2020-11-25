#! /bin/bash

sudo apt-get install npm python3

chmod +x server/startServer.sh client/startClient.sh dataBase/startMongo.sh

cd server 
./startServer.sh &
cd ../client 
./startClient.sh &
cd ../dataBase 
./startMongo.sh &
cd ..
