from datetime import datetime, timezone
from pathlib import Path

print("Security Log Analyzer")
print("----------------------")

# Find all log files
log_folder = Path("sample_logs")
log_files = list(log_folder.glob("*.log"))

print(f"Found {len(log_files)} log files:")

for log_file in log_files:
    print(log_file)

# Read all log files
logs = []

for log_file in log_files:
    with open(log_file, "r") as file:
        for line in file:
            logs.append((log_file.name, line))

print(f"Total log entries: {len(logs)}")

# Find failed login attempts
failed_logins = []

for source_file, log in logs:
    if "LOGIN_FAILED" in log:
        failed_logins.append((source_file, log))

print(f"Failed login attempts: {len(failed_logins)}")

# Count failed login attempts by IP address
ip_attempts = {}

for source_file, log in failed_logins:
    parts = log.split()

    for part in parts:
        if part.startswith("ip="):
            ip_address = part.replace("ip=", "")

            if ip_address in ip_attempts:
                ip_attempts[ip_address] += 1
            else:
                ip_attempts[ip_address] = 1

print("\nFailed Attempts by IP:")
print("----------------------")

for ip, attempts in ip_attempts.items():
    print(f"{ip}: {attempts} failed attempts")

# Detect potentially suspicious IP addresses
print("\nPotentially Suspicious Activity:")
print("---------------------------------")

threshold = 3

for ip, attempts in ip_attempts.items():

    if attempts >= 5:
        severity = "HIGH"

        print(f"ALERT [{severity}]: {ip} has " f"{attempts} failed login attempts")

    elif attempts >= threshold:
        severity = "MEDIUM"

        print(f"ALERT [{severity}]: {ip} has " f"{attempts} failed login attempts")

# Count failed login attempts by username
username_attempts = {}

for source_file, log in failed_logins:
    parts = log.split()

    for part in parts:
        if part.startswith("username="):
            username = part.replace("username=", "")

            if username in username_attempts:
                username_attempts[username] += 1
            else:
                username_attempts[username] = 1

print("\nFailed Attempts by Username:")
print("----------------------------")

for username, attempts in username_attempts.items():
    print(f"{username}: {attempts} failed attempts")

# Detect successful logins after repeated failures
print("\nPossible Account Compromise:")
print("----------------------------")

failed_attempts_by_ip = {}

for source_file, log in logs:

    parts = log.split()

    username = None
    ip_address = None

    if "LOGIN_FAILED" in log:
        event = "LOGIN_FAILED"

    elif "LOGIN_SUCCESS" in log:
        event = "LOGIN_SUCCESS"

    else:
        event = None

    for part in parts:

        if part.startswith("username="):
            username = part.replace("username=", "")

        elif part.startswith("ip="):
            ip_address = part.replace("ip=", "")

    if event == "LOGIN_FAILED":

        if ip_address in failed_attempts_by_ip:
            failed_attempts_by_ip[ip_address] += 1

        else:
            failed_attempts_by_ip[ip_address] = 1

    elif event == "LOGIN_SUCCESS" and failed_attempts_by_ip.get(ip_address, 0) >= 3:

        print(
            f"WARNING: Successful login from {ip_address} "
            f"after repeated failed attempts against account "
            f"{username}"
        )

# Calculate risk information
suspicious_ips = 0
risk_score = 0

for ip, attempts in ip_attempts.items():

    if attempts >= 5:
        suspicious_ips += 1
        risk_score += 3

    elif attempts >= threshold:
        suspicious_ips += 1
        risk_score += 2

# Count possible account compromise events
compromise_events = 0

for source_file, log in logs:

    parts = log.split()
    ip_address = None

    for part in parts:

        if part.startswith("ip="):
            ip_address = part.replace("ip=", "")

    if "LOGIN_SUCCESS" in log and failed_attempts_by_ip.get(ip_address, 0) >= 3:
        compromise_events += 1
        risk_score += 5

# Assign overall risk rating
if risk_score >= 10:
    risk_rating = "HIGH"

elif risk_score >= 5:
    risk_rating = "MODERATE"

else:
    risk_rating = "LOW"

# Create reports directory if it does not exist
reports_folder = Path("reports")
reports_folder.mkdir(exist_ok=True)

# Create a unique timestamped report filename
report_time = datetime.now(timezone.utc)

report_filename = f"security_report_" f"{report_time.strftime('%Y-%m-%d_%H%M%S')}.txt"

report_path = reports_folder / report_filename

# Create security report
with open(report_path, "w") as report:

    report.write("SECURITY LOG ANALYSIS REPORT\n")
    report.write("============================\n\n")

    report.write(
        f"Report Generated: " f"{report_time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
    )

    # Log files analyzed
    report.write("Log Files Analyzed:\n")
    report.write("-------------------\n")

    for log_file in log_files:
        report.write(f"- {log_file.name}\n")

    report.write("\n")

    # Overall activity
    report.write(f"Total log entries: {len(logs)}\n")
    report.write(f"Failed login attempts: {len(failed_logins)}\n\n")

    # Failed attempts by IP
    report.write("Failed Attempts by IP:\n")
    report.write("----------------------\n")

    for ip, attempts in ip_attempts.items():
        report.write(f"{ip}: {attempts} failed attempts\n")

    # Suspicious IP addresses
    report.write("\nPotentially Suspicious Activity:\n")
    report.write("---------------------------------\n")

    for ip, attempts in ip_attempts.items():

        if attempts >= 5:
            severity = "HIGH"

            report.write(
                f"ALERT [{severity}]: {ip} has " f"{attempts} failed login attempts\n"
            )

        elif attempts >= threshold:
            severity = "MEDIUM"

            report.write(
                f"ALERT [{severity}]: {ip} has " f"{attempts} failed login attempts\n"
            )

    # Failed attempts by username
    report.write("\nFailed Attempts by Username:\n")
    report.write("----------------------------\n")

    for username, attempts in username_attempts.items():
        report.write(f"{username}: {attempts} failed attempts\n")

    # Possible account compromise
    report.write("\nPossible Account Compromise:\n")
    report.write("----------------------------\n")

    for source_file, log in logs:

        parts = log.split()

        username = None
        ip_address = None

        for part in parts:

            if part.startswith("username="):
                username = part.replace("username=", "")

            elif part.startswith("ip="):
                ip_address = part.replace("ip=", "")

        if "LOGIN_SUCCESS" in log and failed_attempts_by_ip.get(ip_address, 0) >= 3:
            report.write(
                f"WARNING: Successful login from {ip_address} "
                f"after repeated failed attempts against account "
                f"{username} (Source: {source_file})\n"
            )

    # Risk summary
    report.write("\nRisk Summary:\n")
    report.write("------------\n")

    report.write(f"IPs with failed login activity: " f"{len(ip_attempts)}\n")

    report.write(f"IPs exceeding failed-login threshold: " f"{suspicious_ips}\n")

    report.write(f"Possible account compromise events: " f"{compromise_events}\n")

    report.write(f"Overall risk score: {risk_score}\n")

    report.write(f"Overall risk rating: {risk_rating}\n")

    # Analyst conclusion
    report.write("\nAnalyst Conclusion:\n")
    report.write("------------------\n")

    if suspicious_ips > 0:

        report.write(
            "The log analysis identified multiple IP addresses "
            "with repeated failed login activity. "
            "Further investigation is recommended.\n"
        )

    else:

        report.write(
            "No IP addresses exceeded the failed-login threshold. "
            "No immediate suspicious activity was identified.\n"
        )

print(f"\nSecurity report created: {report_path}")
