#!bin/python

#Author: Sebastiani Aguirre-Navarro
#Date: 3-March-2015 @ 9:49 PM
#atmospheric-sounding.py

from argparse import ArgumentParser
from BeautifulSoup import BeautifulSoup
from math import exp
import numpy as np
import matplotlib.pyplot as plt
import requests


#constants
SERVICE_URL = "http://www.weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%%3ALIST&YEAR=%s&MONTH=%s&FROM=%s&TO=%s&STNM=%s"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}

#utility functions

def refractivity(temp, pressure, dew_pointT):
    #Transform temp from C -> K
    temp_K = temp + 273.15

    #1 hPa = 1 mbars, so no conversion required

    x = dew_pointT*(18.729 - dew_pointT/227.3)/(dew_pointT + 257.87)
    Pw = 6.1121*exp(x)

    #return refractivity
    return (77.6/temp_K)*(pressure + (4810*Pw)/temp_K)

def plot_all(numeric_data, refractivities, gradient_N):
    heightKM = np.array([row[1]/1000.0 for row in numeric_data])
    temperature = np.array([row[2] for row in numeric_data])

    #plotting Height vs Temperature
    plt.title("Sounding for 29-December-2014")
    plt.scatter(temperature, heightKM)
    plt.plot(temperature, heightKM)
    plt.xlabel('Temperature(C)')
    plt.ylabel('Height(km)')
    plt.grid(True)
    plt.savefig('height-temperature.png')
    plt.clf()

    #plotting Height vs Refractivity
    plt.title("Sounding for 29-December-2014")
    plt.scatter(refractivities, heightKM)
    plt.plot(refractivities, heightKM)
    plt.xlabel('Refractivity(N-Units)')
    plt.ylabel('Height(km)')
    plt.grid(True)
    plt.savefig('height-refractivity.png')
    plt.clf()
    height = np.array([row[1] for row in numeric_data][:-1])


    #plotting Height vs Gradient of Refractivity
    plt.title("Sounding for 29-December-2014")
    plt.scatter(gradient_N, height)
    plt.plot(gradient_N, height)
    plt.xlabel('gradient of Refractivity(N-Units)/km')
    plt.ylabel('Height(m)')
    plt.grid(True)
    plt.savefig('height-gradient_refractivity.png')

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

print "creating refractivity array"
refractivities = np.array([refractivity(row[2], row[0], row[3]) for row in numeric_data])
gradient_N = list()

print "creating gradients"
i = 0
length = refractivities.size - 1
while i < length:
    grad = (refractivities[i+1] - refractivities[i])/(numeric_data[i+1][1]/1000 - numeric_data[i][1]/1000)
    gradient_N.append(grad)
    i += 1

gradient_N = np.array(gradient_N)

print "plotting..."
plot_all(numeric_data, refractivities, gradient_N)
