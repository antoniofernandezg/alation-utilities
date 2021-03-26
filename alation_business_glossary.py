# Author: Jonathan Lanham, Alation Professional Services
# Last Modified: 19 Jan 2021

import csv
import requests

# PARAMETERS TO UPDATE
# Add the customer values for the empty parameters below

base_url = 'http://3.227.155.241/'
token = 'keEispU_nSwt_Kzl8V9nbiuDNH6G1k65jTxMquJMcc0' #Can be v0 token or API Access token

#Update with the appropriate article template, if using script to update object pages then switch to default
template_name = 'Little Book of Real Estate Terms' 

#Do not touch for articles. For other data types refer to Alation documentation: https://customerportal.alationdata.com/docs/UploadLogicalMetadataAPI/index.html
object_type = 'article' 

# This will ensure that new articles are created if they do not already exist and that custom fields
# will be updated if articles already exist.
alation_api_endpoint = '/api/v1/bulk_metadata/custom_fields/'
params = '?create_new=true&replace_values=true'

api_url = base_url + alation_api_endpoint + template_name + '/' + object_type + params

print("Alation API URL: " + api_url)


content = 'application/json'
headers = {'token': token, 'Content-Type': content}

with open('./jlltest.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    row_number = 0

    for row in readCSV:
        #print(row)

        if row_number > 0:

            try:

                #Parse out the values from the csv
                article_title = row[0]
                description = row[5]
                asset_id = row[1]
                acronym = row[2]
                acronym_id = row[3]
                status = row[4]

                # Alation Upload Logical Metadata API formats (https://customerportal.alationdata.com/docs/CustomFieldValueUploadFormat/index.html)
                # 
                # Picker - {"<custom_field_name>": "<picker_value>"}
                # Multi-select Picker - {"<custom_field_name>": ["<multi_picker_value1>","<multi_picker_value2>","<multi_picker_value3>"...]}
                # Rich text - {"<custom_field_name>": "<rich_text_html_value>"}
                # Date - {"<custom_field_name>": "<date>"}
                # People set - {"<custom_field_name>": [{"type":"<otype>", "key":"<key>"}]}

                json_value = {
                    "key" : article_title,
                    "description": description,
                    "Asset ID": asset_id,
                    "Acronym": acronym,
                    "Acronym ID": acronym_id,
                    "Status": status
                }

                print("Json value for API call: " + str(json_value))

                res = requests.post(api_url, json=json_value, headers=headers)
                print("HTTP Response: " + str(res.status_code) + " Status: " + res.text)
                print("")

            except Exception as e:
                print(e)
                exit()
        else:
            row_number = row_number + 1