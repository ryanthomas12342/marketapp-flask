from market import datetime,timedelta,jwt,app


def create_jwt_token(user_id):
    payload={
        'user_id':user_id,
       'exp':datetime.utcnow() + timedelta(hours=1)
    }

    token=jwt.encode(payload,app.config['SECRET_KEY'],algorithm='HS256')
    return token

def verify_jwt_token(token):
    """
    Verify and decode a JWT token.
    """
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
