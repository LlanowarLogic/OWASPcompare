import json


def load_json(file_path):
    """
    loads JSON data from the file path.
    """
    with open(file_path, 'r') as file:
        return json.load(file)


def extract_vulnerabilities(data, severities):
    """
    extracts specified severity vulnerabilities from the given data.
    """
    vulnerabilities = []
    for dependency in data.get('dependencies', []):
        for vulnerability in dependency.get('vulnerabilities', []):
            severity = vulnerability.get('cvssv3', {}).get('baseSeverity', '').upper()
            if severity in severities:
                vulnerabilities.append((vulnerability.get('name'), severity))
    return vulnerabilities


def compare_vulnerabilities(branch_data, origin_data, severities):
    """
    compares vulnerabilities between branch and origin data and returns unique high and critical vulnerabilities in branch.
    """
    branch_vulnerabilities = set(extract_vulnerabilities(branch_data, severities))
    origin_vulnerabilities = set(extract_vulnerabilities(origin_data, severities))
    unique_branch_vulnerabilities = branch_vulnerabilities - origin_vulnerabilities
    return list(unique_branch_vulnerabilities)


# load the JSON files for 'branch' and 'origin' data
branch_data = load_json('OWASP_mr_compare_test-dependency-vulnerability-report.json')
origin_data = load_json('develop-dependency-vulnerability-report.json')

# specify severities to compare
sev_compare = ['HIGH', 'CRITICAL']

unique_high_and_critical_vulnerabilities = compare_vulnerabilities(branch_data, origin_data, sev_compare)

for vuln, severity in unique_high_and_critical_vulnerabilities:
    nvst_url = f"https://nvd.nist.gov/vuln/detail/{vuln}"
    print(f"{vuln} (Severity: {severity})\n{nvst_url}\n")
