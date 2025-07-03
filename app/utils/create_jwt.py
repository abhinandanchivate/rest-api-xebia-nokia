  # Ensure that JWT is properly initialized in app/extensions.py
from datetime import datetime, timedelta
import jwt
from flask_jwt_extended import create_access_token
from flask import current_app

def create_jwt_token(user_id: int, email: str) -> str:
    return create_access_token(identity=str(user_id), additional_claims={"email": email}, expires_delta=timedelta(days=1))
    """
    Create a JWT token for the user.
    
    Args:
        user_id (int): The ID of the user.
        email (str): The email of the user.
        
    Returns:
        str: The generated JWT token.
    
    # Get the current time in UTC
    expiration_time = datetime.now() + timedelta(days=1)  # Token expires in 1 day

    payload = {
        'sub':str(user_id),  # 'sub' is a standard claim for the subject of the token
        'user_id': user_id,
        'email': email,
        'exp': expiration_time  # Set the expiration time for the token
    }
    
    # Generate the token using a secret key and the algorithm
    secret_key = current_app.config['SECRET_KEY']  # This should be stored in a config or environment 
    token = jwt.encode(payload, secret_key, algorithm="HS256")  # Encoding the token using HS256
    
    return token"""
