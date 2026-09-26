async function evaluateAccess() {

    const agent = document.getElementById("agent").value;
    const resource = document.getElementById("resource").value;
    const device = document.getElementById("device").value;
    const network = document.getElementById("network").value;
    const behaviour = document.getElementById("behaviour").value;
    const task = document.getElementById("task").value;
    const accessLevel = document.getElementById("accessLevel").value;


    // ==============================
    // RISK VALUES
    // ==============================

    let deviceRisk = 5;
    let networkRisk = 5;
    let behaviourRisk = 5;
    let resourceRisk = 5;


    // DEVICE RISK

    if (device === "Unknown") {
        deviceRisk = 25;
    }

    if (device === "Compromised") {
        deviceRisk = 40;
    }


    // NETWORK RISK

    if (network === "Suspicious") {
        networkRisk = 25;
    }

    if (network === "High Risk Network") {
        networkRisk = 40;
    }


    // BEHAVIOUR RISK

    if (behaviour === "Abnormal") {
        behaviourRisk = 25;
    }

    if (behaviour === "Data Exfiltration Pattern") {
        behaviourRisk = 40;
    }


    // TASK RISK

    let taskRisk = 5;

    if (task === "Unusual") {
        taskRisk = 20;
    }

    if (task === "Critical Operation") {
        taskRisk = 30;
    }


    // RESOURCE RISK

    if (resource === "Payment Database") {
        resourceRisk = 20;
    }

    if (resource === "PaymentService") {
        resourceRisk = 25;
    }


    // ==============================
    // SEND TO BACKEND
    // ==============================

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/evaluate",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    agent: agent,

                    resource: resource,

                    identity_risk: 5,

                    device_risk: deviceRisk,

                    behaviour_risk:
                        behaviourRisk + taskRisk,

                    network_risk: networkRisk,

                    resource_risk: resourceRisk,

                    permission: accessLevel
                })
            }
        );


        // ==============================
        // CHECK RESPONSE
        // ==============================

        if (!response.ok) {

            throw new Error(
                "Backend returned HTTP " +
                response.status
            );
        }


        const result = await response.json();


        console.log(
            "ZERO-TRUST BACKEND RESPONSE:",
            result
        );


        // ==============================
        // RISK SCORE
        // ==============================

        document.getElementById(
            "riskScore"
        ).innerText = result.risk;


        // ==============================
        // DECISION
        // ==============================

        document.getElementById(
            "decision"
        ).innerText = result.decision;


        // ==============================
        // RISK LEVEL
        // ==============================

        const riskLevelElement =
            document.getElementById("riskLevel");

        if (riskLevelElement) {

            riskLevelElement.innerText =
                result.risk_level;
        }


        // ==============================
        // CREDENTIAL
        // ==============================

        const credentialElement =
            document.getElementById("credential");

        if (credentialElement) {

            credentialElement.innerText =
                result.credential_status;
        }


        // ==============================
        // PERMISSION
        // ==============================

        const permissionElement =
            document.getElementById("permissionStatus");

        if (permissionElement) {

            permissionElement.innerText =
                result.permission;
        }


        // ==============================
        // BLAST RADIUS
        // ==============================

        const blastRadiusElement =
            document.getElementById("blastRadius");

        if (blastRadiusElement) {

            if (result.blast_radius >= 3) {

                blastRadiusElement.innerText =
                    "HIGH";

            } else if (result.blast_radius > 0) {

                blastRadiusElement.innerText =
                    "MEDIUM";

            } else {

                blastRadiusElement.innerText =
                    "LOW";
            }
        }


        // ==============================
        // AFFECTED RESOURCES
        // ==============================

        const affectedElement =
            document.getElementById(
                "affectedResources"
            );

        if (affectedElement) {

            if (
                result.affected_resources &&
                result.affected_resources.length > 0
            ) {

                affectedElement.innerText =
                    result.affected_resources.join(", ");

            } else {

                affectedElement.innerText =
                    "None";
            }
        }


        // ==============================
        // IDENTITY
        // ==============================

        document.getElementById(
            "identityStatus"
        ).innerText = result.agent;


        // ==============================
        // DEVICE
        // ==============================

        document.getElementById(
            "deviceStatus"
        ).innerText = device;


        // ==============================
        // BEHAVIOUR
        // ==============================

        document.getElementById(
            "behaviourStatus"
        ).innerText = behaviour;


        // ==============================
        // NETWORK
        // ==============================

        document.getElementById(
            "networkStatus"
        ).innerText = network;


        // ==============================
        // ISOLATION STRATEGY
        // ==============================

        const isolationElement =
            document.getElementById(
                "isolationStrategy"
            );

        if (isolationElement) {

            isolationElement.innerText =
                result.isolation.level +
                " — " +
                result.isolation.action;
        }


        // ==============================
        // AI SECURITY EXPLANATION
        // ==============================

        const explanationElement =
            document.getElementById(
                "securityExplanation"
            );

        if (explanationElement) {

            explanationElement.innerText =
                result.explanation;
        }


        // ==============================
        // CONSOLE DETAILS
        // ==============================

        console.log(
            "Risk Score:",
            result.risk
        );

        console.log(
            "Risk Level:",
            result.risk_level
        );

        console.log(
            "Decision:",
            result.decision
        );

        console.log(
            "Permission:",
            result.permission
        );

        console.log(
            "Credential:",
            result.credential_status
        );

        console.log(
            "Blast Radius:",
            result.blast_radius
        );

        console.log(
            "Affected Resources:",
            result.affected_resources
        );

        console.log(
            "Isolation:",
            result.isolation
        );

    } catch (error) {

        console.error(
            "Evaluation Error:",
            error
        );

        alert(
            "Backend connection failed.\n\n" +
            "Make sure main.py is running on port 5000."
        );
    }
}
// ================= AI COPILOT =================

