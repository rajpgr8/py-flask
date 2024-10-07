
### Run
```
docker-compose down
docker-compose up --build 
OR
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

### Python Best Practices
```

1. **Type Hints**: Added type hints to function arguments and return values for better code readability and IDE support.

2. **Docstrings**: Added detailed docstrings to each function, describing what the function does, its parameters, and return values.

3. **Consistent Return Types**: Ensured that all route handlers return a tuple of (response, status_code) for consistency.

4. **Error Handling**: Consistent error responses with appropriate HTTP status codes.

5. **Code Organization**: Grouped imports by standard library, third-party, and local imports.

6. **Environment Variables**: Using environment variables for configuration, with sensible defaults.

7. **Tracing**: Improved tracing by adding more context (tags) to spans.

8. **PEP 8 Compliance**: Ensured the code follows PEP 8 style guidelines for Python code.

9. **Explicit is better than implicit**: For example, explicitly returning status codes with all responses.

To further improve your project, consider the following:

1. **Configuration Management**: Use a configuration management library like `python-dotenv` for managing environment variables.

2. **Logging**: Implement proper logging throughout your application.

3. **Error Handling**: Implement global error handling to catch and log unexpected exceptions.

4. **Input Validation**: Use a library like `marshmallow` or `pydantic` for request data validation.

5. **API Documentation**: Consider using Swagger/OpenAPI for API documentation.

6. **Testing**: Expand your test coverage, including unit tests for individual functions.

7. **Asynchronous Operations**: If performance is a concern, consider using asynchronous libraries like `aiohttp` or `asyncio`.

These improvements make your code more readable, maintainable, and robust. They also make it easier for other developers to understand and contribute to your project.
```

### Flask Project Structure (Sample)
```
your_project/
│
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── views/
│   ├── templates/
│   ├── static/
│   └── utils/
│
├── config.py
├── requirements.txt
├── run.py
└── tests/
```
Here's a brief explanation of each component:   
1. app/: Main application package    
- __init__.py: Initializes the Flask app and brings together various components
- models/: Database models    
- views/: Route handlers and business logic      
- templates/: Jinja2 templates   
- static/: CSS, JavaScript, images, etc.   
- utils/: Helper functions and classes   
2. config.py: Configuration settings for different environments (development, testing, production)    
3. requirements.txt: List of Python dependencies   
4. run.py: Script to run the application   
5. tests/: Unit and integration tests   
