# Security Log Analyzer

## Overview

The Security Log Analyzer is a Python-based cybersecurity project designed to analyze authentication logs and identify potentially suspicious login activity.

The program searches through multiple log files, counts failed login attempts, analyzes activity by IP address and username, detects successful logins following repeated failures, calculates a risk score, and automatically generates a security analysis report.

This project was created as part of my cybersecurity portfolio to demonstrate practical scripting, log analysis, automation, security monitoring, and basic incident analysis skills.

## Project Goals

The primary goals of this project are to:

- Automate the analysis of authentication logs
- Identify repeated failed login attempts
- Track authentication activity by IP address
- Track failed login attempts by username
- Detect indicators of possible account compromise
- Assign severity levels to suspicious activity
- Calculate an overall risk score
- Generate security reports automatically
- Preserve previous reports for later review

## Technologies Used

- Python 3.13.2
- Visual Studio Code
- Python `pathlib`
- Python `datetime`
- Git
- GitHub
- Windows 11

## Project Structure

```text
Python_Security_Log_Analyzer
│
├── log_analyzer.py
├── README.md
│
├── reports
│   ├── security_report_2026-09-25_175455.txt
│   ├── security_report_2026-09-25_175519.txt
│   └── security_report_2026-09-25_182732.txt
│
├── sample_logs
│   ├── auth.log
│   └── auth2.log
│
└── screenshots
    ├── 01_project_structure.png
    ├── 02_sample_authentication_logs.png
    ├── 03_analyzer_execution.png
    └── 04_generated_security_report.png
```

## How It Works

The analyzer follows several stages when processing authentication logs.

### 1. Locate Log Files

The program searches the `sample_logs` directory for `.log` files.

```python
log_folder = Path("sample_logs")
log_files = list(log_folder.glob("*.log"))
```

This allows the analyzer to process multiple log files rather than depending on a single input file.

### 2. Read the Logs

The program reads each discovered log file and stores its entries for analysis.

Each entry retains the name of its source file so that findings in the generated security report can be associated with the appropriate log source.

### 3. Analyze Failed Login Attempts

The analyzer searches for `LOGIN_FAILED` events and counts failed authentication attempts.

Results are grouped by:

- IP address
- Username

This allows repeated authentication failures to be identified and provides information that could assist an analyst investigating suspicious login activity.

### 4. Identify Suspicious IP Addresses

The analyzer uses a threshold of three failed login attempts.

| Failed Attempts | Severity |
|---:|---|
| 0–2 | No alert |
| 3–4 | Medium |
| 5+ | High |

An alert is generated when an IP address reaches one of the defined thresholds.

### 5. Detect Possible Account Compromise

The analyzer identifies successful logins occurring after repeated failed login attempts from the same IP address.

For example:

```text
LOGIN_FAILED username=admin ip=10.0.0.25
LOGIN_FAILED username=admin ip=10.0.0.25
LOGIN_FAILED username=admin ip=10.0.0.25
LOGIN_SUCCESS username=admin ip=10.0.0.25
```

This pattern is flagged for further investigation because a successful authentication following repeated failures may warrant additional review.

### 6. Calculate Risk

The program assigns points based on detected activity.

The risk score considers:

- IP addresses exceeding the failed-login threshold
- Higher-volume failed login activity
- Possible account compromise events

The resulting score is translated into an overall risk rating.

| Risk Score | Rating |
|---:|---|
| 0–4 | LOW |
| 5–9 | MODERATE |
| 10+ | HIGH |

The score is intended as a basic project-specific method of prioritizing findings rather than a standardized industry risk model.

### 7. Generate Security Reports

After completing its analysis, the program automatically creates a timestamped report inside the `reports` directory.

Example:

```text
reports/security_report_2026-09-25_182732.txt
```

A new report is created each time the analyzer runs, allowing previous analysis results to be preserved.

Each report contains:

- Report generation time
- Log files analyzed
- Total log entries
- Total failed login attempts
- Failed attempts by IP address
- Failed attempts by username
- Suspicious activity alerts
- Possible account compromise events
- Overall risk score
- Overall risk rating
- Analyst conclusion

## Example Findings

Using the sample authentication logs included with this project, the analyzer identifies:

- Multiple IP addresses associated with failed login activity
- IP addresses exceeding the configured failed-login threshold
- Repeated authentication failures against user accounts
- Successful authentication following repeated failed attempts
- Authentication activity that may warrant additional investigation

These findings demonstrate how scripting can reduce the amount of manual log review required and help an analyst identify events that deserve closer examination.

## Skills Demonstrated

This project demonstrates practical experience with:

- Python scripting
- File handling
- Directory and file discovery
- Log parsing
- String processing
- Lists and dictionaries
- Loops
- Conditional logic
- Data aggregation
- Security event detection
- Basic risk scoring
- Automated report generation
- Authentication log analysis
- Security monitoring concepts
- Git version control
- GitHub project documentation

## Cybersecurity Concepts Demonstrated

The project applies several cybersecurity concepts, including:

- Authentication monitoring
- Repeated login-failure detection
- Indicators of possible account compromise
- IP-based activity analysis
- Security alerting
- Basic risk assessment
- Log-based investigation
- Security event monitoring

# Student Learning Outcome Alignment

This project is part of a larger cybersecurity portfolio intended to provide evidence of skills relevant to COMPSFI 212, COMPSFI 213, and COMPSFI 214.

