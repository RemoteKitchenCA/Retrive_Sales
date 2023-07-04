import time

from API_Request_Acess_Token import get_access_token
import requests
import pytz
import datetime
import json


'''# Set the time zone to Vancouver (PST)
vancouver_tz = pytz.timezone('America/Vancouver')
# Get the current time in Vancouver
current_time = datetime.datetime.now(tz=vancouver_tz)
# Format the date as "2023-06-21"
current_date = current_time.strftime('%Y-%m-%d')
# Format the time as "3:17 AM"
time_str = current_time.strftime('%#I:%M %p')
# Print the Vancouver date and time
print("Current Vancouver Date (PST):", current_date)
print("Current Vancouver Time (PST):", time_str)

# Get yesterday's date
yesterday_date = (current_time - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
print("Yesterday's Vancouver Date (PST):", yesterday_date)

# Format yesterday's date in the desired format %d-%b-%Y
Yesterdate_Date_Format_RPA_Data = (current_time - datetime.timedelta(days=1)).strftime("%d-%b-%Y")
print(Yesterdate_Date_Format_RPA_Data)

# Get the date before yesterday
pre_yesterday_date = (datetime.datetime.strptime(yesterday_date, '%Y-%m-%d') - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
print("Date before yesterday (PST):", pre_yesterday_date)

yesterday_date = current_date
#yesterday_date = '2023-06-24'
pre_yesterday_date = (datetime.datetime.strptime(yesterday_date, '%Y-%m-%d') - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
print("Date before yesterday (PST):", pre_yesterday_date)
#Yesterdate_Date_Format_RPA_Data = '23-Jun-2023'
'''

# Set the time zone to Vancouver (PST)
vancouver_tz = pytz.timezone('America/Vancouver')

# Get the current time in Vancouver
current_time = datetime.datetime.now(tz=vancouver_tz)

# Option 1: Manually set the current date
#current_date = '2023-06-01'

# Option 2: Automatically obtain the current date from the system
current_date = current_time.strftime('%Y-%m-%d')

time_str = current_time.strftime('%#I:%M %p')

