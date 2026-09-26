# risk_engine.py

def calculate_risk(
    identity_risk,
    device_risk,
    behaviour_risk,
    network_risk,
    resource_risk
):

    total_risk = (
        identity_risk
        + device_risk
        + behaviour_risk
        + network_risk
        + resource_risk
    )

    total_risk = max(0, min(total_risk, 100))

    if total_risk <= 30:
        level = "LOW"

    elif total_risk <= 60:
        level = "MEDIUM"

    elif total_risk <= 80:
        level = "HIGH"

    else:
        level = "CRITICAL"

    return total_risk, level