The sections below identify only the learning outcomes for which this specific project provides relevant evidence. Additional portfolio projects are used to address outcomes not demonstrated by the Security Log Analyzer.

## COMPSFI 212 – Scripting for Cybersecurity

### SLO 1: Use scripting to automate routine tasks for reuse and efficiency

The program automates the repetitive task of reviewing multiple authentication log files. It discovers available `.log` files, processes their contents, identifies relevant security events, and produces results without requiring each file to be reviewed manually.

### SLO 2: Carry out automation of system processes via scripting and processing of their output

The script performs an automated workflow consisting of file discovery, file reading, event processing, data aggregation, detection logic, risk scoring, and report generation.

The output of the analysis is transformed into a structured security report that can be reviewed by an analyst.

### SLO 3: Use scripts to parse and analyze content of artifacts including log files

Authentication log analysis is the primary function of this project.

The program parses individual log entries, identifies `LOGIN_FAILED` and `LOGIN_SUCCESS` events, extracts usernames and IP addresses, counts repeated events, and analyzes the resulting data for suspicious authentication patterns.

### Additional Scripting Skills

The project also demonstrates use of Python libraries, data structures, loops, conditional statements, string processing, file operations, and automated output generation.

This project does not attempt to demonstrate every COMPSFI 212 Student Learning Outcome. Network programming, forensic scripting, cryptographic scripting, information gathering, and other scripting outcomes are addressed through separate portfolio work.

## COMPSFI 213 – Ethical Hacking

The Security Log Analyzer provides limited supporting evidence for COMPSFI 213 because its primary purpose is defensive log analysis rather than penetration testing or exploitation.

### SLO 1: Describe key issues facing network and security infrastructure defenses

The project demonstrates one security issue affecting authentication systems: repeated unauthorized login attempts.

By identifying repeated authentication failures and successful logins following suspicious activity, the project illustrates why authentication monitoring and review of security logs are important components of infrastructure defense.

### Supporting Ethical Hacking Concepts

The project provides exposure to defensive concepts associated with:

- Authentication attacks
- Repeated login attempts
- Basic indicators of possible brute-force activity
- Security monitoring
- Detection and investigation of suspicious authentication behavior

The project does not perform system exploitation, vulnerability scanning, malware analysis, packet sniffing, web application attacks, SQL injection, wireless attacks, or other offensive-security activities required by additional COMPSFI 213 outcomes. Those skills are demonstrated separately within the larger portfolio.

## COMPSFI 214 – Information Security Systems Analysis

### SLO 2: Analyze results of network reconnaissance using point-in-time data analysis, data correlation, analytics, logs and various tools data output

The project demonstrates log-based data analysis and correlation.

Authentication events from multiple log files are combined and analyzed by IP address and username. The program correlates repeated events to identify patterns that may require investigation.

The project specifically demonstrates the log-analysis and data-correlation portions of this learning outcome. Network reconnaissance analysis will be demonstrated through separate portfolio work.

### SLO 7: Determine the impact of incidents

The analyzer uses detected authentication activity to produce severity classifications and an overall project-specific risk score.

These results provide basic evidence of evaluating the potential significance of security events and prioritizing activity for further investigation.

This represents introductory incident-impact analysis rather than a complete incident response assessment.

### SLO 8: Use security information and event monitoring to identify and respond to security threats

This project provides relevant evidence for security event monitoring.

The analyzer reviews authentication events and identifies:

- Repeated failed authentication attempts
- IP addresses exceeding defined thresholds
- User accounts receiving repeated failed login attempts
- Successful authentication following suspicious failed-login activity

The generated report summarizes these findings and recommends further investigation when suspicious activity is identified.

### Supporting Information Security Analysis Skills

The project additionally demonstrates:

- Security log review
- Event correlation
- Threshold-based alerting
- Basic severity classification
- Risk prioritization
- Documentation of security findings
- Analyst-oriented reporting

Other COMPSFI 214 outcomes involving vulnerability management, security architecture, identity and access management remediation, security frameworks, compensating controls, and incident recovery are addressed through separate portfolio work.

## Future Improvements

Possible future improvements include:

- Supporting additional authentication log formats
- Adding command-line arguments
- Allowing analysts to specify custom thresholds
- Correlating events using defined time windows
- Strengthening correlation between username, IP address, and authentication sequence
- Exporting analysis results to CSV
- Adding graphical data visualization
- Adding automated notifications
- Integrating additional security log sources
- Supporting additional event types

## Disclaimer

The authentication logs used in this project are sample data created for educational, testing, and portfolio purposes. No real user credentials or sensitive production data are used.

# Project Evidence

The following screenshots demonstrate the organization, input data, execution, and output of the Security Log Analyzer.

## Project Structure

The project is organized into separate directories for sample authentication logs, generated security reports, screenshots, source code, and documentation.

![Project Structure](screenshots/01_project_structure.png)

## Sample Authentication Logs

Sample authentication logs contain successful and failed login events with usernames and IP addresses for the analyzer to process.

![Sample Authentication Logs](screenshots/02_sample_authentication_logs.png)

## Security Log Analyzer Execution

The Python script processes the authentication logs and identifies failed login activity, suspicious IP addresses, and possible account compromise events.

![Analyzer Execution](screenshots/03_analyzer_execution.png)

## Generated Security Report

After completing the analysis, the program automatically generates a timestamped security report containing detected activity, risk scoring, an overall risk rating, and an analyst conclusion.

![Generated Security Report](screenshots/04_generated_security_report.png)