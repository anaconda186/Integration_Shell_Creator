def create_ISU(integration: dict, credentials: dict) -> str:
    request = f"""<?xml version="1.0" encoding="utf-8"?>
    <env:Envelope
        xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
        <env:Header>
            <wsse:Security env:mustUnderstand="1">
                <wsse:UsernameToken>
                    <wsse:Username>{credentials["username"]}@{credentials["tenant"]}</wsse:Username>
                    <wsse:Password
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{credentials["password"]}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
        </env:Header>
        <env:Body>
            <wd:Put_Integration_System_User_Request
                xmlns:wd="urn:com.workday/bsvc"
                wd:version="v36.2">
                <wd:Integration_System_Reference>
                    <wd:ID wd:type="Integration_System_ID">{integration["Name"].replace(' ','_')}</wd:ID>
                </wd:Integration_System_Reference>
                <wd:Integration_System_User_Data>
                    <wd:Integration_System_Reference>
                        <wd:ID wd:type="Integration_System_ID">{integration["Name"].replace(' ','_')}</wd:ID>
                    </wd:Integration_System_Reference>
                    <wd:User_Name>ISU {integration["Name"]}</wd:User_Name>
                    <wd:Password>{integration["Password"]}</wd:Password>
                    <wd:Require_New_Password_At_Next_Sign_In>false</wd:Require_New_Password_At_Next_Sign_In>
                    <wd:Session_Timeout_Minutes>10</wd:Session_Timeout_Minutes>
                    <wd:Do_Not_Allow_UI_Sessions>true</wd:Do_Not_Allow_UI_Sessions>
                </wd:Integration_System_User_Data>
            </wd:Put_Integration_System_User_Request>
        </env:Body>
    </env:Envelope>"""
    return request


def create_integration_system(integration: dict, credentials: dict) -> str:
    request = f"""<?xml version="1.0" encoding="utf-8"?>
    <env:Envelope
        xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
        <env:Header>
            <wsse:Security env:mustUnderstand="1">
                <wsse:UsernameToken>
                    <wsse:Username>{credentials["username"]}@{credentials["tenant"]}</wsse:Username>
                    <wsse:Password
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{credentials["password"]}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
        </env:Header>
        <env:Body>
            <wd:Put_Integration_System_Request
                xmlns:wd="urn:com.workday/bsvc"
                wd:Add_Only="false"
                wd:version="v36.2">
                <wd:Integration_System_Data>
                    <wd:Integration_System_ID>{integration["Name"].replace(' ','_')}</wd:Integration_System_ID>
                    <wd:Integration_System_Name>{integration["Name"]}</wd:Integration_System_Name>
                    <wd:Integration_Template_Reference>
                        <wd:ID wd:type="Integration_Template_Name">{integration["Template"]}</wd:ID>
                    </wd:Integration_Template_Reference>
                    {f'''<wd:Integration_Service_Data wd:Enabled="1">
                        <wd:Integration_Service_Reference>
                            <wd:ID wd:type="Workday_Integration_Service_Name">Document Retrieval Service</wd:ID>
                        </wd:Integration_Service_Reference>
                        <wd:Job_Integration_Retrieval_Configuration_Data>
                            <wd:Integration_Data_Source_Data>
                                <wd:Inbound_Protocol_Data>
                                    <wd:Custom_Report_Data_Source_Data>
                                        <wd:Custom_Report_Definition_Reference>
                                            <wd:ID wd:type = "WID">{integration["ReportWID"]}</wd:ID>
                                        </wd:Custom_Report_Definition_Reference>
                                    </wd:Custom_Report_Data_Source_Data>
                                </wd:Inbound_Protocol_Data>
                            </wd:Integration_Data_Source_Data>
                        </wd:Job_Integration_Retrieval_Configuration_Data>
                    </wd:Integration_Service_Data>
                    <wd:Integration_Service_Data wd:Enabled="1">
                        <wd:Integration_Service_Reference>
                            <wd:ID wd:type="Workday_Integration_Service_Name">Document Delivery Service</wd:ID>
                        </wd:Integration_Service_Reference>
                        <wd:Job_Integration_Delivery_Configuration_Data>
                            <wd:Integration_Transport_Protocol_Assignment_Data>
                                <wd:Integration_Transport_Protocol_Data>
                                    <wd:Workday_Attachment_Transport_Protocol_Data>
                                        <wd:Attach_To_Workday>true</wd:Attach_To_Workday>
                                    </wd:Workday_Attachment_Transport_Protocol_Data>
                                </wd:Integration_Transport_Protocol_Data>
                                <wd:Integration_File_Utility_Data>
                                    <wd:Filename>Change_This.csv</wd:Filename>
                                    <wd:Document_Retention_Policy>30</wd:Document_Retention_Policy>
                                </wd:Integration_File_Utility_Data>
                            </wd:Integration_Transport_Protocol_Assignment_Data>
                        </wd:Job_Integration_Delivery_Configuration_Data>
                </wd:Integration_Service_Data>''' if integration["Template"] == "Enterprise Interface Builder" else ''}
                {f'''<wd:Integration_Service_Data
                            wd:Enabled="1">
                            <wd:Integration_Service_Reference>
                                <wd:ID wd:type="Workday_Integration_Service_Name">Cloud Integration Broker</wd:ID>
                            </wd:Integration_Service_Reference>
                        </wd:Integration_Service_Data>''' if integration["Template"] == "Cloud Integration Template" else '' }
                </wd:Integration_System_Data>
            </wd:Put_Integration_System_Request>
        </env:Body>
    </env:Envelope>"""
    return request


