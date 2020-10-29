To install needed requirements you should type
    
    pip3 install -r requirements.txt


To run mongoDB server _script for linux_

    lsof -i:27017
    sudo apt-get install mongodb
    sudo service mongodb start
    tail -n200 /var/log/mongodb/mongodb.log
    
Or you can run bash-script

    bash ./startMongo.sh
