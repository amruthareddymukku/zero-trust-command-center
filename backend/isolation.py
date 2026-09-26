# isolation.py

def generate_isolation_strategy(
    risk_level,
    decision,
    affected_resources
):

    if decision == "REVOKE" or risk_level == "CRITICAL":

        return {
            "level": "FULL ISOLATION",
            "action": "Revoke identity and terminate active sessions",
            "network": "Block network access",
            "resources": affected_resources,
            "monitoring": "Continuous security monitoring"
        }

    elif risk_level == "HIGH":

        return {
            "level": "STRICT ISOLATION",
            "action": "Require re-authentication",
            "network": "Restrict network access",
            "resources": affected_resources,
            "monitoring": "Enhanced monitoring"
        }

    elif risk_level == "MEDIUM":

        return {
            "level": "LIMITED ISOLATION",
            "action": "Reduce privileges",
            "network": "Allow trusted network only",
            "resources": affected_resources,
            "monitoring": "Continuous monitoring"
        }

    else:

        return {
            "level": "NORMAL MONITORING",
            "action": "Continue access with minimum privileges",
            "network": "Normal network access",
            "resources": affected_resources,
            "monitoring": "Standard monitoring"
        }