# Calculate the previous date
previous_date = (datetime.datetime.strptime(current_date, '%Y-%m-%d') - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
Yesterdate_Date_Format_RPA_Data = (datetime.datetime.strptime(current_date, '%Y-%m-%d') - datetime.timedelta(days=1)).strftime('%d-%b-%Y')

print("Current Vancouver Date (PST):", current_date)
print("Current Vancouver Time (PST):", time_str)
print("Previous Date (YYYY-MM-DD):", previous_date)
print("Previous Date Format for RPA Data:", Yesterdate_Date_Format_RPA_Data)

# Make the API call to get the access token
response_Bitable_API = get_access_token()
Base_access_token = response_Bitable_API['tenant_access_token']
print(Base_access_token)

url = 'https://open.larksuite.com/open-apis/bitable/v1/apps/LFgnb5CgMa45i6sYecguIw43sWf/tables/tblULfltBykVRAYY/records'
headers = {'Authorization': f'Bearer {Base_access_token}'}
params = {
    'view_id': 'vewgYGpWVO',
    'field_names': '["Promotion Date","Platform","VR Name","Retrieve Sales Extract Status"]',
    'filter': f'CurrentValue.[Promotion Date] = "{Yesterdate_Date_Format_RPA_Data}" && CurrentValue.[Retrieve Sales Extract Status] = ""'
}

response_RPA = requests.get(url, headers=headers, params=params)
if response_RPA.status_code == 200:
    RPA_data = response_RPA.json()['data']
    if 'items' in RPA_data:
        RPA_Data_items = RPA_data['items']
        #print(RPA_Data_items)
        url = 'https://api.tryotter.com/graphql'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJzdWIiOiI0NWNjM2VkYy05Mjc3LTRkN2ItOTY5MS0wMWMzMzlhZTQ2ZDciLCJpc1JlZnJlc2giOmZhbHNlLCJ2ZXIiOiIzIiwiZXhwIjoxNjkwMTgyMzY5LCJ0eXBlIjoiYWNjb3VudCIsImlhdCI6MTY4NzU5MDM2OSwic2lkIjoiNzkxN2FmMDMtYTU5My00ZjBmLWI1MmUtMDllZDRmOGY3NGNmIn0.AQKh3QdPSS9k_zXFPtN0MIRUZfBi8pP3CscumHN2yStNPuklWTBecm5AFdU4xhxhfOq7rmZu-pPPCmU8nOtBFeKNAWWOeuEWJfESGCAkP2vU2kqZz_0IjBwRcDqbS9Vv-AL3l7geywgP6MRFWDg28-JhR186fSNtW48B3HExCyAMnT1G',
            'Cookie': '__cf_bm=OSOY449GbQlWVMJtaX78aCh4kXAw3UuT3anYeNjNrOk-1687607472-0-AVvsfsEBYz0zUZuFlWDS/NTOUr/dMTgziKEI8TCXp0fp/tGaXdjmcfQnPsFyyjtks85BHoWlQBu0T8tPRHNagwk='
        }
        payload = {
            "query": "query GetOrganization($input: OrganizationByIdInput!, $includeVirtualBrands: Boolean = false, $storeLimit: Int = 1000, $organizationId: ID!) {\r\n  organizationById(input: $input) {\r\n  ...OrganizationFields\r\n  __typename\r\n  }\r\n  }\r\n  \r\n  fragment OrganizationFields on Organization {\r\n  id\r\n  name\r\n  brandsV2(first: 1000, scope: FINANCE) {\r\n  ...BrandV2Fields\r\n  __typename\r\n  }\r\n  virtualBrands(first: 1000) @include(if: $includeVirtualBrands) {\r\n  ...VirtualBrandFields\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  \r\n  fragment BrandV2Fields on OrganizationBrandConnection {\r\n  edges {\r\n  node {\r\n  ...BrandFields\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  fragment BrandFields on Brand {\r\n  id\r\n  name\r\n  storesV2(first: $storeLimit, scope: FINANCE, organizationIds: [$organizationId]) {\r\n  edges {\r\n  node {\r\n  ...StoreFields\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  \r\n  fragment StoreFields on Store {\r\n  id\r\n  brandId\r\n  facility {\r\n  ...FacilityFields\r\n  __typename\r\n  }\r\n  currencyCode\r\n  tenantType\r\n  __typename\r\n  }\r\n  \r\n  fragment FacilityFields on Facility {\r\n  id\r\n  name\r\n  address {\r\n  ...AddressFields\r\n  __typename\r\n  }\r\n  externalName\r\n  timezone\r\n  currencyCode\r\n  isCssFacility\r\n  __typename\r\n  }\r\n  \r\n  fragment AddressFields on Address {\r\n  addressOne\r\n  addressTwo\r\n  latLong {\r\n  latitude\r\n  longitude\r\n  __typename\r\n  }\r\n  countryCode\r\n  __typename\r\n  }\r\n  \r\n  fragment VirtualBrandFields on OrganizationVirtualBrandConnection {\r\n  edges {\r\n  node {\r\n  id\r\n  name\r\n  stores(first: 1000) {\r\n  edges {\r\n  node {\r\n  id\r\n  active\r\n  currencyCode\r\n  facility {\r\n  id\r\n  name\r\n  address {\r\n  addressOne\r\n  countryCode\r\n  latLong {\r\n  latitude\r\n  longitude\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  __typename\r\n  }\r\n  __typename\r\n  }",
            "variables": {
                "includeVirtualBrands": False,
                "input": {"organizationId": "86ce5423-7fdc-489f-9382-8b164f560bb4"},
                "organizationId": "86ce5423-7fdc-489f-9382-8b164f560bb4",
                "storeLimit": 1000
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        # print(data)

        # Parse the JSON data
        # data = json.loads(json_data)

        # Sales_API_URL
        # StoreID = '0f6a2bc7-e0d6-4792-80ae-2ca60288d695'
        Platform = 'ubereats'
        Authorisation_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzUxMiJ9.eyJzdWIiOiI0NWNjM2VkYy05Mjc3LTRkN2ItOTY5MS0wMWMzMzlhZTQ2ZDciLCJpc1JlZnJlc2giOmZhbHNlLCJ2ZXIiOiIzIiwiZXhwIjoxNjkwMTc0OTA5LCJ0eXBlIjoiYWNjb3VudCIsImlhdCI6MTY4NzU4MjkwOSwic2lkIjoiMWRjNjk0YzUtODllNy00NmZlLThjMjktZmU1NjkzODNjNWRjIn0.AJpCcMA41yya2y9y3e8q7ruBwMTPf1PLKl9AGM32Pu6gZST1AJnrSdilKx7w1usrUiSs1hMLbM3CIsrVl6OGdLqOAAvN6PQP56702RiC5BLhsP9QOyVbV_-tPzTFMJ8OREGqQRZgaNgoRDH9GREPfcJiYeNqocZzxrIZJNkHTpFV2b3u'

        sales_url = "https://api.tryotter.com/analytics/summary/order_performance_cullinan/total_revenue_non_cancelled_local_currency"
        brands = data['data']['organizationById']['brandsV2']['edges']
        found_match = False
        for item in RPA_Data_items:
            fields = item['fields']
            promotion_date = fields['Promotion Date']
            platform = fields['Platform']
            if "Uber" in platform:
                platform = "ubereats"
            elif "DoorDash" in platform:
                platform = "doordash"
            elif "Skip" in platform:
                platform = "Skip The Dishes"
            vr_name = fields['VR Name']
            get_store_name = vr_name
            record_id = item['record_id']
            print()
            print("Promotion Date:", promotion_date)
            print("Platform:", platform)
            print("VR Name:", vr_name)
            print("record_id:", record_id)
            print()  # Add an empty line between each item

            for brand in brands:
                store_node = brand['node']
                store_name = store_node['name']
                stores_v2 = store_node['storesV2']['edges']
                for store in stores_v2:
                    store_id = store['node']['id']
                    brand_id = store['node']['brandId']

                    #if store_name.upper().strip() == get_store_name.upper().strip():
                    if get_store_name.upper().strip() in store_name.upper().strip():
                        print("Store name:", store_name)
                        print("Store ID:", store_id)
                        print("Brand ID:", brand_id)
                        print()
                        payload = {
                            "filterSet": [
                                {
                                    "maxDate": f"{current_date}T06:59:59.999Z",
                                    "minDate": f"{previous_date}T07:00:00.000Z",
                                    "filterType": "dateRangeFilter"
                                },
                                {
                                    "filterType": "categoryFilter",
                                    "dimensionName": "store",
                                    "op": "IN",
                                    "values": [store_id]
                                },
                                {
                                    "filterType": "categoryFilter",
                                    "dimensionName": "ofo",
                                    "op": "IN",
                                    "values": [Platform]
                                }
                            ],

                            "scopeSet": [
                                {
                                    "key": "store",
                                    "values": [store_id]
                                }
                            ],
                            "useRealTimeDataset": False
                        }

                        headers = {
                            'authority': 'api.tryotter.com',
                            'accept': '*/*',
                            'accept-language': 'en-US,en;q=0.9',
                            'application-name': 'op-app-insights',
                            'authorization': f'{Authorisation_token}',
                            'content-type': 'application/json',
                            'origin': 'https://manager.tryotter.com',
                            'referer': 'https://manager.tryotter.com/',
                            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-site',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                            'Cookie': '__cf_bm=nksfY7Jr74QZisZDVRmAnUxRzd3r4y6bqjvBkpWw5D8-1687611162-0-AdZZ7ofhn+ljHYL6kXZwiAG6axOCDYonel7mkeuTDa8lJwhTlRBVPkHEO5xNHjtFl9H9JY0eP8+c7CV3qQIpd6I='
                        }

                        response = requests.post(sales_url, headers=headers, json=payload)
                        # print(response.text)
                        # Parse the JSON response
                        sales_data = json.loads(response.text)

                        # Extract the desired data
                        platform = sales_data['request']['filterSet'][2]['values'][0]
                        # store_id = sales_data['request']['scopeSet'][0]['values'][0]
                        # gross_sale = round(data['value'], 2)
                        #gross_sale = f'{sales_data["value"]:.2f}'
                        #gross_sale = round(sales_data['value'], 2)
                        gross_sale = '{:.2f}'.format(round(sales_data['value'], 2))

                        # Print the extracted data
                        print("Platform:", platform)
                        # print("Store_ID:", store_id)
                        print("Gross_Sale:", gross_sale)
                        found_match = True
                        time.sleep(1)
                        # URL
                        url = f"https://open.larksuite.com/open-apis/bitable/v1/apps/LFgnb5CgMa45i6sYecguIw43sWf/tables/tblULfltBykVRAYY/records/{record_id}"
                        # Authorization header value
                        token = f'Bearer {Base_access_token}'
                        # print(token)
                        write_headers = {"Authorization": token}
                        # Request body data
                        data = {"fields": {"Sales": str(gross_sale), "Retrieve Sales Extract Status": "Done"}}
                        # Send the PUT request
                        time.sleep(0.5)
                        response = requests.put(url, headers=write_headers, json=data)
                        # Print the response status code and body
                        print(f"Status code: {response.status_code}")
                        # print(f"Response body: {response.json()}")
                        # ----------------------------------------
                        time.sleep(0.5)
                        break

                    if found_match:
                        break

            if not found_match:
                print("No Data Found")

    else:
        print("No Data available")