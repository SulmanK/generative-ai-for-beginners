"""
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run()
```

suggest three improvements of the above code
"""

import logging
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

def sanitize_input(input_string):
    return re.sub(r'[^\w\s]', '', input_string)

def get_name():
    name = request.args.get('name', 'World')
    name = sanitize_input(name)
    if not name.isalpha():
        logging.error('Invalid name: %s', name)
        raise ValueError('Name must contain only alphabetic characters')
    return name

@app.route('/')
def hello():
    try:
        name = get_name()
        return f'Hello, {name}!'
    except ValueError as e:
        logging.error('Error processing request: %s', str(e))
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error('Internal server error: %s', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run()
