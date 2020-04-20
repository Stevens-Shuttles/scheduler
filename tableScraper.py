import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
lines = []
urls = []

lines.append("Blue")
urls.append('https://www.stevens.edu/directory/division-facilities-campus-operations/transportation-and-parking/stevens-shuttles/stevens-shuttle-blue-line-schedule')

if len(urls) != len(lines):
    print("Invalid Input Data")
else:
    for i in range(len(urls)):
        html = requests.get(urls[i]).content
        df_list = pd.read_html(html)
        df = df_list[-1]
        json_data = str(df.to_dict('list'))
        json_data = "{0}".format(json_data)

        s = json.dump(json_data)
        open('json/'+lines[i]+'.json', 'w', encoding='utf-8').write(s)
        print("Succesfully updated " + lines[i] + " line")