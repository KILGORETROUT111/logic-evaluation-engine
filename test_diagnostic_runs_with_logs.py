import subprocess
import os
from datetime import datetime

test_cases = {
    "Test 1 - Respiratory + Unknown": "cough, fatigue, joint pain",
    "Test 2 - Autoimmune Vector": "rash, fatigue, fever",
    "Test 3 - Minimal or Ambiguous": "nausea"
}

log_dir = "diagnostic_test_logs"
os.makedirs(log_dir, exist_ok=True)

for title, input_str in test_cases.items():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{log_dir}/{title.replace(' ', '_').replace('-', '').lower()}_{timestamp}.txt"
    result = subprocess.run(
        ["python", "run_diagnostic.py", "--input", input_str],
        capture_output=True,
        text=True
    )
    with open(log_filename, "w") as log_file:
        log_file.write(f"=== {title} ===\n")
        log_file.write(f"Timestamp: {timestamp}\n")
        log_file.write(f"Input: {input_str}\n\n")
        log_file.write(result.stdout)
    print(f"{title} logged to {log_filename}")
