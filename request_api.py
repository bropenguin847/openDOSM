"""
APIs (Application Programming Interfaces) are an essential part of modern software development,
allowing different applications to communicate and share data. Think of it as a bridge between
two different software systems, allowing them to exchange information and functionality.   


Libraries to install:
        - pandas fastparquet    (do: pip install pandas fastparquet)
        - requests library      (do: pip install requests)

data.gov.my is Malaysia's official open data portal.
This file details the API's response code and what each code means

Query Response:
CODE        STATUS              DESCRIPTION
200         OK                  Successful Request
400         Bad Request         Invalid request. Check error message for more information.
404	        Not Found	        The resource requested doesn't exist.
429	        Too Many Requests	Your client is currently being rate limited.
                                Request an API token at Authentication to increase usage limits.
500	        Server Error	    Something went wrong with OpenAPI!

By default, the API returns a list of records.
If more details are needed, implement the meta parameter:
Use & to combine meta parameter together.

Example: 
    (Without Meta)  "https://api.data.gov.my/data-catalogue?id=YOURID&limit=3"
    (With Meta)     "https://api.data.gov.my/data-catalogue?id=YOURID&limit=3&meta=true"

To request with pandas fastparquet, and convert to dataframe
Example:
    import pandas as pd

    URL_DATA = 'https://storage.data.gov.my/mining/mineral_extraction.parquet'

    df = pd.read_parquet(URL_DATA)
    if 'date' in df.columns: df['date'] = pd.to_datetime(df['date'])

    print(df)    

Query Parameters:
Parameters----------Type------------Description
filter              string      Filters results to match the exact column value (case-sensitive)
ifilter             string      Filters results to match the exact column value (case-insensitive)
contains            string      Filters results to match a partial column value (case-sensitive)
icontains           string      Filters results to match a partial column value (case-insensitive)
range               string      Filters numerical column values within a specified range.
sort                string      Specifies the records order (ascending or descending).
date_start          date        Filters results starting from a specific date.
date_end            date        Filters results ending at a specific date.
timestamp_start     datetime    Filters results starting from a specific timestamp.
timestamp_end       datetime    Filters results ending at a specific timestamp.
limit               integer     Sets the maximum number of records to return.
include             string      Specifies which columns to include in the records.
exclude             string      Specifies which columns to exclude from the records.

Please note that the filter parameter is used for row-level filtering,
while include/exclude parameters are used for column-level filtering.

More detail can be found here:
https://developer.data.gov.my/request-query

"""


import requests

def get_post(url, limit=int, meta=bool):
    r"""Sends a GET request and returns a json of response.

    :param params: meta, limit
    :return: response.json()

    If request successfully, returns json of response.
    If failed, returns error message
    """

    try:
        url += f"&limit={limit}"

        if meta is True:
            url += "&meta=true"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print("Error: ", response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
        print('Error:', e)
        return None


def main():
    """
    Example code with parameters: meta=True, limit=3
    """

    url = "https://api.data.gov.my/data-catalogue?id=prisoners_state"
    posts = get_post(url, limit=3, meta=True)

    if posts:
        # print('Posts Meta:', posts['meta'])
        # print('Fetched Data:', posts['data'])
        print(posts)
    else:
        print('Failed to fetch posts from API.')

    # Output
    # {'meta': {'catalogue_id': 'prisoners_state',  'data_as_of': '2022-12-31 23:59', 'last_updated': '2023-12-31 12:00', 'next_update': '2024-12-31 12:00', 'data_source': ['Penjara'], 'update_frequency': 'YEARLY', 'total': 3, 'limit': 3},
    #  'data': [{'sex': 'both', 'date': '2017-01-01', 'state': 'Malaysia', 'prisoners': 120048},
    #           {'sex': 'both', 'date': '2018-01-01', 'state': 'Malaysia', 'prisoners': 115488},
    #           {'sex': 'both', 'date': '2019-01-01', 'state': 'Malaysia', 'prisoners': 136145}]}

if __name__ == "__main__":
    main()
