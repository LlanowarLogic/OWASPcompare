# OWASP compare

To achieve the goal of comparing OWASP dependency check reports between a Merge Request (MR) pipeline and the latest scan in the develop branch, the process involves several steps. First, we need to decide on the most efficient report format for comparison. Then, we can write a script to perform the comparison. Given the available formats (HTML, XML, CSV, JSON, JUNIT, SARIF, JENKINS, GITLAB), JSON is the most suitable for this task due to its structured, easily parsable nature, and widespread support in various programming languages, including Python.

Here is a Python script outline that would accomplish this task:

    Fetch Reports: The script must first download the latest dependency-check-report from the develop branch and the dependency-check-report from the MR.

    Parse JSON Reports: Load the reports using Python's JSON module.

    Compare Vulnerabilities: Iterate through the vulnerabilities in the MR report and compare them against those in the develop branch report. The script should focus on new vulnerabilities that are present in the MR report but not in the develop branch report.

    Merge Criteria: If new vulnerabilities are found in the MR report, the script should prevent the merge.

    Integration with GitLab CI/CD: This script should be set up as a job in the .gitlab-ci.yml file, running on MR events.


Note:

    Replace 'URL_FOR_DEVELOP_REPORT' and 'URL_FOR_MR_REPORT' with the actual URLs where the JSON reports are hosted.
    Ensure that the script has the necessary permissions to download reports from these URLs.
    You may need to adjust the parsing logic based on the exact structure of your JSON reports.
    This script assumes that each vulnerability has a unique 'CVE' identifier for comparison.
