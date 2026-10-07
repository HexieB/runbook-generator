# Automated IT Runbook & Playbook Generator

An operational CLI infrastructure utility that ingests machine-readable system logs, MDM patch failures (Jamf/Intune), CVE vulnerability scans, and network alerts, and dynamically orchestrates Gemini AI to generate structured, production-ready Standard Operating Procedures (SOPs) and troubleshooting runbooks for technical engineering teams.

## 🚀 Operations Value & Impact
* **Accelerates Documentation Lifecycles:** Instantly turns obscure compliance error codes into actionable documentation, closing security gaps faster.
* **Streamlines Tier-1 Helpdesk Workflows:** Empowers technicians with immediate, copy-pasteable terminal commands to remediate system drift.
* **Standardizes Fleet Health:** Bridges the documentation gap between DevOps, Security Operations, and IT Systems Administration.

## 🛠️ Step-by-Step Execution Guide

1. Clone the repository:
   ```bash
   git clone https://github.com
   cd automated-it-runbook-generator
   ```

2. Establish your isolated virtual environment layer:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Export your workspace Gemini credential token:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

4. Execute individual or batch directory processing:
   ```bash
   python generate_runbook.py
   ```
