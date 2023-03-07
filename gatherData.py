import pandas as pd


def read_template() -> dict:
    integrationInfo = {}
    dataframe1 = pd.read_excel(
        "data_files/Mass_load_Template.xlsx",
        usecols=[
            0,
            1,
        ],
        skiprows=[4, 5, 6, 7, 8],
    )
    dataframe2 = pd.read_excel(
        "data_files/Mass_load_Template.xlsx",
        usecols=[
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
        ],
        skiprows=[4, 5, 6, 7, 8],
        header=2,
    )
    integrationInfo["tenant"] = dataframe1["Tenant"][0]
    integrationInfo["dataCenter"] = dataframe1["Data Center"][0]
    integrationInfo["integrationName"] = dataframe2["Integration Name"][0]
    integrationInfo["integrationTemplate"] = dataframe2["Integration Template"][0]
    integrationInfo["reportDataSource"] = dataframe2["Report Data Source (Optional)"][0]
    integrationInfo["reportDataSourceFilter"] = dataframe2[
        "Report Data Source Filter (Optional)"
    ][0]
    integrationInfo["deliveryService"] = dataframe2["Delivery (T/F)"][0]
    integrationInfo["deliveryProtocol"] = dataframe2["Delivery Protocol (Optional)"][0]
    integrationInfo["retrievalService"] = dataframe2["Retrieval (T/F)"][0]
    integrationInfo["retrievalProtocol"] = dataframe2["Retrieval Protocol (Optional)"][
        0
    ]

    return integrationInfo
