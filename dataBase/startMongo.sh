#! /bin/bash

lsof -i:27017
sudo apt-get install mongodb
sudo service mongodb start
tail -n200 /var/log/mongodb/mongodb.log
sudo mongod
