# image-service

## .env
    SECRET_KEY=geenrate your own secret
    STORAGE_PATH=path where images will be saved
    
    MONGO_INITDB_ROOT_USERNAME=username for admin user
    MONGO_INITDB_ROOT_PASSWORD=password fro admin user
    
    MONGO_HOST=hostname for mognodb
    MONGO_USER=username for mongodb
    MONGO_PASS=password for mongodb
    MONGO_DBNAME=database name
    
    GUNICORN_LOG_LEVEL=debug
    
    MAX_CONTENT_LENGTH=max uploaded file size in MB

    REDIS_HOST=IP:port for redis