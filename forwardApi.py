#!/usr/bin/python

# import Python packages

import requests
from requests.auth import HTTPBasicAuth
import argparse
import json


# import functions modules
from properties import FWD_URL, USERNAME, PASSWORD

headers = {"accept": "application/json"}
fwd_auth = HTTPBasicAuth(USERNAME, PASSWORD)

# Disable insecure https warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def parse_common_arguments():
    """
    Parse and return command-line arguments common to all the APIs
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        default=FWD_URL,
        help="The URL of a Forward Networks instance, e.g. https://fwd.app.",
    )
    parser.add_argument(
        "--username",
        "-u",
        default=USERNAME,
        help="The username of an account on the above-specified "
        "Forward Networks instance.",
    )
    parser.add_argument(
        "--password",
        "-p",
        default=PASSWORD,
        help="The password of an account on the above-specified "
        "Forward Networks instance.",
    )
    return parser


def get_api(url):
    """
    REST GET method
    """
    response = requests.get(url, auth=fwd_auth, headers=headers, verify=False)
    return response.json()
