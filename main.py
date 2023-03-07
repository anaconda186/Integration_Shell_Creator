#!/usr/bin/env python

import getpass
from io import TextIOWrapper
import xml.dom.minidom
import os.path
import os
from time import sleep

import requests
from requests import Response

from gatherData import read_template
from password_generator import generate_password
from webRequest import (
    create_business_process,
    create_custom_report,
    create_integration_system,
    create_issg,
    create_isu,
)


credentials: dict[str, str] = {
    "username": input("Username: "),
    "password": getpass.getpass(prompt="Password: "),
    "tenant": input("Tenant: "),
    "dataCenter": input("Data Center: ").lower(),
}


def main():

    wsdls = {
        "Integrations": f"https://{credentials['dataCenter']}-impl-services1.workday.com/ccx/service/{credentials['tenant']}/Integrations/v38.0",
        "Core_Implementation_Service": f"https://{credentials['dataCenter']}-impl-services1.workday.com/ccx/service/{credentials['tenant']}/Core_Implementation_Service/v23.2",
    }
    integration = {}
    header = {"content-type": "text/xml"}
    # Integration Name
    integration["Name"] = input(
        "What is the INTEGRATION NAME (INTXXX INTEGRATION NAME)?"
    )

    # Generate Password for ISU
    integration["Password"] = generate_password()

    # Integration Template
    TEMPLATE_TXT = os.path.join(
        os.path.dirname(__file__), "data_files\\Integration_Templates.txt"
    )
    template_file = open(TEMPLATE_TXT, "r")
    integration_templates = [(line.strip()) for line in template_file]
    template_file.close()

    while True:
        # print(integration_templates)
        integration_template_name = input(
            "What INTEGRATION TEMPLATE would you like to create? "
        )
        if integration_template_name in integration_templates:
            print(f"INTEGRATION TEMPLATE: {integration_template_name} recognized.")
            break
        else:
            print(
                f"INTEGRATION TEMPLATE: {integration_template_name} was not recogized. Please confirm template."
            )
    integration["Template"] = integration_template_name

    # If EIB Create Custom Report
    if integration["Template"] == "Enterprise Interface Builder":
        # Ask if they know the data source for report
        while True:
            create_report_tf = input(
                "Do you know what DATA SOURCE you want to use for the Report? (Y or N) "
            ).upper()

            if create_report_tf in ("Y", "N"):
                break
            else:
                print("That command was not recognized")

        # If they know the Data Source, Ask for the Data Source
        if create_report_tf == "Y":
            # Create list of Data Sources
            DATA_SOURCE_TXT = os.path.join(
                os.path.dirname(__file__), "data_files\\Data_Sources.txt"
            )
            data_source_file = open(DATA_SOURCE_TXT, "r")
            data_source_list = {}
            for _ in data_source_file:
                _ = _.strip().split("\t")
                data_source_list[_[0]] = _[1]
            data_source_file.close()
            # Ask For Data Source Input
            while True:
                data_source = input("What DATA SOURCE would you like to use? ")
                if data_source in data_source_list:
                    print(f"\nDATA SOURCE: '{data_source}' confirmed.")
                    break
                else:
                    print(
                        f"\nDATA SOURCE: '{data_source}' was not recogized. Please confirm DATA SOURCE."
                    )
            integration["Data_Source"] = data_source_list[data_source]

            DATA_SOURCE_FILTER_TXT = os.path.join(
                os.path.dirname(__file__), "data_files\\Data_Sources_with_Filters.txt"
            )
            data_source_filter_file = open(DATA_SOURCE_FILTER_TXT, "r")
            data_source_filter_list = {}
            for _ in data_source_filter_file:
                _ = _.strip().split("\t")
                data_source_filter_list[_[0]] = _[1:]
            data_source_filter_file.close()

            # Check if Data Source needs filter
            if data_source_filter_list[data_source]:
                # Ask for Data Source Filter Input
                while True:
                    print("\n".join(data_source_filter_list[data_source]))
                    data_source_filter = input("\nWhich filter would you like to use? ")
                    if data_source_filter in data_source_filter_list[data_source]:
                        print(
                            f"\nDATA SOURCE FILTER: '{data_source_filter}' confirmed."
                        )
                        break
                    else:
                        print(
                            f"\nDATA SOURCE FILTER: '{data_source_filter}' was not recogized. Please confirm DATA SOURCE FILTER.\n"
                        )
                DATA_FILTER_TXT = os.path.join(
                    os.path.dirname(__file__), "data_files\\Data_Source_Filters.txt"
                )
                data_filter_file: TextIOWrapper = open(DATA_FILTER_TXT, "r")
                data_filter_list = {}
                for _ in data_filter_file:
                    _ = _.strip().split("\t")
                    data_filter_list[_[0]] = _[1]
                data_filter_file.close()

                integration["Filter"] = data_filter_list[data_source_filter]

        # If they don't know the Data source, create temporary report
        else:
            print("A temporary report will be created to load the integration")

        # Create Request
        request: str = create_custom_report(integration, credentials).strip("\n")
        header: dict[str, str] = {"content-type": "text/xml"}
        print("Putting Report...")
        r: Response = requests.post(
            wsdls["Core_Implementation_Service"], data=request, headers=header
        )

        # Parse Repsonse
        xml_response = xml.dom.minidom.parseString(r.text)
        # sleep(5)
        if r.status_code == 200:
            print(r, " - ", r.reason)
            print(f"CRI {integration['Name']} was successfully placed in target tenant")
            ID = xml_response.getElementsByTagName("wd:ID")
            integration["ReportWID"] = ID[0].firstChild.data

        else:
            response_error(r, request, integration, "Custom Report")
        input("Continue?")
    else:
        input("No report needed. Continue?")

    # Create Integration System
    request: str = create_integration_system(integration, credentials).strip("\n")
    print("Putting Integration...")
    r: Response = requests.post(wsdls["Integrations"], data=request, headers=header)
    # sleep(5)
    if r.status_code == 200:
        print(r, " - ", r.reason)
        print(f"{integration['Name']} was successfully placed in target tenant")

    else:
        response_error(r, request, integration, "Integration System")
    input("Continue?")

    # Create ISU
    request: str = create_isu(integration, credentials).strip("\n")
    print("Putting ISU...")
    r: Response = requests.post(wsdls["Integrations"], data=request, headers=header)
    sleep(2)
    if r.status_code == 200:
        print(r, " - ", r.reason)
        print(
            f"ISU {integration['Name']} was successfully created and attached to Integration"
        )
        integration["ISU"] = "ISU " + integration["Name"]

    else:
        response_error(r, request, integration, "ISU")
    input("Continue?")

    # Create ISSG
    request: str = create_issg(integration, credentials).strip("\n")
    print("Putting ISSG...")
    r: Response = requests.post(
        wsdls["Core_Implementation_Service"], data=request, headers=header
    )
    # sleep(5)
    if r.status_code == 200:
        print(r, " - ", r.reason)
        print(
            f"ISSG {integration['Name']} was successfully created and attached to ISU"
        )
        integration["ISSG"] = "ISSG " + integration["Name"]

    else:
        response_error(r, request, integration, "ISSG")
    input("Continue?")

    # Create Integration Business Process
    if integration["Template"] != "Enterprise Interface Builder":
        while True:
            create_retrieval_service_tf = input(
                "Do you want to configure a Retrieval Service? (Y/N)"
            ).upper()

            if create_retrieval_service_tf == "Y":
                create_retrieval_service_tf = True
                break
            elif create_retrieval_service_tf == "N":
                create_retrieval_service_tf = False
                break
            else:
                print("That command was not recognized")
        while True:
            create_delivery_service_tf = input(
                "Do you want to configure a Delivery Service? (Y/N)"
            ).upper()

            if create_delivery_service_tf == "Y":
                create_delivery_service_tf = True
                break
            elif create_delivery_service_tf == "N":
                create_delivery_service_tf = False
                break
            else:
                print("That command was not recognized")
        request = create_business_process(
            integration,
            credentials,
            create_retrieval_service_tf,
            create_delivery_service_tf,
        ).strip("\n")
        print("Putting Business Process...")
        r = requests.post(
            wsdls["Core_Implementation_Service"], data=request, headers=header
        )
        # sleep(5)
        if r.status_code == 200:
            print(r, " - ", r.reason)
            print(
                f"The Business Process was successfully created for {integration['Name']}"
            )
        else:
            response_error(r, request, integration, "Business Process")
        input("Continue?")

    print(integration)
    input("End Script?")
    os.system("cls" if os.name == "nt" else "clear")
    exit(0)


def response_error(response, request, integration_dict, component_name):
    print(response, " - ", response.reason)
    print(
        f"{component_name} for {integration_dict['Name']} could not be created in target tenant"
    )
    print("Please check the xml response for more information.")
    print("Request: ")
    # print(xml.dom.minidom.parseString(request).toprettyxml(indent="   "))
    print(request)
    print("Response: ")
    print(xml.dom.minidom.parseString(response.text).toprettyxml(indent="   "))
    input("Error: Hit enter to close.")
    os.system("cls" if os.name == "nt" else "clear")
    exit(1)


if __name__ == "__main__":
    main()
