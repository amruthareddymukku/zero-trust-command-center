# credential_service.py

import jwt
import time

SECRET_KEY = "hackfusion-demo-secret"


def create_credential(agent_id, resource, permission, lifetime=300):

    current_time = int(time.time())

    payload = {
        "agent_id": agent_id,
        "resource": resource,
        "permission": permission,
        "issued_at": current_time,
        "expires_at": current_time + lifetime
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    return token


def verify_credential(token):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return {
            "valid": True,
            "data": payload
        }

    except jwt.ExpiredSignatureError:

        return {
            "valid": False,
            "reason": "Credential expired"
        }

    except jwt.InvalidTokenError:

        return {
            "valid": False,
            "reason": "Invalid credential"
        }