# def create_integration_service(integration: dict, credentials: dict) -> str:
#     request = f"""<?xml version="1.0" encoding="utf-8"?>
#     <env:Envelope
#         xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
#         xmlns:xsd="http://www.w3.org/2001/XMLSchema"
#         xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
#         <env:Header>
#             <wsse:Security env:mustUnderstand="1">
#                 <wsse:UsernameToken>
#                     <wsse:Username>{credentials["username"]}@{credentials["tenant"]}</wsse:Username>
#                     <wsse:Password
#                         Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{credentials["password"]}</wsse:Password>
#                 </wsse:UsernameToken>
#             </wsse:Security>
#         </env:Header>
#         <env:Body>
#             <wd:Put_Integration_System_Request
#                 xmlns:wd="urn:com.workday/bsvc"
#                 wd:Add_Only="false"
#                 wd:version="v36.2">
#                 <wd:Integration_System_Data>
#                     <wd:Integration_System_Name>{integration["Name"]}</wd:Integration_System_Name>
#                     <wd:Integration_Template_Reference>
#                         <wd:ID wd:type="Integration_Template_Name">{integration["Template"]}</wd:ID>
#                     </wd:Integration_Template_Reference>
#                 </wd:Integration_System_Data>
#             </wd:Put_Integration_System_Request>
#         </env:Body>
#     </env:Envelope>"""
#     return request


def create_ISSG(integration: dict, credentials: dict) -> str:
    request = f"""<?xml version="1.0" encoding="utf-8"?>
    <env:Envelope
        xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
        <env:Header>
            <wsse:Security env:mustUnderstand="1">
                <wsse:UsernameToken>
                    <wsse:Username>{credentials["username"]}@{credentials["tenant"]}</wsse:Username>
                    <wsse:Password
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{credentials["password"]}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
        </env:Header>
        <env:Body>
            <wd:Put_Integration_System_Security_Group__Unconstrained__Request xmlns:wd="urn:com.workday/bsvc"
                wd:Add_Only="0" wd:version="v23.2">
                <wd:Integration_System_Security_Group__Unconstrained__Data wd:ID="ISSG_{integration["Name"].replace(' ','_')}">
                    <wd:Name>ISSG {integration["Name"]}</wd:Name>
                    <wd:Comment>Security Group for Integration with ID {integration["Name"].replace(' ','_')}</wd:Comment>
                    <wd:Inactive>0</wd:Inactive>
                    <wd:Integration_System_User_Reference>
                            <wd:ID wd:type="System_User_ID">ISU {integration["Name"]}</wd:ID>
                        </wd:Integration_System_User_Reference>
                </wd:Integration_System_Security_Group__Unconstrained__Data>
            </wd:Put_Integration_System_Security_Group__Unconstrained__Request>
        </env:Body>
    </env:Envelope>"""
    return request


