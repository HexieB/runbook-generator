import os
import json
import argparse
import glob
from google import genai
from google.genai import errors

# Validate architecture environments
if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("CRITICAL: Environment key (GEMINI_API_KEY) missing from runtime context.")

client = genai.Client()

def parse_cli_arguments():
    """Configures CLI input processing for log ingestion."""
    parser = argparse.ArgumentParser(description="Automated IT Runbook & Playbook Generator Pipeline.")
    parser.add_argument(
        "--src",
        type=str,
        help="Path to an incident JSON log or a full directory of incident logs.",
        default=None
    )
    return parser.parse_args()

def determine_target_path(args):
    """Interactively resolves data target path if CLI arguments are bare."""
    if args.src:
        return args.src
    print("=== Automated Incident Runbook Pipeline ===")
    user_input = input("Enter log file or folder path (Leave blank for 'sample_incident_log.json'): ").strip()
    return user_input if user_input else "sample_incident_log.json"

def read_json_payload(file_path):
    """Ingests a target JSON error file."""
    resolved_path = os.path.abspath(os.path.expanduser(file_path))
    if not os.path.exists(resolved_path):
        raise FileNotFoundError(f"Source file not located at: {resolved_path}")
    with open(resolved_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Data Failure: {file_path} is corrupt or invalid JSON.")

def generate_markdown_runbook(log_data, file_name):
    """Orchestrates Gemini 2.5 to turn a raw error log into an enterprise SOP/Runbook."""
    prompt = f"""
    You are a Senior Infrastructure Engineer and Technical Documentation Master.
    Ingest the following raw incident log payload:
    
    {json.dumps(log_data, indent=2)}

    Generate a highly technical, production-ready Standard Operating Procedure (SOP) / Troubleshooting Runbook for the IT and Helpdesk engineering teams based on this error. 
    
    Output your text strictly in professional Markdown format using this exact schema:
    # RUNBOOK: [Insert Clear, Concise Title for the Incident/Error]
    ## Incident Reference ID: [Extract from log] | Target Platform: [Extract from log]
    ## 1. Problem Description & Root Cause Analysis (Deep dive into what this error actually means technically)
    ## 2. Immediate Triage & Containment Steps (Step-by-step terminal or console commands for a tier-1 engineer)
    ## 3. Long-Term Remediation & Patch Verification (How to permanently resolve and verify compliance)
    ## 4. End-User Communication Template (A short, professional message to drop to the affected user if their machine requires rebooting or isolation)
    """
    print(f"Orchestrating documentation generation for {file_name}...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

def write_runbook_to_disk(runbook_text, source_path):
    """Saves the output as a clean markdown file."""
    base_name = os.path.splitext(os.path.basename(source_path))[0]
    output_filename = f"SOP_{base_name}_remediation.md"
    with open(output_filename, "w") as f:
        f.write(runbook_text)
    print(f"[Success] Enterprise Runbook published flat to: {os.path.abspath(output_filename)}\n")

if __name__ == "__main__":
    try:
        arguments = parse_cli_arguments()
        raw_path = determine_target_path(arguments)
        target = os.path.abspath(os.path.expanduser(raw_path))
        
        # Batch directory loop logic
        if os.path.isdir(target):
            target_files = glob.glob(os.path.join(target, "*.json"))
            if not target_files:
                print(f"Notice: No target JSON log files found in directory {target}")
                exit(0)
            print(f"Directory Mode Active. Processing {len(target_files)} logs into runbooks...\n")
            for path in target_files:
                try:
                    data = read_json_payload(path)
                    sop_text = generate_markdown_runbook(data, os.path.basename(path))
                    write_runbook_to_disk(sop_text, path)
                except Exception as loop_error:
                    print(f"[Skip] Error with {os.path.basename(path)}: {str(loop_error)}")
        # Single file execution path
        else:
            data = read_json_payload(target)
            sop_text = generate_markdown_runbook(data, os.path.basename(target))
            write_runbook_to_disk(sop_text, target)
            
    except errors.APIError as api_err:
        print(f"GenAI Ingestion Failure: {api_err}")
    except Exception as error:
        print(f"\n[CRITICAL FAILURE] Pipeline halted: {str(error)}")
