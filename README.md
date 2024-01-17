# cardx_fhir_testing2024
Introduction

This README provides instructions for setting up and using the Python script in the cardx_fhir_testing2024 GitHub repository. The cardx_fhir_testing script was developed by Noah Pierce for testing the Cardx server at the January 2024 FHIR Connectathon.
Prerequisites

    Python: Ensure Python is installed on your system. If not, download and install it from python.org.
    Pip: Python's package installer, usually included with Python.

Installation

    Clone or download the repository from GitHub.
    Navigate to the repository directory in your terminal or command prompt.
    Run pip install -r requirements.txt to install the necessary Python packages.

Configuration

    Go to the bottom of main.py and edit the configuration variables as needed.
    You'll need a directory for uploading files. Default is smbp_observation, but can be changed in the configuration variables.
    The URL might require a patient_id depending on the system you're interfacing with.

Usage

    Execute the script by uncommenting the lines corresponding to the functions you want to use and running python main.py.
    To comment out or uncomment a line, use CTRL + '?' (this may vary depending on your text editor or IDE).

Note

For specific implementation details and troubleshooting, refer to the script comments or raise an issue in the GitHub repository.
