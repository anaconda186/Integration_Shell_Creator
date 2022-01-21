import getpass
import xml.dom.minidom

import requests

from password_generator import generate_password
from webRequest import (
    create_custom_report,
    create_integration_system,
    create_ISSG,
    create_ISU,
)


def main():
    # TODO: Remove hardcode of creds
    credentials = {
        "username": input("Username: ") or "AWILL-IMPL",
        "password": getpass.getpass(prompt="Password: "),
        "tenant": input("Tenant: ") or "invisors_dpt1",
    }

    # TODO: Add input and Dict for different Data Centers
    wsdls = {
        "Integrations": f"https://wd2-impl-services1.workday.com/ccx/service/{credentials['tenant']}/Integrations/v38.0",
        "Core_Implementation_Service": f"https://wd2-impl-services1.workday.com/ccx/service/{credentials['tenant']}/Core_Implementation_Service/v23.2",
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
    template_file = open("./data_files/Integration_Templates.txt", "r")
    integration_templates = [(line.strip()) for line in template_file]
    template_file.close()

    while True:
        print(integration_templates)
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
            )

            if create_report_tf in ("Y", "N"):
                break
            else:
                print("That command was not recognized")

        # If they know the Data Source, Ask for the Data Source
        if create_report_tf == "Y":
            # Create list of Data Sources
            data_source_file = open("./data_files/Data_Sources.txt", "r")
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

            data_source_filter_file = open(
                "./data_files/Data_Sources_with_Filters.txt", "r"
            )
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
                data_filter_file = open("data_files/Data_Source_Filters.txt", "r")
                data_filter_list = {}
                for _ in data_filter_file:
                    _ = _.strip().split("\t")
                    data_filter_list[_[0]] = _[1]
                data_filter_file.close()

                integration["Filter"] = data_filter_list[data_source_filter]

        # If they don't know the Data source, create temporary report
        else:
            print("A temporary report will be created to load the integration")
            # integration["Data_Source"] = data_source_list["Workers for HCM Reporting"]
            # integration["Filter"] = "a413a552c8b110000b0468f8f9af002b"

        # Create Request
        request = create_custom_report(integration, credentials).strip("\n")
        header = {"content-type": "text/xml"}

        r = requests.post(
            wsdls["Core_Implementation_Service"], data=request, headers=header
        )

        # Parse Repsonse
        xml_response = xml.dom.minidom.parseString(r.text)
        if r.status_code == 200:
            print(r, " - ", r.reason)
            print(f"CRI {integration['Name']} was successfully placed in target tenant")
            ID = xml_response.getElementsByTagName("wd:ID")
            integration["ReportWID"] = ID[0].firstChild.data
        else:

            print(r, " - ", r.reason)
            print(
                f"Error: CRI {integration['Name']} could not be placed in target tenant"
            )
            print("Please check below for more information.")
            print("Request: ")
            print(xml.dom.minidom.parseString(request).toprettyxml(indent="   "))
            print("Response: ")
            print(xml_response.toprettyxml(indent="   "))
            close = input("Error: Hit enter to close.")
            exit(1)
        input("Continue?")
    else:
        input("No report needed. Continue?")

    # Create Integration System
    request = create_integration_system(integration, credentials).strip("\n")
    r = requests.post(wsdls["Integrations"], data=request, headers=header)

    if r.status_code == 200:
        print(r, " - ", r.reason)
        print(f"{integration['Name']} was successfully placed in target tenant")
    else:
        print(r, " - ", r.reason)
        print(f"Error: {integration['Name']} could not be placed in target tenant")
        print("Please check below for more information.")
        print("Request: ")
        print(xml.dom.minidom.parseString(request).toprettyxml(indent="   "))
        print("Response: ")
        print(xml.dom.minidom.parseString(r.text).toprettyxml(indent="   "))
        close = input("Error: Hit enter to close.")
        exit(1)
    input("Continue?")

    # Create ISU
    request = create_ISU(integration, credentials).strip("\n")
    r = requests.post(wsdls["Integrations"], data=request, headers=header)

    if r.status_code == 200:
        print(r, " - ", r.reason)
        print(
            f"ISU {integration['Name']} was successfully created and attached to Integration"
        )
        integration["ISU"] = "ISU " + integration["Name"]
    else:
        print(r, " - ", r.reason)
        print(f"Error: ISU {integration['Name']} could not be placed in target tenant")
        print("Please check below for more information.")
        print("Request: ")
        print(xml.dom.minidom.parseString(request).toprettyxml(indent="   "))
        print("Response: ")
        print(xml.dom.minidom.parseString(r.text).toprettyxml(indent="   "))
        close = input("Error: Hit enter to close.")
        exit(1)
    input("Continue?")

    # Create ISSG
    request = create_ISSG(integration, credentials).strip("\n")
    r = requests.post(
        wsdls["Core_Implementation_Service"], data=request, headers=header
    )

    if r.status_code == 200:
        print(r, " - ", r.reason)
        print(
            f"ISSG {integration['Name']} was successfully created and attached to ISU"
        )
        integration["ISSG"] = "ISSG " + integration["Name"]
    else:
        print(r, " - ", r.reason)
        print(f"ISSG {integration['Name']} could not be created in target tenant")
        print("Please check the xml response for more information.")
        # xml.dom.minidom.parseString(r.text)
        print("Request: ")
        print(xml.dom.minidom.parseString(request).toprettyxml(indent="   "))
        print("Response: ")
        print(xml.dom.minidom.parseString(r.text).toprettyxml(indent="   "))
        close = input("Error: Hit enter to close.")
        exit(1)

    print(integration)
    input("End Script?")


if __name__ == "__main__":
    main()
