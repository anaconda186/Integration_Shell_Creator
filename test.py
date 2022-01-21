import cProfile
import getpass
import time
import xml.dom.minidom
import argparse
import os.path
import requests

from password_generator import generate_password
from webRequest import (
    create_custom_report,
    create_integration_system,
    create_ISSG,
    create_ISU,
)


def main():
    INPUT_TXT = os.path.join(
        os.path.dirname(__file__), "data_files\\Integration_Templates.txt"
    )
    print(INPUT_TXT)
    template_file = open(INPUT_TXT, "r")
    integration_templates = [(line.strip()) for line in template_file]
    template_file.close()
    print(integration_templates)


if __name__ == "__main__":
    main()
