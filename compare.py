import json
import sys
import requests

# Function to download and parse the JSON report
def download_and_parse_report(url):
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.text)

# URLs for the dependency check reports
develop_report_url = 'URL_FOR_DEVELOP_REPORT'
mr_report_url = 'URL_FOR_MR_REPORT'

try:
    develop_report = download_and_parse_report(develop_report_url)
    mr_report = download_and_parse_report(mr_report_url)

    develop_vulnerabilities = {v['CVE'] for v in develop_report.get('vulnerabilities', [])}
    mr_vulnerabilities = {v['CVE'] for v in mr_report.get('vulnerabilities', [])}

    # Find new vulnerabilities in MR that are not in develop
    new_vulnerabilities = mr_vulnerabilities - develop_vulnerabilities

    if new_vulnerabilities:
        print("New vulnerabilities found in MR:")
        for vuln in new_vulnerabilities:
            print(vuln)
        sys.exit(1)  # Exit with error code to block the merge

    else:
        print("No new vulnerabilities found in MR.")
        sys.exit(0)  # Exit successfully

except Exception as e:
    print(f"Error occurred: {e}")
    sys.exit(1)  # Exit with error code in case of any failure
