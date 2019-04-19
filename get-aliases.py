#!/usr/bin/python

"""
Python script to get and print Forward Aliases
"""

# import Python packages
import json

# import functions modules
from properties import FWD_URL, USERNAME, PASSWORD, SNAPSHOT_ID
from forwardApi import parse_common_arguments, get_api, headers, fwd_auth

ALIASES_set = {"HOSTS", "DEVICES", "INTERFACES", "HEADERS"}


def parse_aliases_arguments():
    """
    Parse common, add Aliases specific and return command-line arguments
    """
    parser = parse_common_arguments()
    parser.add_argument(
        "--snapshot-id", "-id", default=SNAPSHOT_ID, help="Snapshot ID"
    )
    parser.add_argument(
        "--alias_group",
        "-g",
        default="all",
        help="Available groups are HOSTS, DEVICES, INTERFACES, HEADERS. "
        "Default is all",
    )
    parser.add_argument(
        "--dump",
        "-d",
        dest="dump",
        action="store_true",
        help="Prints all JSON data",
    )
    args = parser.parse_args()
    return args


def get_aliases_url(base_url, id):
    """
    Build and return full Alias URL
    """
    url = base_url + "api/snapshots/" + str(id) + "/aliases"
    return url


def get_aliases(url):
    """
    Get the Aliases dictionary and return the Aliases list.
    """
    aliases_dictionary = get_api(url)
    print(type(aliases_dictionary["aliases"]))
    return aliases_dictionary["aliases"]


def print_aliases_group(aliases, group, dump):
    """
    Print a given <group> of Aliases.
    If dump is True, print the entire JSON data.
    If it's False, prints only the main data.
    """
    print("=== Group " + group + " ===")
    for alias in aliases:
        if alias["type"] == group:
            print("  Name: " + alias["name"])
            if dump:
                print(json.dumps(alias, sort_keys=True, indent=4))
            else:
                # Print if specific content exists for the given alias
                try:
                    alias["values"]
                except:
                    var_exists = False
                else:
                    print("  Values: ")
                    for value in alias["values"]:
                        print("        " + value)

                try:
                    alias["vlanIds"]
                except:
                    var_exists = False
                else:
                    print("  VLAN IDs: " + alias["vlanIds"])
                    print("  VLAN Interface Type: " + alias["vlanIntfTypes"])

                try:
                    alias["locations"]
                except:
                    var_exists = False
                else:
                    print("  Locations: ")
                    for value in alias["locations"]:
                        print("        " + value)


def print_aliases(aliases, my_group, dump):
    """
    Print a given group or all Aliases.
    """
    if my_group == "all":
        for group in ALIASES_set:
            print_aliases_group(aliases, group, dump)
    elif my_group in ALIASES_set:
        print_aliases_group(aliases, my_group, dump)
    else:
        print("There is no group named " + my_group)
        print("possible values are: ")
        for group in ALIASES_set:
            print(group)


def main():

    args = parse_aliases_arguments()
    url = get_aliases_url(args.url, args.snapshot_id)
    aliases = get_aliases(url)
    print_aliases(aliases, args.alias_group, args.dump)


if __name__ == "__main__":
    main()
