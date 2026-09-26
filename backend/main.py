from flask import Flask, request, jsonify
from flask_cors import CORS

from risk_engine import calculate_risk
from authorization import authorize
from credential_service import create_credential, verify_credential
from blast_radius import calculate_blast_radius
from isolation import generate_isolation_strategy


app = Flask(__name__)
CORS(app)


@app.route("/evaluate", methods=["POST"])
def evaluate():

    data = request.get_json(silent=True) or {}

    # ==============================
    # 1. INPUTS
    # ==============================

    agent_id = data.get(
        "agent",
        "CustomerSupport-Agent"
    )

    resource = data.get(
        "resource",
        "CustomerDB"
    )

    identity_risk = int(
        data.get("identity_risk", 5)
    )

    device_risk = int(
        data.get("device_risk", 5)
    )

    behaviour_risk = int(
        data.get("behaviour_risk", 5)
    )

    network_risk = int(
        data.get("network_risk", 5)
    )

    resource_risk = int(
        data.get("resource_risk", 5)
    )

    requested_permission = data.get(
        "permission",
        "READ_ONLY"
    )


    # ==============================
    # 2. RISK ENGINE
    # ==============================

    risk, risk_level = calculate_risk(
        identity_risk=identity_risk,
        device_risk=device_risk,
        behaviour_risk=behaviour_risk,
        network_risk=network_risk,
        resource_risk=resource_risk
    )


    # ==============================
    # 3. AUTHORIZATION
    # ==============================

    authorization_result = authorize(
        risk_level,
        resource
    )

    decision = authorization_result["decision"]

    granted_permission = authorization_result["permission"]


    # ==============================
    # 4. SHORT-LIVED CREDENTIAL
    # ==============================

    credential_valid = False
    credential_status = "NOT ISSUED"

    if decision == "ALLOW":

        token = create_credential(
            agent_id,
            resource,
            granted_permission,
            lifetime=300
        )

        verification = verify_credential(token)

        credential_valid = verification["valid"]

        if credential_valid:
            credential_status = "ACTIVE - 5 MINUTES"

    elif decision == "RESTRICT":

        token = create_credential(
            agent_id,
            resource,
            granted_permission,
            lifetime=120
        )

        verification = verify_credential(token)

        credential_valid = verification["valid"]

        if credential_valid:
            credential_status = "LIMITED - 2 MINUTES"

    elif decision == "RE-AUTHENTICATE":

        credential_status = "RE-AUTHENTICATION REQUIRED"

    else:

        credential_status = "REVOKED"


    # ==============================
    # 5. RESOURCE GRAPH
    # ==============================

    network = {

        "CustomerSupport-Agent": [
            "RESOURCE:CustomerDB",
            "RESOURCE:PublicAPI",
            "PaymentService"
        ],

        "PaymentService": [
            "RESOURCE:PaymentDB"
        ]
    }


    # ==============================
    # 6. BLAST RADIUS
    # ==============================

    affected_resources = calculate_blast_radius(
        network,
        agent_id
    )


    # ==============================
    # 7. ISOLATION STRATEGY
    # ==============================

    isolation = generate_isolation_strategy(
        risk_level,
        decision,
        affected_resources
    )


    # ==============================
    # 8. EXPLANATION
    # ==============================

    if risk_level == "LOW":

        explanation = (
            "Low-risk request. Identity, device, "
            "behaviour and network signals appear normal. "
            "Access can continue with minimum required privileges."
        )

    elif risk_level == "MEDIUM":

        explanation = (
            "Moderate risk detected. Access is allowed with "
            "reduced privileges and increased monitoring."
        )

    elif risk_level == "HIGH":

        explanation = (
            "High risk detected from the supplied context. "
            "Re-authentication is required before sensitive access continues."
        )

    else:

        explanation = (
            "Critical risk detected. Access should be revoked "
            "and the identity isolated to limit potential impact."
        )


    # ==============================
    # 9. FINAL RESPONSE
    # ==============================

    return jsonify({

        "success": True,

        "agent": agent_id,

        "resource": resource,

        "requested_permission": requested_permission,

        "risk": risk,

        "risk_level": risk_level,

        "decision": decision,

        "permission": granted_permission,

        "credential_valid": credential_valid,

        "credential_status": credential_status,

        "blast_radius": len(affected_resources),

        "affected_resources": affected_resources,

        "isolation": isolation,

        "explanation": explanation
    })


# ==============================
# SERVER START
# ==============================

if __name__ == "__main__":

    print("=" * 60)
    print("ZERO-TRUST AGENT SECURITY PLATFORM")
    print("=" * 60)
    print("Backend: http://127.0.0.1:5000")
    print("Endpoint: POST /evaluate")
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )