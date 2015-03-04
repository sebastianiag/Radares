#!bin/python

#Author: Sebastiani Aguirre-Navarro
#Date: 3-March-2015 @ 9:49 PM
#atmospheric-sounding.py

from argparse import ArgumentParser
from BeautifulSoup import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import requests


#constants
SERVICE_URL = "http://www.weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%%3ALIST&YEAR=%s&MONTH=%s&FROM=%s&TO=%s&STNM=%s"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}

#options parser
parser = ArgumentParser()
parser.add_argument("--year", type=str, help="year of interest")
parser.add_argument("--month", type=str, help="month of interest")
parser.add_argument("--From", type=str, help="from Day/{00 or 12}")
parser.add_argument("--to", type=str, help="to Day/{00 or 12}")
parser.add_argument("--station", type=str, default="78526", help="station number, default is #78526 San Juan, PR")
args = parser.parse_args()

#fetching data
url = SERVICE_URL % (args.year, args.month, args.From, args.to,  args.station)
req = requests.get(url, headers=HEADERS)
html_text = BeautifulSoup(req.text)

pre_info = html_text.find('pre').string

pre_split = pre_info.split("-----------------------------------------------------------------------------")
data_headers = pre_split[1]
string_data = pre_split[2].strip().split('\n')
string_data = [filter(lambda x: x != '', sublist) for sublist in map(lambda x: x.strip().split(' '), string_data)]
numeric_data = np.array([map(lambda x: float(x), sublist) for sublist in string_data])


