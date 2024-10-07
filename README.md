
### Run
```
docker-compose down
docker-compose up --build
docker-compose up -d

# Check
http://127.0.0.1:5000
http://127.0.0.1:5000/api/items

=> Access the Jaeger UI by navigating to http://localhost:16686 in your web browser. 
```

### Test
```
docker-compose up -d mongodb  # Start MongoDB if it's not already running
docker-compose run --rm test

# Check MongoDB logs:
docker-compose ps
docker-compose logs mongodb

OR
docker-compose build  # Rebuild the images to include any changes
docker-compose up -d mongodb  # Start MongoDB
docker-compose run --rm test  # Run the tests


OR
docker-compose run --rm test mongo mongodb://mongodb:27017/testdb


OR
python3 api_post.py  # To test the POST request


# BDD Test:
docker-compose run --rm bdd-test
```

