from functools import wraps
from flask import request, jsonify, current_app

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != current_app.config['API_KEY']:
            return jsonify({
                "status": "error",
                "data": None,
                "message": "401 Unauthorized: Invalid or missing API Key"
            }), 401
        return f(*args, **kwargs)
    return decorated_function
