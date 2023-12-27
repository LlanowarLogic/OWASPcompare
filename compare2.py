import json
import sys

def read_report(file_path):
    """Read and parse the JSON report."""
    with open(file_path, 'r') as file:
        return json.load(file)

def get_critical_vulnerabilities(report):
    """Extract 'High' and 'Critical' vulnerabilities from the report."""
    return {
        item['name'] for item in report['dependencies']
        if any(vuln['severity'] in ['HIGH', 'CRITICAL'] for vuln in item.get('vulnerabilities', []))
    }

def compare_reports(merge_request_report, develop_report):
    """Compare two reports and return the vulnerabilities that are only in the merge request report."""
    mr_vulns = get_critical_vulnerabilities(merge_request_report)
    develop_vulns = get_critical_vulnerabilities(develop_report)

    return mr_vulns - develop_vulns

# File paths to the OWASP reports
merge_request_report_path = 'path/to/merge_request_report.json'
develop_report_path = 'path/to/develop_report.json'

# Read and parse reports
merge_request_report = read_report(merge_request_report_path)
develop_report = read_report(develop_report_path)

# Compare the reports
new_vulnerabilities = compare_reports(merge_request_report, develop_report)

if new_vulnerabilities:
    print("New high/critical vulnerabilities found in Merge Request:")
    for vuln in new_vulnerabilities:
        print(vuln)
    sys.exit(1)
else:
    print("No new high/critical vulnerabilities found.")
    sys.exit(0)


"""
To create a job that compares OWASP Dependency-Check reports between the Merge Request pipeline and the Develop branch in a GitLab project, we need to follow these steps:

    Setup OWASP Dependency-Check in the Pipelines: Ensure that OWASP Dependency-Check is integrated into both the "Develop" branch pipeline and the "Merge Request" pipeline.

    Generate and Store Reports: In both pipelines, generate reports in a format that can be easily parsed (like JSON or XML).

    Create a Comparison Script: Write a script in Python (or Bash) that compares the two reports. This script will look for vulnerabilities marked as "High" or "Critical" in the Merge Request report that are not present in the Develop report.

    Integrate the Script into the Merge Request Pipeline: Add a job in the Merge Request pipeline to execute this comparison script.

    Fail the Job on New High/Critical Vulnerabilities: If the script finds new high/critical vulnerabilities, it should exit with a non-zero status, causing the job to fail.

Here's a detailed breakdown of the Python script that can be used for comparing the two OWASP reports:
Python Script for Comparing OWASP Reports

    Read and Parse Reports: The script will read the OWASP reports from both the Merge Request and Develop pipelines. Assume these reports are in JSON format and accessible at specified file paths.

    Compare Vulnerabilities: The script will compare the vulnerabilities listed in both reports, focusing on those marked as "High" or "Critical".

    Output Differences: If there are vulnerabilities in the Merge Request report that are not in the Develop report, the script will list these vulnerabilities.

    Exit Status: The script will exit with a non-zero status if new high/critical vulnerabilities are found.
Integration into GitLab CI/CD

To integrate this script into the GitLab CI/CD pipeline:

    Store the Script in the Repository: Add this Python script to your GitLab repository.

    Update .gitlab-ci.yml: Create a new job in the .gitlab-ci.yml file that runs this script after the OWASP Dependency-Check job in the Merge Request pipeline.

    Handle Report Paths: Ensure that the paths to the OWASP reports (both for the Merge Request and Develop branches) are correctly set in the script or passed as arguments.

    Run the Job: When the Merge Request pipeline runs, it will execute this script after the OWASP Dependency-Check job. If new high/critical vulnerabilities are found, the job will fail, preventing the merge into the Develop branch.
"""
