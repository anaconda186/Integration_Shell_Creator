# Integration_Shell_Creator

## Repo URL
https://github.com/anaconda186/Integration_Shell_Creator.git

The goal of this program is to completely automate the initilization of Integrations. 
This will create the initial shell of the integration. 
Custom configuration will still need to be made. 

## TODO/Milestones
 - [ ] Create Integration System
    - [X] Connector - Completed 2021-10-15
    - [X] EIB - Completed 2021-10-17
       - [X] Create Shell Report - Completed 2021-10-16
       - [X] Create Report with defined Data Source - Completed 2021-10-17
       - [X] Create EIB - Completed 2021-10-17
       - [X] Add Integration Report Tag - 2022-04-25
    - [ ] Studio
       - [X] Create Cloud Integration Template - Completed 2021-10-15
       - [ ] Initialize Cloud Collection
       - [ ] Attach Empty Clar file
 - [X] Create ISU - Completed: 2021-10-16
    - [X] Create ISU - Completed: 2021-10-13
    - [X] Generate Password - Completed: 2021-10-16
 - [ ] Create Security Group
    - [X] Create ISSG
    - [ ] Add security domain to ISSG
 - [ ] Add BP Customization
    - [ ] Define Delivery/ Retrieval Step
 - [ ] Create Optional Services
 - [ ] GUI
 - [ ] Read Template Data for Mass Load


## Notes
 - Need to be careful adding security to ISSG
    * https://community.workday.com/node/524925
    * Adding ISSG to Domain will overwrite the entire domain
 - This Program can only be used by implementer
    * Uses private web services
 

## Reminders
 - Ask BT about migration studio. How do migrate Clar file and load clar file
 - For studio creation look into what happens when studio deploys integration.

## Testing adding a Cloud Collection
 <?xml version="1.0"?>
<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:wd="urn:com.workday/bsvc">
    <soapenv:Body>
        <wd:Put_Cloud_Collection_Request>
            <wd:Cloud_Collection_Data>
                <wd:Cloud_Collection_ID>INTXXX_Testing_Cloud_Collection</wd:Cloud_Collection_ID>
                <wd:Integration_System_References>
                    <wd:Integration_System_Reference>
                        <wd:ID wd:type="Integration_System_ID">INTXXX_Testing_Studio_Build_v1</wd:ID>
                    </wd:Integration_System_Reference>
                </wd:Integration_System_References>
                <wd:Repository_Document_Data
                    wd:Document_ID = "Test_Clar_v1"
                    wd:File_Name = "Test_Clar_v1">
                    <wd:Expiration_Timestamp>2025-10-18T10:19:32</wd:Expiration_Timestamp>
                    <wd:Content_Type_Reference>
                        <wd:ID wd:type = "Content_Type_ID">application/zip</wd:ID>
                    </wd:Content_Type_Reference>
                    <wd:Document_Type_Reference>
                        <wd:ID wd:type = "Document_Type_ID">ZIP</wd:ID>
                    </wd:Document_Type_Reference>
                </wd:Repository_Document_Data>
            </wd:Cloud_Collection_Data>
        </wd:Put_Cloud_Collection_Request>
    </soapenv:Body>
</soapenv:Envelope>

Get_Cloud_Collection

<?xml version="1.0"?>
<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:wd="urn:com.workday/bsvc">
    <soapenv:Body>
        <wd:Get_Cloud_Collections_Request>
            <wd:Request_References>
                <wd:Cloud_Collection_Reference>
                	<wd:ID wd:type = "Cloud_Collection_ID">INT_Studio_Positive_Pay_File_Outbound_Collection</wd:ID>
                </wd:Cloud_Collection_Reference>
            </wd:Request_References>
        </wd:Get_Cloud_Collections_Request>
    </soapenv:Body>
</soapenv:Envelope>

Get Business Process Definition

<?xml version="1.0" encoding="utf-8"?>
<env:Envelope
    xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
    <env:Body>
        <wd:Get_Business_Process_Definitions_Request
            wd:version="v35.0"
            xmlns:wd="urn:com.workday/bsvc">
            <wd:Request_References>
                <wd:Business_Process_Definition_Reference>
                    <wd:ID wd:type= "Business_Process_Definition_ID">INTEGRATION_PROCESS_EVENT_FOR_INTXXX_ANSI_SERVICES_TEST_(TOP_LEVEL)</wd:ID>
                </wd:Business_Process_Definition_Reference>
            </wd:Request_References>
        </wd:Get_Business_Process_Definitions_Request>
    </env:Body>
</env:Envelope>

Put Business Process with Delivery

<?xml version="1.0" encoding="utf-8"?>
<env:Envelope
    xmlns:env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
    <env:Body>
        <wd:Put_Business_Process_Definition_Request
            wd:version="v35.0"
            xmlns:wd="urn:com.workday/bsvc">
            <wd:Business_Process_Definition_Data>
                <wd:Business_Process_Definition_ID>
               Test_Value
                </wd:Business_Process_Definition_ID>
                <wd:Business_Process_Type_Reference>
                    <wd:ID wd:type="Business_Process_Type">Integration Process ID
                </wd:ID>
                </wd:Business_Process_Type_Reference>
                <wd:Integration_System_Reference>
                    <wd:ID wd:type="Integration_System_ID">INTXXX_Test_ANSI</wd:ID>
                </wd:Integration_System_Reference>
                <wd:Rule_Based_Definition>0</wd:Rule_Based_Definition>
                <wd:Effective_Date>2022-04-27</wd:Effective_Date>
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
                        <wd:ID wd:type="Event_Service_Name">Fire Integration</wd:ID>
                    </wd:Event_Service_Reference>
                    <wd:Process_by_All_in_Role>0</wd:Process_by_All_in_Role>
                    <wd:Disable_System_Notification>0</wd:Disable_System_Notification>
                </wd:Business_Process_Step_Data>
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
                        </wd:Integration_Data_Communication_Data>
                    </wd:Document_Delivery_Configuration_Data>
                    <wd:Process_by_All_in_Role>0</wd:Process_by_All_in_Role>
                    <wd:Disable_System_Notification>0</wd:Disable_System_Notification>
                </wd:Business_Process_Step_Data>
            </wd:Business_Process_Definition_Data>
        </wd:Put_Business_Process_Definition_Request>
    </env:Body>
</env:Envelope>
