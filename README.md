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
       - [ ] Add Integration Report Tag
    - [ ] Studio
       - [X] Create Cloud Integration Template - Completed 2021-10-15
       - [ ] Initialize Cloud Collection
       - [ ] Attach Empty Clar file
 - [X] Create ISU - Completed: 2021-10-16
    - [X] Create ISU - Completed: 2021-10-13
    - [X] Generate Password - Completed: 2021-10-16
 - [ ] Create Security Groupx
    - [X] Create ISSG
    - [ ] Add security domain to ISSG
 - [ ] Create Optional Services
 - [ ] GUI
 - [ ] Retrieve Smartsheet Data


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
