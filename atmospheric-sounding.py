#!bin/python

#Author: Sebastiani Aguirre-Navarro
#Date: 3-March-2015 @ 9:49 PM
#atmospheric-sounding.py

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from math import exp
import numpy as np
import matplotlib.pyplot as plt
import requests


#constants
SERVICE_URL = "http://www.weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%%3ALIST&YEAR=%s&MONTH=%s&FROM=%s&TO=%s&STNM=%s"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}

#utility functions

class SoundingTable:
    def __init__(self):
        self.name = ''
        self.tableHeaders = ''
        self.numericData = np.array([])
        self.refractivities = np.array([])
        self.gradient_N = np.array([])
        self.no_vapor_Ns = np.array([])

    def plot_all(self):
        heightKM = np.array([row[1]/1000.0 for row in self.numericData])
        temperature = np.array([row[2] for row in self.numericData])
        dew_temperature = np.array([row[3] for row in self.numericData])
        
        #plotting Height vs Temperature
        plt.title("Sounding for %s-December-2014" % self.name)
        plt.scatter(temperature, heightKM)
        plt.plot(temperature, heightKM)
        plt.scatter(dew_temperature, heightKM, color="red")
        plt.plot(dew_temperature, heightKM, 'r')
        plt.xlabel('Temperature(C)')
        plt.ylabel('Height(km)')
        plt.grid(True)
        plt.savefig('%s-height-temperature.png' % self.name)
        plt.clf()

        #plotting Height vs Refractivity without vapor
        plt.title("Sounding for %s-December-2014"% self.name)
        plt.scatter(self.no_vapor_Ns, heightKM, color="green")
        plt.plot(self.no_vapor_Ns, heightKM, 'g')
        plt.scatter(temperature, heightKM)
        plt.plot(temperature, heightKM)
        plt.xlabel('Refractivity(N-Units)')
        plt.ylabel('Height(km)')
        plt.grid(True)
        plt.savefig('%s-height-refractivity-no-Vapor.png' % self.name)
        plt.clf()
        
        #plotting Height vs Refractivity
        plt.title("Sounding for %sZ-December-2014" % self.name)
        plt.scatter(self.refractivities, heightKM)
        plt.plot(self.refractivities, heightKM)
        plt.xlabel('Refractivity(N-Units)')
        plt.ylabel('Height(km)')
        plt.grid(True)
        plt.savefig('%s-height-refractivity.png' % self.name)
        plt.clf()
        height = np.array([row[1] for row in self.numericData][:-1])


        #plotting Height vs Gradient of Refractivity
        plt.title("Sounding for %sZ-December-2014" % self.name)
        plt.scatter(self.gradient_N, height)
        plt.plot(self.gradient_N, height)
        plt.xlabel('gradient of Refractivity(N-Units)/km')
        plt.ylabel('Height(m)')
        plt.grid(True)
        plt.savefig('%s-height-gradient_refractivity.png' % self.name)
        plt.clf()
        
        
def refractivity(temp, pressure, dew_pointT):
    #Transform temp from C -> K
    temp_K = temp + 273.15

    #1 hPa = 1 mbars, so no conversion required

    x = dew_pointT*(18.729 - dew_pointT/227.3)/(dew_pointT + 257.87)
    Pw = 6.1121*exp(x)

    #return refractivity
    return (77.6/temp_K)*(pressure + (4810*Pw)/temp_K)
    
def noVaporRefractivity(temp, pressure):
    temp_K = temp + 273.15
    return (77.6/temp_K)*pressure
    
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

pre_info = html_text.find_all('pre')[::2]
tables = list()
names = ["2900Z", "2912Z"]
k=0
for pre_tag in pre_info:
    table = SoundingTable()
    table.name = names[k]
    k += 1
    pre_split = pre_tag.string.split("-----------------------------------------------------------------------------")
    table.tableHeaders = pre_split[1]
    string_data = pre_split[2].strip().split('\n')
    string_data = [filter(lambda x: x != '', sublist) for sublist in map(lambda x: x.strip().split(' '), string_data)]
    table.numericData = np.array([map(lambda x: float(x), sublist) for sublist in string_data])
    tables.append(table)

    
print "creating refractivity array"
for table in tables:
    table.refractivities = np.array([refractivity(row[2], row[0], row[3]) for row in table.numericData])
    table.no_vapor_Ns = np.array([noVaporRefractivity(row[2], row[0]) for row in table.numericData])
    gradient_N = list()
    print "creating gradients"
    i = 0
    length = table.refractivities.size - 1
    while i < length:
        grad = (table.refractivities[i+1] - table.refractivities[i])/(table.numericData[i+1][1]/1000 - table.numericData[i][1]/1000)
        gradient_N.append(grad)
        i += 1
    table.gradient_N = gradient_N

    print "plotting..."
    table.plot_all()
