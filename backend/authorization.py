# authorization.py

def authorize(risk_level, resource_sensitivity):

    if risk_level == "LOW":
        return {
            "decision": "ALLOW",
            "permission": "READ_WRITE"
        }

    elif risk_level == "MEDIUM":
        return {
            "decision": "RESTRICT",
            "permission": "READ_ONLY"
        }

    elif risk_level == "HIGH":
        return {
            "decision": "RE-AUTHENTICATE",
            "permission": "READ_ONLY"
        }

    else:
        return {
            "decision": "REVOKE",
            "permission": "NO_ACCESS"
        }