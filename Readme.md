# Yousician Test 
Marc Siquier Penyafort   
marcsiquierpenyafort@gmail.com

### Installing Required Packages:

``` sudo pip install -r requirements.txt```

### Installing MongoDB in Ubuntu:

[Here you can find tutorials for other Platforms](https://docs.mongodb.com/v3.4/installation/#tutorials)

1. Import the public key used by the package management system.  
```sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6```

2. Create a list file for MongoDB.   
```echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list```

3. Reload local package database.   
```sudo apt-get update```

4. Install the MongoDB packages.   
```sudo apt-get install -y mongodb-org```

5. Start MongoDB   
```sudo service mongod start```

### Run Server.py
```
usage: server.py [-h] [-P SERVER_PORT]

Yousician Server

optional arguments:
  -h, --help      show this help message and exit
  -P SERVER_PORT  Server Listening Port
 ```

### Run Test.py
```
usage: test.py [-h] [-H HOSTNAME] [-P PORT]

Yousician api test

optional arguments:
  -h, --help   show this help message and exit
  -H HOSTNAME
  -P PORT
```
