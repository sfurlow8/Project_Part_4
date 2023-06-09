import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import boto3, pathlib

# Scraping the website and extracting paragraphs
url = "https://www.abs.gov.au/statistics/health/health-conditions-and-risks/smoking/2020-21"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
paragraphs = soup.find_all("p")

for paragraph in paragraphs:
    print(paragraph)

# Connecting to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

table = dynamodb.Table('group-19')

# Inserting paragraphs into DynamoDB
i = 0
for paragraph in paragraphs:
    data = {
        'id': str(i), 
        'content': paragraph.text,
        'url': url,
        'access_time': str(datetime.now())
    }
    table.put_item(Item=data)
    i += 1

# The previous data, as obtained from the relevant code of part 3

url = "https://www.abs.gov.au/statistics/health/health-conditions-and-risks/smoking/latest-release" # site to scrape
response = requests.get(url).text
soup = BeautifulSoup(response, "html.parser")

# get table attributes
tab = soup.find_all("table")[0]
#print(tab)
age_rates = [] # list of lists
for tr in tab.find_all("tr"): 
  if tr.find("td") is not None: # age rates in tr's
      age_group = tr.find("th").text
      rate = tr.find("td").text
      age_rates.append([age_group, rate])

print(age_rates)

"""My own code to convert age_rates to numbers"""

age_rates =  pd.DataFrame(age_rates).T.values.tolist()

print(age_rates)

numbers = age_rates[1]
numbers = [float(x) for x in numbers]
print(numbers)


# Searching for numbers in DynamoDB

for number in numbers:
    response = table.scan(
        FilterExpression="contains(content, :num)",
        ExpressionAttributeValues={":num": str(number)}
    )
    
    if response['Count'] == 0:
        print(f"Alert: Number {number} is not referenced in any paragraph.")
