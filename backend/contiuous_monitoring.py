# continuous_monitoring.py

from risk_engine import calculate_risk
from authorization import authorize


def monitor_agent(agent):

    risk, level = calculate_risk(
        agent["identity_risk"],
        agent["device_risk"],
        agent["behaviour_risk"],
        agent["network_risk"],
        agent["resource_risk"]
    )

    decision = authorize(
        level,
        agent["resource_sensitivity"]
    )

    return {
        "agent": agent["name"],
        "risk": risk,
        "risk_level": level,
        "decision": decision["decision"],
        "permission": decision["permission"]
    }


# Normal agent
agent = {
    "name": "CustomerSupport-Agent",

    "identity_risk": 5,
    "device_risk": 5,
    "behaviour_risk": 5,
    "network_risk": 5,
    "resource_risk": 5,

    "resource_sensitivity": "HIGH"
}

print("NORMAL ACTIVITY")
print(monitor_agent(agent))


# Suspicious behaviour
agent["behaviour_risk"] = 35
agent["network_risk"] = 20

print("\nSUSPICIOUS ACTIVITY")
print(monitor_agent(agent))


# Severe compromise
agent["behaviour_risk"] = 50
agent["network_risk"] = 30

print("\nCRITICAL ACTIVITY")
print(monitor_agent(agent))