import urllib
import pandas as pd
import requests as requests
from bs4 import BeautifulSoup

datasetLocation = "nifty50.xlsx";
df = pd.read_excel(datasetLocation, "Sheet1")
userAgent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'}
searchURL = "https://www.google.com/search?q="
for x in range(0, len(df.index)):
    if str(df.iloc[x, 2]) is None:
        print(str(df.iloc[x, 0]) + " | " + str(df.iloc[x, 2]) + " | " + str(df.iloc[x, 3]))
    else:
        companyName = df.iloc[x, 0]
        searchOne = BeautifulSoup(requests.get(searchURL + urllib.parse.quote_plus(companyName) + '+headquarters ', headers=userAgent).text, 'html.parser')
        headline = searchOne.find('div', {"class": "Z0LcW"})
        if headline is not None:
            headquarters = headline.get_text()
        searchTwo = BeautifulSoup(requests.get(searchURL + urllib.parse.quote_plus(headquarters) + '+coordinates', headers=userAgent).text, 'html.parser')
        coordinates = searchTwo.find('div', {"class": "Z0LcW"}).get_text()
        df.loc[x, 'Location'] = headquarters;
        df.loc[x, 'Coordinates'] = coordinates
        print(df.iloc[x, 0] + " | " + headquarters + " | " + coordinates)
    df.to_excel(datasetLocation, index=False)
