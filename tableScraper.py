import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.stevens.edu/directory/division-facilities-campus-operations/transportation-and-parking/stevens-shuttles/stevens-shuttle-blue-line-schedule'
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[-1]
json = str(df.to_dict('list'))
print(json)
