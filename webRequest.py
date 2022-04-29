from datetime import date


def create_isu(integration: dict, credentials: dict) -> str:
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


def create_integration_service(integration: dict, credentials: dict) -> str:
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
                    <wd:Integration_System_Name>{integration["Name"]}</wd:Integration_System_Name>
                    <wd:Integration_Template_Reference>
                        <wd:ID wd:type="Integration_Template_Name">{integration["Template"]}</wd:ID>
                    </wd:Integration_Template_Reference>
                </wd:Integration_System_Data>
            </wd:Put_Integration_System_Request>
        </env:Body>
    </env:Envelope>"""
    return request


def create_issg(integration: dict, credentials: dict) -> str:
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
                    <wd:Report_Tag_Reference>
                        <wd:ID wd:type="Custom_Report_Tag_ID">Integration</wd:ID>
                    </wd:Report_Tag_Reference>
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


def create_business_process(
    integration: dict,
    credentials: dict,
    create_retrieval_service_tf: bool,
    create_delivery_service_tf: bool,
) -> str:
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
            <wd:Put_Business_Process_Definition_Request
                wd:version="v35.0"
                xmlns:wd="urn:com.workday/bsvc">
                <wd:Business_Process_Definition_Data>
                    <wd:Business_Process_Definition_ID>BP_{integration["Name"].replace(' ','_')}</wd:Business_Process_Definition_ID>
                    <wd:Business_Process_Type_Reference>
                        <wd:ID wd:type="Business_Process_Type">Integration Process ID
                    </wd:ID>
                    </wd:Business_Process_Type_Reference>
                    <wd:Integration_System_Reference>
                        <wd:ID wd:type="Integration_System_ID">{integration["Name"].replace(' ','_')}</wd:ID>
                    </wd:Integration_System_Reference>
                    <wd:Rule_Based_Definition>0</wd:Rule_Based_Definition>
                    <wd:Effective_Date>{date.today()}</wd:Effective_Date>
                    <wd:Due_Date_Is_Based_On_Effective_Date>0</wd:Due_Date_Is_Based_On_Effective_Date>
                    <wd:Enable_Autocomplete>0</wd:Enable_Autocomplete>
                    <wd:Business_Process_Step_Data>
                        <wd:Order>a</wd:Order>
                        <wd:Dynamic_Parallel_Step>0</wd:Dynamic_Parallel_Step>
                        <wd:Completion_Step>0</wd:Completion_Step>
                        <wd:Business_Process_Step_Type_Reference>
                            <wd:ID wd:type="Workflow_Step_Type_ID">INITIATION</wd:ID>
                        </wd:Business_Process_Step_Type_Reference>
                        <wd:Optional_Step>0</wd:Optional_Step>
                        <wd:Asynchronous>0</wd:Asynchronous>
                        <wd:Due_Date_Is_Based_On_Effective_Date>0</wd:Due_Date_Is_Based_On_Effective_Date>
                        <wd:Process_by_All_in_Role>0</wd:Process_by_All_in_Role>
                        <wd:Disable_System_Notification>0</wd:Disable_System_Notification>
                    </wd:Business_Process_Step_Data>
                    {f'''
                    <wd:Business_Process_Step_Data>
                        <wd:Order>b</wd:Order>
                        <wd:Dynamic_Parallel_Step>0</wd:Dynamic_Parallel_Step>
                        <wd:Completion_Step>0</wd:Completion_Step>
                        <wd:Business_Process_Step_Type_Reference>
                            <wd:ID wd:type="Workflow_Step_Type_ID">SERVICE</wd:ID>
                        </wd:Business_Process_Step_Type_Reference>
                        <wd:Optional_Step>0</wd:Optional_Step>
                        <wd:Asynchronous>0</wd:Asynchronous>
                        <wd:Due_Date_Is_Based_On_Effective_Date>0</wd:Due_Date_Is_Based_On_Effective_Date>
                        <wd:Event_Service_Reference>
                            <wd:ID wd:type="Event_Service_Name">Document Retrieval</wd:ID>
                        </wd:Event_Service_Reference>
                        <wd:Document_Retrieval_Configuration_Data>
                            <wd:Document_Retention_Policy>30</wd:Document_Retention_Policy>
                            <wd:Integration_Data_Retrieval_Data>
                                <wd:Retrieval_File_Data>
                                    <wd:File_Name_Pattern>*.*</wd:File_Name_Pattern>
                                </wd:Retrieval_File_Data>
                                <wd:Transport_Protocol_Data>
                                    <wd:SFTP_Transport_Protocol_Data>
                                        <wd:SFTP_Address>sftp://change.me</wd:SFTP_Address>
                                        <wd:Directory>changeme</wd:Directory>
                                        <wd:Dual_Authentication>0</wd:Dual_Authentication>
                                        <wd:User_ID>changeme</wd:User_ID>
                                        <wd:Password>changeme</wd:Password>
                                        <wd:Use_Temp_File>0</wd:Use_Temp_File>
                                        <wd:Block_Size>32768</wd:Block_Size>
                                        <wd:Block_Size_Name>32K</wd:Block_Size_Name>
                                    </wd:SFTP_Transport_Protocol_Data>
                                </wd:Transport_Protocol_Data>
                                <wd:Restricted_To_Environment_Reference>
                                    <wd:ID wd:type="OMS_Environment_Type">IMPL</wd:ID>
                                </wd:Restricted_To_Environment_Reference>
                                <wd:Restricted_To_Environment_Reference>
                                    <wd:ID wd:type="OMS_Environment_Type">SANDBOX</wd:ID>
                                </wd:Restricted_To_Environment_Reference>
                                <wd:Decompress>0</wd:Decompress>
                                <wd:Delete_After_Retrieval>0</wd:Delete_After_Retrieval>
                            </wd:Integration_Data_Retrieval_Data>
                            <wd:Integration_Data_Retrieval_Data>
                                <wd:Retrieval_File_Data>
                                    <wd:File_Name_Pattern>*.*</wd:File_Name_Pattern>
                                </wd:Retrieval_File_Data>
                                <wd:Transport_Protocol_Data>
                                    <wd:SFTP_Transport_Protocol_Data>
                                        <wd:SFTP_Address>sftp://changeme</wd:SFTP_Address>
                                        <wd:Directory>changeme</wd:Directory>
                                        <wd:Dual_Authentication>0</wd:Dual_Authentication>
                                        <wd:User_ID>changeme</wd:User_ID>
                                        <wd:Password>changeme</wd:Password>
                                        <wd:Use_Temp_File>0</wd:Use_Temp_File>
                                        <wd:Block_Size>32768</wd:Block_Size>
                                        <wd:Block_Size_Name>32K</wd:Block_Size_Name>
                                    </wd:SFTP_Transport_Protocol_Data>
                                </wd:Transport_Protocol_Data>
                                <wd:Restricted_To_Environment_Reference>
                                    <wd:ID wd:type="OMS_Environment_Type">PROD</wd:ID>
                                </wd:Restricted_To_Environment_Reference>
                                <wd:Decompress>0</wd:Decompress>
                                <wd:Delete_After_Retrieval>0</wd:Delete_After_Retrieval>
                            </wd:Integration_Data_Retrieval_Data>
                        </wd:Document_Retrieval_Configuration_Data>
                        <wd:Process_by_All_in_Role>0</wd:Process_by_All_in_Role>
                        <wd:Disable_System_Notification>0</wd:Disable_System_Notification>
                    </wd:Business_Process_Step_Data>
                    ''' if create_retrieval_service_tf else ""}
                    <wd:Business_Process_Step_Data>
                        <wd:Order>{'c' if create_retrieval_service_tf else 'b'}</wd:Order>
                        <wd:Dynamic_Parallel_Step>0</wd:Dynamic_Parallel_Step>
                        <wd:Completion_Step>0</wd:Completion_Step>
                        <wd:Business_Process_Step_Type_Reference>
                            <wd:ID wd:type="Workflow_Step_Type_ID">SERVICE</wd:ID>
                        </wd:Business_Process_Step_Type_Reference>
                        <wd:Optional_Step>0</wd:Optional_Step>
                        <wd:Asynchronous>0</wd:Asynchronous>
                        <wd:Due_Date_Is_Based_On_Effective_Date>0</wd:Due_Date_Is_Based_On_Effective_Date>
                        <wd:Event_Service_Reference>
                            <wd:ID wd:type="Event_Service_Name">Fire Integration</wd:ID>
                        </wd:Event_Service_Reference>
                        <wd:Process_by_All_in_Role>0</wd:Process_by_All_in_Role>
                        <wd:Disable_System_Notification>0</wd:Disable_System_Notification>
                    </wd:Business_Process_Step_Data>
                    {f'''
                    <wd:Business_Process_Step_Data>
                        <wd:Order>c</wd:Order>
                        <wd:Dynamic_Parallel_Step>0</wd:Dynamic_Parallel_Step>
                        <wd:Completion_Step>0</wd:Completion_Step>
                        <wd:Business_Process_Step_Type_Reference>
                            <wd:ID wd:type="Workflow_Step_Type_ID">SERVICE</wd:ID>
                        </wd:Business_Process_Step_Type_Reference>
                        <wd:Optional_Step>0</wd:Optional_Step>
                        <wd:Asynchronous>0</wd:Asynchronous>
                        <wd:Due_Date_Is_Based_On_Effective_Date>0</wd:Due_Date_Is_Based_On_Effective_Date>
                        <wd:Event_Service_Reference>
                            <wd:ID wd:type="Event_Service_Name">Document Delivery</wd:ID>
                        </wd:Event_Service_Reference>
                        <wd:Document_Delivery_Configuration_Data>
                            <wd:Deliver_Documents_from_This_Event>1</wd:Deliver_Documents_from_This_Event>
                            <wd:Delivery_Attempts_Reference>
                                <wd:ID wd:type="Maximum_Limit">3</wd:ID>
                            </wd:Delivery_Attempts_Reference>
                            <wd:Integration_Data_Communication_Data>
                                <wd:Transport_Protocol_Data>
                                    <wd:SFTP_Transport_Protocol_Data>
                                        <wd:SFTP_Address>sftp://change.me</wd:SFTP_Address>
                                        <wd:Directory>changeme</wd:Directory>
                                        <wd:Dual_Authentication>0</wd:Dual_Authentication>
                                        <wd:User_ID>changeme</wd:User_ID>
                                        <wd:Password>changeme</wd:Password>
                                        <wd:Use_Temp_File>1</wd:Use_Temp_File>
                                        <wd:Block_Size>32768</wd:Block_Size>
                                        <wd:Block_Size_Name>32K</wd:Block_Size_Name>
                                    </wd:SFTP_Transport_Protocol_Data>
                                </wd:Transport_Protocol_Data>
                                <wd:Content_Data>
                                    <wd:Compressed>0</wd:Compressed>
                                    <wd:Use_Improved_Compression>0</wd:Use_Improved_Compression>
                                    <wd:Transfer_Acceleration_Enabled>0</wd:Transfer_Acceleration_Enabled>
                                </wd:Content_Data>
                                <wd:Restricted_To_Environment_Reference>
                                    <wd:ID wd:type="OMS_Environment_Type">IMPL</wd:ID>
                                </wd:Restricted_To_Environment_Reference>
                                <wd:Restricted_To_Environment_Reference>
                                    <wd:ID wd:type="OMS_Environment_Type">SANDBOX</wd:ID>
                                </wd:Restricted_To_Environment_Reference>
                            </wd:Integration_Data_Communication_Data>
                            <wd:Integration_Data_Communication_Data>
                                <wd:Transport_Protocol_Data>
                                    <wd:SFTP_Transport_Protocol_Data>
                                        <wd:SFTP_Address>sftp://change.me</wd:SFTP_Address>
                                        <wd:Directory>changeme</wd:Directory>
                                        <wd:Dual_Authentication>0</wd:Dual_Authentication>
                                        <wd:User_ID>changeme</wd:User_ID>
                                        <wd:Password>changeme</wd:Password>
                                        <wd:Use_Temp_File>1</wd:Use_Temp_File>
                                        <wd:Block_Size>32768</wd:Block_Size>
                                        <wd:Block_Size_Name>32K</wd:Block_Size_Name>
                                    </wd:SFTP_Transport_Protocol_Data>
                                </wd:Transport_Protocol_Data>
                                <wd:Content_Data>
                                    <wd:Compressed>0</wd:Compressed>
                                    <wd:Use_Improved_Compression>0</wd:Use_Improved_Compression>
                                    <wd:Transfer_Acceleration_Enabled>0</wd:Transfer_Acceleration_Enabled>
                                </wd:Content_Data>
                                <wd:Restricted_To_Environment_Reference>
                                    <wd:ID wd:type="OMS_Environment_Type">PROD</wd:ID>
                                </wd:Restricted_To_Environment_Reference>
                            </wd:Integration_Data_Communication_Data>
                        </wd:Document_Delivery_Configuration_Data>
                        <wd:Process_by_All_in_Role>0</wd:Process_by_All_in_Role>
                        <wd:Disable_System_Notification>0</wd:Disable_System_Notification>
                    </wd:Business_Process_Step_Data>
                    ''' if (create_delivery_service_tf and not(create_retrieval_service_tf)) else ""}
                    {f'''
                    <wd:Business_Process_Step_Data>
                        <wd:Order>d</wd:Order>
                        <wd:Dynamic_Parallel_Step>0</wd:Dynamic_Parallel_Step>
                        <wd:Completion_Step>0</wd:Completion_Step>
                        <wd:Business_Process_Step_Type_Reference>
                            <wd:ID wd:type="Workflow_Step_Type_ID">SERVICE</wd:ID>
                        </wd:Business_Process_Step_Type_Reference>
                        <wd:Optional_Step>0</wd:Optional_Step>
                        <wd:Asynchronous>0</wd:Asynchronous>
                        <wd:Due_Date_Is_Based_On_Effective_Date>0</wd:Due_Date_Is_Based_On_Effective_Date>
                        <wd:Event_Service_Reference>
                            <wd:ID wd:type="Event_Service_Name">Document Delivery</wd:ID>
                        </wd:Event_Service_Reference>
                        <wd:Document_Delivery_Configuration_Data>
                            <wd:Deliver_Documents_from_This_Event>1</wd:Deliver_Documents_from_This_Event>
                            <wd:Delivery_Attempts_Reference>
                                <wd:ID wd:type="Maximum_Limit">3</wd:ID>
                            </wd:Delivery_Attempts_Reference>
                            <wd:Integration_Data_Communication_Data>
                                <wd:Transport_Protocol_Data>
                                    <wd:SFTP_Transport_Protocol_Data>
                                        <wd:SFTP_Address>sftp://change.me</wd:SFTP_Address>
                                        <wd:Directory>changeme</wd:Directory>
                                        <wd:Dual_Authentication>0</wd:Dual_Authentication>
                                        <wd:User_ID>changeme</wd:User_ID>
                                        <wd:Password>changeme</wd:Password>
                                        <wd:Use_Temp_File>1</wd:Use_Temp_File>
                                        <wd:Block_Size>32768</wd:Block_Size>
                                        <wd:Block_Size_Name>32K</wd:Block_Size_Name>
                                    </wd:SFTP_Transport_Protocol_Data>
                                </wd:Transport_Protocol_Data>
                                <wd:Content_Data>
                                    <wd:Compressed>0</wd:Compressed>
                                    <wd:Use_Improved_Compression>0</wd:Use_Improved_Compression>
                                    <wd:Transfer_Acceleration_Enabled>0</wd:Transfer_Acceleration_Enabled>
                                </wd:Content_Data>
                                <wd:Restricted_To_Environment_Reference>
                                    <wd:ID wd:type="OMS_Environment_Type">IMPL</wd:ID>
                                </wd:Restricted_To_Environment_Reference>
                                <wd:Restricted_To_Environment_Reference>
                                    <wd:ID wd:type="OMS_Environment_Type">SANDBOX</wd:ID>
                                </wd:Restricted_To_Environment_Reference>
                            </wd:Integration_Data_Communication_Data>
                            <wd:Integration_Data_Communication_Data>
                                <wd:Transport_Protocol_Data>
                                    <wd:SFTP_Transport_Protocol_Data>
                                        <wd:SFTP_Address>sftp://change.me</wd:SFTP_Address>
                                        <wd:Directory>changeme</wd:Directory>
                                        <wd:Dual_Authentication>0</wd:Dual_Authentication>
                                        <wd:User_ID>changeme</wd:User_ID>
                                        <wd:Password>changeme</wd:Password>
                                        <wd:Use_Temp_File>1</wd:Use_Temp_File>
                                        <wd:Block_Size>32768</wd:Block_Size>
                                        <wd:Block_Size_Name>32K</wd:Block_Size_Name>
                                    </wd:SFTP_Transport_Protocol_Data>
                                </wd:Transport_Protocol_Data>
                                <wd:Content_Data>
                                    <wd:Compressed>0</wd:Compressed>
                                    <wd:Use_Improved_Compression>0</wd:Use_Improved_Compression>
                                    <wd:Transfer_Acceleration_Enabled>0</wd:Transfer_Acceleration_Enabled>
                                </wd:Content_Data>
                                <wd:Restricted_To_Environment_Reference>
                                    <wd:ID wd:type="OMS_Environment_Type">PROD</wd:ID>
                                </wd:Restricted_To_Environment_Reference>
                            </wd:Integration_Data_Communication_Data>
                        </wd:Document_Delivery_Configuration_Data>
                        <wd:Process_by_All_in_Role>0</wd:Process_by_All_in_Role>
                        <wd:Disable_System_Notification>0</wd:Disable_System_Notification>
                    </wd:Business_Process_Step_Data>
                    ''' if (create_delivery_service_tf and create_retrieval_service_tf) else ""}
                </wd:Business_Process_Definition_Data>
            </wd:Put_Business_Process_Definition_Request>
        </env:Body>
    </env:Envelope>"""
    return request


# <xsl:attribute name="wd:ID">ISSG_{integration["Name"].replace(' ','_')}</xsl:attribute>

# TODO: Add security domains to Security Group. Don't erase security for entire domain
