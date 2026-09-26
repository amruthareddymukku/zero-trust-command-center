import streamlit as st
import pandas as pd
from supabase_client import supabase

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Zero Trust Command Center",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Zero Trust Command Center")
st.caption("AI Agent Identity & Privilege Fabric")


# =========================================================
# DATABASE FUNCTION
# =========================================================

def load_table(table_name):
    try:
        response = supabase.table(table_name).select("*").execute()

        data = response.data

        if data:
            return pd.DataFrame(data)

        return pd.DataFrame()

    except Exception as e:
        st.error(f"Error loading {table_name}: {e}")
        return pd.DataFrame()


# =========================================================
# LOAD ALL DATABASE TABLES
# =========================================================

resources = load_table("RESOURCES")
identities = load_table("Identities")
devices = load_table("devices")
access_decisions = load_table("access_decisions")
risk_assessments = load_table("risk_assessments")


# =========================================================
# SECURITY OVERVIEW
# =========================================================

st.header("📊 Security Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("👤 Identities", len(identities))

with col2:
    st.metric("💻 Devices", len(devices))

with col3:
    st.metric("📦 Resources", len(resources))

with col4:
    st.metric("🔐 Decisions", len(access_decisions))

with col5:
    st.metric("⚠️ Risk Assessments", len(risk_assessments))


# =========================================================
# RESOURCES TABLE
# =========================================================

st.divider()
st.header("📦 Protected Resources")

if not resources.empty:

    st.dataframe(
        resources,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning("No Resources found.")


# =========================================================
# IDENTITIES TABLE
# =========================================================

st.divider()
st.header("👤 AI Agent Identities")

if not identities.empty:

    st.dataframe(
        identities,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning("No Identities found.")


# =========================================================
# DEVICES TABLE
# =========================================================

st.divider()
st.header("💻 Devices")

if not devices.empty:

    st.dataframe(
        devices,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning("No Devices found.")


# =========================================================
# ACCESS DECISIONS TABLE
# =========================================================

if st.button("🧪 Test Supabase Save"):

    try:
        result = supabase.table("access_decisions").insert({
            "identity": "PaymentAgent",
            "resource": "Payment Database",
            "risk_score": 90,
            "decision": "REVOKED",
            "reason": "Critical risk detected",
            "action": "Credentials revoked"
        }).execute()

        st.success("✅ DATA SAVED TO SUPABASE")
        st.write(result.data)

    except Exception as e:
        st.error("❌ SUPABASE INSERT FAILED")
        st.code(str(e))
    


# =========================================================
# RISK ASSESSMENTS TABLE
# =========================================================

st.divider()
st.header("⚠️ Risk Assessments")

if not risk_assessments.empty:

    st.dataframe(
        risk_assessments,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning("No Risk Assessments")
    st.divider()
st.header("⚡ Access Evaluation")

agent = st.selectbox(
    "AI Agent",
    ["InvoiceAgent", "PaymentAgent", "SecurityAgent", "RobotAgent"]
)

device = st.selectbox(
    "Device State",
    ["Trusted", "Unknown", "Compromised"]
)

network = st.selectbox(
    "Network",
    ["Normal", "Suspicious", "High Risk"]
)

behaviour = st.selectbox(
    "Behaviour",
    ["Normal", "Abnormal", "Rapid Requests"]
)

if st.button("⚡ Evaluate Access"):

    risk = 0

    if device == "Unknown":
        risk += 25
    elif device == "Compromised":
        risk += 50

    if network == "Suspicious":
        risk += 20
    elif network == "High Risk":
        risk += 40

    if behaviour == "Abnormal":
        risk += 20
    elif behaviour == "Rapid Requests":
        risk += 30

    st.metric("Risk Score", f"{risk}%")

    if risk >= 60:
        st.error("🚫 ACCESS REVOKED")
    elif risk >= 30:
        st.warning("⚠️ ACCESS RESTRICTED")
    else:
        st.success("✅ ACCESS ALLOWED")
        st.subheader("🔄 Continuous Authorization")

st.write(
    "Access is continuously re-evaluated as the security context changes."
)

# Initial security state
initial_risk = st.slider(
    "Initial Risk Score",
    min_value=0,
    max_value=100,
    value=20
)

current_risk = st.slider(
    "Current Risk Score",
    min_value=0,
    max_value=100,
    value=20
)

if st.button("🔄 Re-evaluate Session"):

    if current_risk < 30:
        decision = "ALLOWED"
        action = "Privileges Maintained"

    elif current_risk < 60:
        decision = "RESTRICTED"
        action = "Privileges Reduced"

    elif current_risk < 80:
        decision = "RE-AUTHENTICATION REQUIRED"
        action = "Additional Verification Required"

    else:
        decision = "REVOKED"
        action = "Credentials Revoked"

    st.write("### Authorization Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Initial Risk", f"{initial_risk}%")

    with col2:
        st.metric("Current Risk", f"{current_risk}%")

    with col3:
        st.metric("Decision", decision)

    st.info(f"Action: {action}")

    if current_risk > initial_risk:
        st.warning(
            "⚠️ Risk increased during the session. "
            "Access privileges were dynamically updated."
        )
    elif current_risk < initial_risk:
        st.success(
            "✅ Risk decreased. Access can continue with the current context."
        )
    else:
        st.success("No significant risk change detected.")
        # -------------------------------------------------
# CREDENTIAL & BLAST RADIUS
# -------------------------------------------------

st.divider()
st.header("🔑 Credential & Blast Radius")

if st.button("🔐 Issue Credential"):

    if risk < 30:
        st.success("Credential Issued")
        st.info("⏱️ Valid for 5 minutes")
        st.write("Blast Radius: LOW")

    elif risk < 60:
        st.warning("Limited Credential Issued")
        st.info("⏱️ Valid for 2 minutes")
        st.write("Blast Radius: MEDIUM")

    else:
        st.error("Credential NOT Issued")
        st.write("Blast Radius: HIGH")
        st.warning("🚨 Identity should be isolated")
        st.subheader("🔑 Ephemeral Credential Service")

st.write(
    "Short-lived credentials are issued only for the current "
    "identity, device, task, resource and risk context."
)

credential_identity = st.text_input(
    "Identity / Agent",
    value="PaymentAgent"
)

credential_resource = st.text_input(
    "Protected Resource",
    value="Payment Database"
)

credential_task = st.text_input(
    "Task",
    value="Read Payment Records"
)

credential_risk = st.slider(
    "Credential Risk Score",
    0,
    100,
    20
)

credential_duration = st.selectbox(
    "Credential Validity",
    ["5 minutes", "10 minutes", "15 minutes"]
)

if st.button("🔑 Issue Ephemeral Credential"):

    if credential_risk >= 80:
        credential_status = "REJECTED"
        st.error("🚫 Credential not issued — Critical risk detected.")

    else:
        credential_id = "CRED-" + str(
            abs(hash(
                credential_identity +
                credential_resource +
                credential_task
            )))[:8]

        credential_status = "ACTIVE"

        st.success("✅ Ephemeral Credential Issued")

        st.write("### Credential Details")

        st.write(f"**Credential ID:** {credential_id}")
        st.write(f"**Identity:** {credential_identity}")
        st.write(f"**Resource:** {credential_resource}")
        st.write(f"**Task:** {credential_task}")
        st.write(f"**Risk Score:** {credential_risk}%")
        st.write(f"**Validity:** {credential_duration}")
        st.write(f"**Status:** {credential_status}")
        st.subheader("💥 Compromise Blast Radius Analysis")

st.write(
    "Estimate the resources and privilege paths that may be reachable "
    "if an identity is compromised."
)

blast_identity = st.selectbox(
    "Select Identity",
    [
        "PaymentAgent",
        "DataAgent",
        "AdminService",
        "RobotAgent"
    ]
)

blast_status = st.selectbox(
    "Identity Status",
    ["Normal", "Suspicious", "Compromised"]
)

if st.button("💥 Analyze Blast Radius"):

    if blast_status == "Compromised":

        if blast_identity == "PaymentAgent":
            resources = [
                "Payment Database",
                "Customer Database",
                "Payment API"
            ]

        elif blast_identity == "DataAgent":
            resources = [
                "Customer Database",
                "Analytics Database",
                "Cloud Storage"
            ]

        elif blast_identity == "AdminService":
            resources = [
                "User Database",
                "Cloud Storage",
                "Configuration Service",
                "Admin API"
            ]

        else:
            resources = [
                "Robot Control API",
                "Telemetry Database"
            ]

        reachable_count = len(resources)

        if reachable_count >= 4:
            blast_level = "CRITICAL"
        elif reachable_count >= 3:
            blast_level = "HIGH"
        else:
            blast_level = "MEDIUM"

        st.error(f"🚨 Blast Radius: {blast_level}")

        st.write("### Reachable Resources")

        for resource in resources:
            st.write(f"🔗 {resource}")

        st.write("### Privilege Path")

        st.code(
            f"{blast_identity} → "
            "Identity → Privileges → "
            "Reachable Resources"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Reachable Resources",
                reachable_count
            )

        with col2:
            st.metric(
                "Blast Radius",
                blast_level
            )

    else:
        st.success(
            "✅ No compromise detected. "
            "Normal access boundaries remain active."
        )
        st.subheader("🛡️ Compromise Isolation")

st.write(
    "Simulate containment of a compromised identity while "
    "keeping unaffected users and services operational."
)

isolation_identity = st.selectbox(
    "Compromised Identity",
    ["PaymentAgent", "DataAgent", "AdminService", "RobotAgent"],
    key="isolation_identity"
)

isolation_device = st.selectbox(
    "Device State",
    ["Trusted", "Suspicious", "Compromised"],
    key="isolation_device"
)

isolation_network = st.selectbox(
    "Network State",
    ["Normal", "Suspicious", "Malicious"],
    key="isolation_network"
)

if st.button("🛡️ Simulate Isolation"):

    if (
        isolation_device == "Compromised"
        or isolation_network == "Malicious"
    ):

        st.error("🚨 Compromise detected — containment initiated.")

        st.write("### Isolation Actions")

        actions = [
            "🔒 Identity isolated",
            "🔑 Active credentials revoked",
            "💻 Device quarantined",
            "🌐 Network access blocked",
            "📦 Sensitive resource access restricted"
        ]

        for action in actions:
            st.write(action)

        st.success(
            "✅ Unaffected users and services remain operational."
        )

        st.write("### Isolation Status")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Identity", "ISOLATED")

        with col2:
            st.metric("Device", "QUARANTINED")

        with col3:
            st.metric("Credentials", "REVOKED")

    else:

        st.success(
            "✅ No critical compromise detected. "
            "Isolation is not required."
        )
        st.subheader("📜 Auditable Decision Logs")

st.write(
    "Every authorization change is recorded with the reason "
    "and security action."
)

if "audit_logs" not in st.session_state:
    st.session_state.audit_logs = []

audit_identity = st.selectbox(
    "Identity",
    ["PaymentAgent", "DataAgent", "AdminService", "RobotAgent"],
    key="audit_identity"
)

audit_resource = st.selectbox(
    "Resource",
    [
        "Payment Database",
        "Customer Database",
        "Cloud Storage",
        "Robot Control API"
    ],
    key="audit_resource"
)

audit_risk = st.slider(
    "Risk Score",
    0,
    100,
    20,
    key="audit_risk"
)

if st.button("📝 Record Access Decision"):

    if audit_risk < 30:
        new_decision = "ALLOWED"
        reason = "Low risk and trusted security context"
        action = "Access maintained"

    elif audit_risk < 60:
        new_decision = "RESTRICTED"
        reason = "Elevated risk detected"
        action = "Privileges reduced"

    elif audit_risk < 80:
        new_decision = "RE-AUTHENTICATION"
        reason = "High risk requires additional verification"
        action = "Re-authentication required"

    else:
        new_decision = "REVOKED"
        reason = "Critical risk detected"
        action = "Credentials revoked"

    from datetime import datetime

    log = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Identity": audit_identity,
        "Resource": audit_resource,
        "Risk Score": f"{audit_risk}%",
        "Decision": new_decision,
        "Reason": reason,
        "Action": action
    }

    st.session_state.audit_logs.append(log)

    st.success("✅ Decision recorded in audit log.")

if st.session_state.audit_logs:

    st.write("### 📋 Decision History")

    st.dataframe(
        st.session_state.audit_logs,
        use_container_width=True
    )
else:
    st.info("No authorization changes recorded yet.")
st.subheader("🔄 Continuous Authorization")

st.write(
    "Access is continuously re-evaluated as the security context changes."
)

initial_risk = st.slider(
    "Initial Risk Score",
    min_value=0,
    max_value=100,
    value=20,
    key="initial_risk_continuous"
)

current_risk = st.slider(
    "Current Risk Score",
    min_value=0,
    max_value=100,
    value=20,
    key="current_risk_continuous"
)

if st.button("🔄 Re-evaluate Session", key="reevaluate_session"):

    # IMPORTANT: decision is calculated ONLY from current_risk
    if current_risk < 30:
        auth_decision = "ALLOWED"
        auth_action = "Privileges Maintained"

    elif current_risk < 60:
        auth_decision = "RESTRICTED"
        auth_action = "Privileges Reduced"

    elif current_risk < 80:
        auth_decision = "RE-AUTHENTICATION REQUIRED"
        auth_action = "Additional Verification Required"

    else:
        auth_decision = "REVOKED"
        auth_action = "Credentials Revoked"

    st.write("### Authorization Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Initial Risk",
            f"{initial_risk}%"
        )

    with col2:
        st.metric(
            "Current Risk",
            f"{current_risk}%"
        )

    with col3:
        st.metric(
            "Decision",
            auth_decision
        )

    st.info(f"Action: {auth_action}")

    if current_risk > initial_risk:

        st.warning(
            f"⚠️ Risk increased from {initial_risk}% "
            f"to {current_risk}%. Access privileges changed."
        )

    elif current_risk < initial_risk:

        st.success(
            f"✅ Risk decreased from {initial_risk}% "
            f"to {current_risk}%."
        )

    else:

        st.success(
            "Security context remains unchanged."
        )
    
        # -------------------------------------------------
# AI COPILOT
# -------------------------------------------------

st.divider()
st.header("✦ ZeroTrust AI Copilot")

question = st.text_input(
    "Ask about access, risk or security",
    placeholder="Can PaymentAgent access Payment Database?"
)

if st.button("🤖 ASK COPILOT"):

    q = question.lower()

    if "paymentagent" in q and "payment database" in q:
        st.info(
            "PaymentAgent can access Payment Database only "
            "when the device, network and behaviour are trusted."
        )

    elif "risk" in q:
        st.info(
            "Risk is calculated using device state, "
            "network context and historical behaviour."
        )

    elif "credential" in q:
        st.info(
            "Credentials are short-lived and issued only "
            "after successful authorization."
        )

    elif "resource" in q:
        st.info(
            f"The system currently monitors {len(resources)} protected resources."
        )

    else:
        st.info(
            "I can analyze access requests, risk, credentials and resources."
        )