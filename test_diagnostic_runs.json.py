import subprocess
import os
import json
from datetime import datetime

test_cases = {
    "Test 1 - Respiratory + Unknown": "cough, fatigue, joint pain",
    "Test 2 - Autoimmune Vector": "rash, fatigue, fever",
    "Test 3 - Minimal or Ambiguous": "nausea"
}

log_dir = "diagnostic_test_logs"
os.makedirs(log_dir, exist_ok=True)

for title, input_str in test_cases.items():
    timestamp = datetime.now().isoformat()
    short_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    input_list = [s.strip() for s in input_str.split(",")]

    # Call the Python diagnostic runner as a subprocess
    result = subprocess.run(
        ["python", "run_diagnostic.py", "--input", input_str],
        capture_output=True,
        text=True
    )

    # Build the JSON record from CLI output
    output_record = {
        "title": title,
        "timestamp": timestamp,
        "input": input_list,
        "output_raw": result.stdout.strip()
    }

    # Save JSON file
    filename = f"{log_dir}/{title.replace(' ', '_').replace('-', '').lower()}_{short_timestamp}.json"
    with open(filename, "w") as f:
        json.dump(output_record, f, indent=2)

    print(f"✅ {title} written to {filename}")