function addCopilotMessage(message, type = "bot") {
    const chat = document.getElementById("copilotChat");

    const div = document.createElement("div");
    div.className = type === "user" ? "user-message" : "bot-message";

    div.innerHTML = `
        <strong>${type === "user" ? "You" : "AI Copilot"}</strong>
        <p>${message}</p>
    `;

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}


function askCopilot() {

    const input = document.getElementById("copilotInput");
    const question = input.value.trim();

    if (!question) return;

    addCopilotMessage(question, "user");

    const q = question.toLowerCase();

    const allowedTopics = [
        "access",
        "risk",
        "credential",
        "resource",
        "agent",
        "device",
        "network",
        "identity",
        "zero trust",
        "authorization",
        "permission",
        "security",
        "paymentagent",
        "payment database"
    ];

    const isProjectQuestion = allowedTopics.some(
        topic => q.includes(topic)
    );

    let answer = "";

    if (!isProjectQuestion) {

        answer =
            "❌ I can only answer questions related to this Zero Trust security system.";

    } else if (
        q.includes("paymentagent") &&
        q.includes("payment database")
    ) {

        answer =
            "PaymentAgent can access the Payment Database only when identity, device, network and behaviour checks pass.";

    } else if (q.includes("risk")) {

        answer =
            "Risk is calculated from device state, network context and behaviour.";

    } else if (q.includes("credential")) {

        answer =
            "Credentials are short-lived and issued only after successful authorization.";

    } else if (q.includes("resource")) {

        answer =
            "Resources are protected according to their sensitivity and business criticality.";

    } else if (q.includes("device")) {

        answer =
            "Device trust is one of the factors used during access evaluation.";

    } else if (q.includes("network")) {

        answer =
            "Network context contributes to the overall risk score.";

    } else if (q.includes("identity") || q.includes("agent")) {

        answer =
            "Every AI agent must be verified before receiving access to a protected resource.";

    } else if (
        q.includes("access") ||
        q.includes("authorization") ||
        q.includes("permission")
    ) {

        answer =
            "Access is evaluated continuously using identity, device, network and behaviour context.";

    } else {

        answer =
            "I understand this is related to the Zero Trust system, but I don't have enough information to answer that specifically.";
    }

    setTimeout(() => {
        addCopilotMessage(answer, "bot");
    }, 300);

    input.value = "";
}

// ================= COPILOT ACTIONS =================

function openEvaluateAccess() {

    const agent = prompt(
        "Enter AI Agent name:",
        "PaymentAgent"
    );

    if (!agent) return;

    const resource = prompt(
        "Enter Resource name:",
        "Payment Database"
    );

    if (!resource) return;

    const device = prompt(
        "Device status (Trusted / Unknown / Compromised):",
        "Trusted"
    );

    if (!device) return;

    const network = prompt(
        "Network status (Normal / Suspicious / High Risk):",
        "Normal"
    );

    if (!network) return;

    let risk = 0;

    if (device.toLowerCase() === "unknown") risk += 25;
    if (device.toLowerCase() === "compromised") risk += 50;

    if (network.toLowerCase() === "suspicious") risk += 20;
    if (network.toLowerCase() === "high risk") risk += 40;

    let decision;

    if (risk >= 60) {
        decision = "🚫 ACCESS REVOKED";
    } else if (risk >= 30) {
        decision = "⚠️ ACCESS RESTRICTED";
    } else {
        decision = "✅ ACCESS ALLOWED";
    }

    addCopilotMessage(
        `<b>Access Evaluation</b><br>
        Agent: ${agent}<br>
        Resource: ${resource}<br>
        Device: ${device}<br>
        Network: ${network}<br>
        Risk Score: <b>${risk}%</b><br>
        Decision: <b>${decision}</b>`,
        "bot"
    );
}


function openAnalyzeRisk() {

    const device = prompt(
        "Device status (Trusted / Unknown / Compromised):",
        "Unknown"
    );

    if (!device) return;

    const network = prompt(
        "Network status (Normal / Suspicious / High Risk):",
        "Suspicious"
    );

    if (!network) return;

    const behaviour = prompt(
        "Behaviour (Normal / Abnormal / Rapid Requests):",
        "Abnormal"
    );

    if (!behaviour) return;

    let risk = 0;

    if (device.toLowerCase() === "unknown") risk += 25;
    if (device.toLowerCase() === "compromised") risk += 50;

    if (network.toLowerCase() === "suspicious") risk += 20;
    if (network.toLowerCase() === "high risk") risk += 40;

    if (behaviour.toLowerCase() === "abnormal") risk += 20;
    if (behaviour.toLowerCase() === "rapid requests") risk += 30;

    let result;

    if (risk >= 60) {
        result = "🚨 HIGH RISK";
    } else if (risk >= 30) {
        result = "⚠️ MEDIUM RISK";
    } else {
        result = "🟢 LOW RISK";
    }

    addCopilotMessage(
        `<b>Risk Analysis</b><br>
        Device: ${device}<br>
        Network: ${network}<br>
        Behaviour: ${behaviour}<br>
        Risk Score: <b>${risk}%</b><br>
        Result: <b>${result}</b>`,
        "bot"
    );
}