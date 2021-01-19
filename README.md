# image-service

![CI](https://github.com/uniq-app/image-service/workflows/CI/badge.svg)

## swagger

if enabled

[localhost:80/](localhost:80/)

## .env
    SERVER_NAME=localhost:5000 or just localhost or your domain or your IP
    STORAGE_PATH=path where images will be saved
    
    MONGO_INITDB_ROOT_USERNAME=username for admin user
    MONGO_INITDB_ROOT_PASSWORD=password fro admin user
    
    MONGO_HOST=hostname for mognodb
    MONGO_USER=username for mongodb
    MONGO_PASS=password for mongodb
    MONGO_DBNAME=database name
    
    MAX_CONTENT_LENGTH=max uploaded file size in MB

    REDIS_HOST=IP:port for redis
    REDIS_PASSWORD=set strong password for redis

    SWAGGER=True/False to enable/disable swagger
