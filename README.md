# Bookstore    
 RESTFul API for managing book data    
  
## Technology stack
 - Python as programming language
 - Postgresql for data store  
 - Docker for setup integration test environment    
    
## Run service  

 Requirements:
 - Python 3.6+
 - pip
 - Docker
 - Postgresql 9
 
 Required environment variable:
 - DB_HOST: database host name
 - DB_PASSWORD: database password
 - DB_PORT: database port number
 - DB_USER: database user name

run command to start postgresql container

    docker run --name postgres -e POSTGRES_PASSWORD=pingu123 -e POSTGRES_DB=bookstore -p 5432:5432 -d postgres:9    

run command to install required library
    
    pip install -r requirements.txt

run command to start server(with hot reload option):

    uvicorn main:api --reload
    
OR just use docker-compose
    
    docker-compose up
    
API document will be available at

    http://localhost:8000/docs

## Integration test

    pip install -r requirements.txt
    ./run_test.sh