def create_custom_report(integration: dict, credentials: dict) -> str:
    request = f"""<?xml version="1.0" encoding="utf-8"?>
    <env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
        <env:Header>
            <wsse:Security env:mustUnderstand="1">
                <wsse:UsernameToken>
                    <wsse:Username>{credentials["username"]}@{credentials["tenant"]}</wsse:Username>
                    <wsse:Password
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText"
                        >{credentials["password"]}</wsse:Password>
                </wsse:UsernameToken>
            </wsse:Security>
        </env:Header>
        <env:Body>
            <wd:Put_Tenanted_Report_Definition_Request wd:version="v22.1"
                xmlns:wd="urn:com.workday/bsvc">
                <wd:Tenanted_Report_Definition_Data
                    xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
                    <wd:Name>CRI {integration["Name"] if "Data_Source" in integration.keys() else "Temp Report DNU"}</wd:Name>
                    <wd:Tenanted_Report_Definition_System_User_Reference>
                        <wd:ID wd:type="System_User_ID">{credentials["username"]}</wd:ID>
                    </wd:Tenanted_Report_Definition_System_User_Reference>
                    <wd:Tenanted_Report_Definition_Type_Reference>
                        <wd:ID wd:type="Report_Type_ID">Advanced</wd:ID>
                    </wd:Tenanted_Report_Definition_Type_Reference>
                    <wd:Enable_As_Worklet>0</wd:Enable_As_Worklet>
                    <wd:Web_Service_API_Version_Reference>
                        <wd:ID wd:type="Version">v32.0</wd:ID>
                    </wd:Web_Service_API_Version_Reference>
                    <wd:Data_Source_Reference>
                        <wd:ID wd:type="WID">{integration["Data_Source"] if "Data_Source" in integration.keys() else "8143c64d478e49f7af08e027cbe9509f"}</wd:ID>
                    </wd:Data_Source_Reference>
                    {f'''<wd:Data_Source_Filter_Reference>
                        <wd:ID wd:type="WID">{integration["Filter"]}</wd:ID>
                    </wd:Data_Source_Filter_Reference>''' if 'Filter' in integration.keys() else ''}
                    <wd:Enable_Compare>0</wd:Enable_Compare>
                    <wd:Enable_Save_Parameters>0</wd:Enable_Save_Parameters>
                    <wd:Enforce_Web_Service_Validations>1</wd:Enforce_Web_Service_Validations>
                    <wd:Web_Service_Namespace_Suffix>urn:com.workday/bsvc</wd:Web_Service_Namespace_Suffix>           
                    <wd:Worklet_Max_Rows>0</wd:Worklet_Max_Rows>
                    <wd:Disable_All_Drilling>0</wd:Disable_All_Drilling>
                        <wd:Matrix_Enable_Drilling_to_Detail_Data>0</wd:Matrix_Enable_Drilling_to_Detail_Data>
                    <wd:Tenanted_Report_Worklet_Layout_Data>
                        <wd:Enable_as_Worklet>1</wd:Enable_as_Worklet>
                    </wd:Tenanted_Report_Worklet_Layout_Data>
                    <wd:Use_Specified_Facet_Sort>1</wd:Use_Specified_Facet_Sort>
                    <wd:Use_Specified_Dimension_Sort>0</wd:Use_Specified_Dimension_Sort>
                    <wd:Transpose_Left_Justify_Numerics>0</wd:Transpose_Left_Justify_Numerics>
                    <wd:Uses_Optional_Row_Effective_Date>0</wd:Uses_Optional_Row_Effective_Date>
                    <wd:Shared>0</wd:Shared>
                    <wd:Include_All_Time_Periods>0</wd:Include_All_Time_Periods>
                    <wd:Counter_for_Reference_ID>1</wd:Counter_for_Reference_ID>
                </wd:Tenanted_Report_Definition_Data>
            </wd:Put_Tenanted_Report_Definition_Request>
        </env:Body>
    </env:Envelope>"""
    return request


# <xsl:attribute name="wd:ID">ISSG_{integration["Name"].replace(' ','_')}</xsl:attribute>

# TODO: Add security domains to Security Group. Don't erase security for entire domain
