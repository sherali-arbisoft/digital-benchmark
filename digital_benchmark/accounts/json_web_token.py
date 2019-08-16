from django.conf import settings

import json
import base64
import hmac
import hashlib

header = {
    'alg': 'HS256',
    'typ': 'JWT'
}

def get_jwt(payload):
    encoded_header = base64.urlsafe_b64encode(bytes(json.dumps(header), 'utf-8')).decode('utf-8').rstrip('=')
    encoded_payload = base64.urlsafe_b64encode(bytes(json.dumps(payload), 'utf-8')).decode('utf-8').rstrip('=')
    data = bytes(f"{encoded_header}.{encoded_payload}", 'utf-8')
    signature = hmac.new(bytes(settings.SECRET_KEY, 'utf-8'), msg=data, digestmod=hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')
    jwt = f"{encoded_header}.{encoded_payload}.{encoded_signature}"
    return jwt

def get_payload(jwt):
    encoded_payload = jwt.split('.')[1]
    decode_payload = base64.urlsafe_b64decode(encoded_payload + '=' * (-len(encoded_payload) % 4))
    return json.loads(decode_payload.decode('utf-8'))

def verify_signature(jwt):
    payload = get_payload(jwt)
    encoded_header = base64.urlsafe_b64encode(bytes(json.dumps(header), 'utf-8')).decode('utf-8').rstrip('=')
    encoded_payload = base64.urlsafe_b64encode(bytes(json.dumps(payload), 'utf-8')).decode('utf-8').rstrip('=')
    data = bytes(f"{encoded_header}.{encoded_payload}", 'utf-8')
    signature = hmac.new(bytes(settings.SECRET_KEY, 'utf-8'), msg=data, digestmod=hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode('utf-8').rstrip('=')
    return encoded_signature == jwt.split('.')[-1]