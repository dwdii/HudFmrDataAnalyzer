#
# Author: Daniel Dittenhafer
#
#     Created: Oct 18, 2014
#
# Description: Semester Project
#
__author__ = 'Daniel Dittenhafer'

import csv
import json
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
import numpy as np
import os.path
from scipy.optimize import curve_fit
from Tkinter import *
import tkFileDialog
import tkFont
import ttk
import urllib


class HudFairMarketRentsDataSet:
    def __init__(self):
        self.google_api_key = "AIzaSyCoRtlb-qvaq7bc-5NDdrEfcifLQwUDV0U"
        self.data = dict()
        self.yearData = dict()
        self.latlongs = dict()
        self.years = list()
        self.states = list()
        self.states.append("State")
        self.counties = dict()
        self.columnMapping = dict()
        self.fmrNames = ["fmr0","fmr1","fmr2","fmr3","fmr4"]

        self.prepColumnMappings()
        self.loadLocationData()

    def prepColumnMappings(self):

        # 2005
        mapping2005 = dict()
        mapping2005["county"] = 8
        mapping2005["state"] = 6
        mapping2005["fmr0"] = 1
        mapping2005["fmr1"] = 2
        mapping2005["fmr2"] = 3
        mapping2005["fmr3"] = 4
        mapping2005["fmr4"] = 5
        mapping2005["areaName"] = 10
        mapping2005["countyName"] = 9
        mapping2005["stateAlpha"] = 13
        self.columnMapping[2005] = mapping2005

        # 2006
        mapping2006 = dict()
        mapping2006["county"] = 7
        mapping2006["state"] = 6
        mapping2006["fmr0"] = 2
        mapping2006["fmr1"] = 3
        mapping2006["fmr2"] = 1
        mapping2006["fmr3"] = 4
        mapping2006["fmr4"] = 5
        mapping2006["areaName"] = 11
        mapping2006["countyName"] = 13
        mapping2006["stateAlpha"] = 14
        self.columnMapping[2006] = mapping2006

        # 2007
        mapping2007 = dict()
        mapping2007["county"] = 9
        mapping2007["state"] = 8
        mapping2007["fmr0"] = 1
        mapping2007["fmr1"] = 2
        mapping2007["fmr2"] = 3
        mapping2007["fmr3"] = 4
        mapping2007["fmr4"] = 5
        mapping2007["areaName"] = 7
        mapping2007["countyName"] = 13
        mapping2007["stateAlpha"] = 14
        self.columnMapping[2007] = mapping2007

        # 2008
        mapping2008 = dict()
        mapping2008["county"] = 7
        mapping2008["state"] = 6
        mapping2008["fmr0"] = 1
        mapping2008["fmr1"] = 2
        mapping2008["fmr2"] = 3
        mapping2008["fmr3"] = 4
        mapping2008["fmr4"] = 5
        mapping2008["areaName"] = 12
        mapping2008["countyName"] = 10
        mapping2008["stateAlpha"] = 14
        self.columnMapping[2008] = mapping2008

        # 2009
        mapping2009 = dict()
        mapping2009["county"] = 6
        mapping2009["state"] = 7
        mapping2009["fmr0"] = 1
        mapping2009["fmr1"] = 2
        mapping2009["fmr2"] = 3
        mapping2009["fmr3"] = 4
        mapping2009["fmr4"] = 5
        mapping2009["areaName"] = 12
        mapping2009["countyName"] = 10
        mapping2009["stateAlpha"] = 14
        self.columnMapping[2009] = mapping2009

        # 2010
        mapping2010 = mapping2009.copy()
        mapping2010["stateAlpha"] = 15
        self.columnMapping[2010] = mapping2010

        # 2011
        self.columnMapping[2011] = mapping2010

        # 2012
        self.columnMapping[2012] = mapping2009

        # 2013
        mapping2013 = dict()
        mapping2013["county"] = 7
        mapping2013["state"] = 8
        mapping2013["fmr0"] = 2
        mapping2013["fmr1"] = 3
        mapping2013["fmr2"] = 4
        mapping2013["fmr3"] = 5
        mapping2013["fmr4"] = 6
        mapping2013["areaName"] = 12
        mapping2013["countyName"] = 10
        mapping2013["stateAlpha"] = 15
        self.columnMapping[2013] = mapping2013

        # 2014
        mapping2014 = dict()
        mapping2014["county"] = 7
        mapping2014["state"] = 8
        mapping2014["fmr0"] = 3
        mapping2014["fmr1"] = 4
        mapping2014["fmr2"] = 2
        mapping2014["fmr3"] = 5
        mapping2014["fmr4"] = 6
        mapping2014["areaName"] = 12
        mapping2014["countyName"] = 10
        mapping2014["stateAlpha"] = 15
        self.columnMapping[2014] = mapping2014

        # 2015
        self.columnMapping[2015] = mapping2014

    def append(self, item):
        self.data.append(item)

    def find(self, year, state, county):
        return self.data.get(self.formatKey(year, state, county))

    def formatKey(self, year, state, county):
        key = "{0}.{1}.{2}".format(year, state, county)
        return key;

    def findAll(self, state, county):
        resultSet = list()
        for yr in self.years:
            resultSet.append(self.find(yr, state, county))
        return resultSet

    def load(self, year, file, geocode):
        """Loads the specified HUD FMR data for the specified year."""

        # Open a file stream
        strmData = open(file)

        # Wrap in a CSV data reader
        dataReader = csv.reader(strmData)

        # Get relevant column mapping for this year
        if not self.columnMapping.has_key(year):
            raise "Column mappings are unknown for year {0}.".format(year)
        else:
            mapYr = self.columnMapping[year]

        # Ensure we have allocated list for this year.
        if not self.yearData.has_key(year):
            self.yearData[year] = list()

        # Loop to read in the data rows
        for row in dataReader:
            try:
                if dataReader.line_num > 1:
                    dataRow = HudFairMarketRentsRow(year,
                                                    row[mapYr["county"]],
                                                    row[mapYr["state"]],
                                                    row[mapYr["areaName"]],
                                                    row[mapYr["countyName"]],
                                                    row[mapYr["stateAlpha"]],
                                                    row[mapYr["fmr0"]],
                                                    row[mapYr["fmr1"]],
                                                    row[mapYr["fmr2"]],
                                                    row[mapYr["fmr3"]],
                                                    row[mapYr["fmr4"]]
                    )
                    key = "{0}.{1}.{2}".format(dataRow.year, dataRow.stateAlpha, dataRow.countyName)
                    self.data[key] = dataRow
                    self.yearData[year].append(dataRow)

                    # Augment with lat/long
                    self.geocodeLocation(dataRow, geocode)

                    # Keep track of state and counties we've seen.
                    if not dataRow.stateAlpha in self.states:
                        self.states.append(dataRow.stateAlpha)
                        self.states.sort()

                    if not self.counties.has_key(dataRow.stateAlpha):
                        self.counties[dataRow.stateAlpha] = list()

                    if not dataRow.countyName in self.counties[dataRow.stateAlpha]:
                        self.counties[dataRow.stateAlpha].append(dataRow.countyName)
                        self.counties[dataRow.stateAlpha].sort()

            except Exception, ex:
                print ("On line {1}: {0} Skipping row...".format(ex, dataReader.line_num))

        # Close the file stream
        strmData.close()

        # Remember our year
        self.years.append(year)

    def geocodeLocation(self, dataRow, geocode):

        locationKey = "{0}-{1}".format(dataRow.countyName, dataRow.stateAlpha)
        if not self.latlongs.has_key(locationKey) and geocode:
            jd = json.JSONDecoder()

            url = "https://maps.googleapis.com/maps/api/geocode/json?address={0},+{1}&key={2}".format(
                dataRow.countyName, dataRow.stateAlpha, self.google_api_key)

            h = urllib.urlopen(url)
            if 200 == h.code:
                data = h.read()
                loc = jd.decode(data)
                if loc["status"] == "OK":
                    results = loc["results"]
                    self.latlongs[locationKey] = results[0]["geometry"]["location"]
                    self.saveLocationData()
                else:
                    print(locationKey.decode("latin1") + ": " + loc["status"])

        # populate the row lat/long data
        if self.latlongs.has_key(locationKey):
            dataRow.latitude = float(self.latlongs[locationKey]["lat"])
            dataRow.longitude = float(self.latlongs[locationKey]["lng"])
        else:
            dataRow.latitude = None
            dataRow.longitude = None

    def saveLocationData(self):
        with open('./Data/locationData.csv', 'wb') as locationfile:
            csv_writer = csv.writer(locationfile)

            for y in self.latlongs.keys():
                row = [y, self.latlongs[y]["lat"],self.latlongs[y]["lng"]]
                csv_writer.writerow(row)

    def loadLocationData(self):

        locationFilename = './Data/locationData.csv'

        if os.path.isfile(locationFilename):
            with open(locationFilename, 'rb') as locationfile:
                csv_reader = csv.reader(locationfile)

                for row in csv_reader:
                    loc = dict()
                    loc["lat"] = float(row[1])
                    loc["lng"] = float(row[2])
                    self.latlongs[row[0]] = loc

class HudFairMarketRentsRow:
    def __init__(self, year, countyid, stateid, areaname, countyName, stateAlpha, fmr0, fmr1, fmr2, fmr3, fmr4):
        self.year = year
        self.countyId = countyid
        self.stateId = stateid
        self.areaName = areaname
        self.countyName = countyName
        self.stateAlpha = stateAlpha
        self.latitude = 0.0
        self.longitude = 0.0

        self.fmr0 = int(fmr0)
        self.fmr1 = int(fmr1)
        self.fmr2 = int(fmr2)
        self.fmr3 = int(fmr3)
        self.fmr4 = int(fmr4)
        self.fmrAvg = (self.fmr0 + self.fmr1 + self.fmr2 + self.fmr3 + self.fmr4) / 5

    def __repr__(self):
        return repr("{0}-{1}: {2},{3},{4},{5},{6}".format(
            self.year, self.areaName,
            self.fmr0, self.fmr1,
            self.fmr2, self.fmr3,
            self.fmr4))


class App:
    def __init__(self, master):
        self.root = master
        self.root.title("HUD Fair Market Rents DataEuler")

        self.dataSet = HudFairMarketRentsDataSet()
        self.bGeoCode = BooleanVar()
        self.colorbar = None
        self.yearMaps = dict()
        self.mapFigure = None

        self.frame = Frame(self.root, width=400, height=500)
        self.frame.grid_propagate(0)
        self.frame.pack()

        # First Row: Header text about the app
        curRow = 0
        fullrowColSpan = 4
        self.lblInfo = Label(self.frame, wraplength=300, justify="left",
                             text="The HUD Fair Market Rents Data Analyzer app loads FMR data from CSV formatted files and provides an interface for basic analysis and visualization.""")
        self.lblInfo.grid(row=curRow, columnspan=fullrowColSpan)

        # Row:
        curRow += 1
        self.lblYear = Label(self.frame, text="Year: ", justify="right")
        self.lblYear.grid(row=curRow)

        self.txtYear = Entry(self.frame)
        self.txtYear.insert('insert', "2005")
        self.txtYear.grid(row=curRow, column=1)

        self.btnLoadFile = Button(self.frame, text="Load Data File", command=self.btnLoadFile_Click)
        self.btnLoadFile["state"] = "disabled"
        self.btnLoadFile.grid(row=curRow, column=2)

        # Row
        curRow += 1
        self.chkQueryGoogleGeocodeApi = Checkbutton(self.frame, text="Use Google Geocoding API", variable=self.bGeoCode)
        self.chkQueryGoogleGeocodeApi.grid(row=curRow, column=1)

        curRow += 1

        self.lblStatus = Label(self.frame, text="", justify="left")
        self.lblStatus.grid(row=curRow, column=0, columnspan=2)

        self.btnLoadAllFiles = Button(self.frame, text="Load All Files", command=self.btnLoadAllFiles_Click)
        self.btnLoadAllFiles.grid(row=curRow, column=2)

        # Row: Header -  Map Data Analysis
        curRow += 1

        self.lblGrpMapViz = Label(self.frame, text="Map Visualization")
        self.lblGrpMapViz.grid(row=curRow)
        self.lblGrpMapViz.grid(row=curRow, columnspan=fullrowColSpan)

        f = tkFont.Font(self.root, self.lblGrpMapViz.cget("font"))
        f.configure(underline = True)
        self.lblGrpMapViz.configure(font=f)

        # Row: Map Bedrooms
        curRow += 1

        self.lblBedrooms = Label(self.frame, text="Bedrooms: ", justify="right")
        self.lblBedrooms.grid(row=curRow, column=0)

        self.cbBedrooms = ttk.Combobox(self.frame, state="readonly")
        self.cbBedrooms['values'] = self.dataSet.fmrNames
        self.cbBedrooms.grid(row=curRow, column=1)

        # Row: Map Year
        curRow += 1

        self.lblMapYear = Label(self.frame, text="Year: ", justify="right")
        self.lblMapYear.grid(row=curRow, column=0)

        self.cbYears = ttk.Combobox(self.frame, state="readonly")
        self.cbYears['values'] = self.dataSet.years
        self.cbYears.grid(row=curRow, column=1)

        self.btnShowMap = Button(self.frame, text="Show Map", command=self.btnShowMap_Click)
        self.btnShowMap.grid(row=curRow, column=2)

        # Row: Header -  Multiyear Analysis
        curRow += 1

        self.lblGrpMultiYear = Label(self.frame, text="Multi-Year Analysis")
        self.lblGrpMultiYear.grid(row=curRow)
        self.lblGrpMultiYear.grid(row=curRow, columnspan=fullrowColSpan)
        self.lblGrpMultiYear.configure(font=f)

        # Row: States combo box
        curRow += 1

        self.lblState = Label(self.frame, text="State: ", justify="right")
        self.lblState.grid(row=curRow, column=0)

        self.cbStates = ttk.Combobox(self.frame, state="readonly")
        self.cbStates.bind('<<ComboboxSelected>>', self.cbStates_SelectionChanged)
        self.cbStates['values'] = self.dataSet.states
        self.cbStates.grid(row=curRow, column=1)

        # Row: County combo box
        curRow += 1

        self.lblCounty = Label(self.frame, text="County: ", justify="right")
        self.lblCounty.grid(row=curRow, column=0)

        self.cbCounties = ttk.Combobox(self.frame, state="readonly")
        self.cbCounties.grid(row=curRow, column=1)

        # Row: Button to launch Multi-year Linear Regression
        curRow += 1

        self.btnMultiYrLinearReg = Button(self.frame, text="Linear Reg", command=self.btnMultiYrLinearReg_Click)
        self.btnMultiYrLinearReg.grid(row=curRow, column=2)

        curRow += 1

        strCredits = "* The data included with this application was originally published by the U.S. Department of "
        strCredits += "Housing & Urban Development as required by Section 8 of the United States Housing Act of 1937."
        strCredits += " It is publicly available at: http://www.huduser.org/portal/datasets/fmr.html"

        self.lblCredits = Label(self.frame, wraplength=350,
            text=strCredits , justify="left")
        self.lblCredits.grid(row=curRow, column=0, columnspan=4, padx=(10,10), pady=(10,10))

        #self.load_file()

    def refreshStatesComboBox(self):
        self.cbStates["values"] = self.dataSet.states

    def refreshYearsComboBox(self):
        self.cbYears["values"] = self.dataSet.years

    def btnLoadFile_Click(self):
        #file = "C:/Users/Dan/Downloads/Data/50thPercentailRentEstimates/RawData/Csv/Revised_FY2005_CntLevel.csv"
        datafile = ""

        # If the hardcoded path doesn't exist, then prompt for a file.
        if not os.path.isfile(datafile):
            datafile = tkFileDialog.askopenfilename(parent=self.root)

        # get the year the user specified
        sYear = self.txtYear.get()
        bGeocode = self.bGeoCode.get()

        # load the file into our data set
        self.dataSet.load(int(sYear), datafile, bGeocode)

        # Update the UI list of states we know about.
        self.refreshStatesComboBox()

    def btnLoadAllFiles_Click(self):

        codePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Data")
        bGeocode = self.bGeoCode.get()

        # Disable while loading
        self.btnLoadAllFiles["state"] = "disabled"

        # Start with clean slate
        self.dataSet.data.clear()

        files = {
            2005: "2005-FMR.csv",
            2006: "2006-FMR.csv",
            2007: "2007-FMR.csv",
            2008: "2008-FMR.csv",
            2009: "2009-FMR.csv",
            2010: "2010-FMR.csv",
            2011: "2011-FMR.csv",
            2012: "2012-FMR.csv",
            2013: "2013-FMR.csv",
            2014: "2014-FMR.csv",
            2015: "2015-FMR.csv",
        }

        for yr in files.keys():
            # load the file into our data set
            filepath = os.path.join(codePath, files[yr])
            self.lblStatus.configure(text="Loading {0}...".format(files[yr]))
            self.root.update()
            self.dataSet.load(yr, filepath, bGeocode)

        self.lblStatus.configure(text="All files loaded.")
        self.root.update()

        # Update the UI list of states we know about.
        self.refreshStatesComboBox()
        self.refreshYearsComboBox()

        # enable while loading
        self.btnLoadAllFiles["state"] = "normal"

    def btnShowMap_Click(self):
        sYear = self.cbYears.get()
        self.MapData(int(sYear), self.cbBedrooms.get())

    def cbStates_SelectionChanged(self, val):
        self.cbCounties['values'] = self.dataSet.counties[self.cbStates.get()]

    def btnMultiYrLinearReg_Click(self):

        # Local Vars
        state = self.cbStates.get()
        county = self.cbCounties.get()
        data = self.dataSet.findAll(state, county)
        years = list()
        fmrX = dict()

        # Prep data for linear regression
        for d in data:
            years.append(d.year)

            # For each fmr type
            for f in self.dataSet.fmrNames:
                # Make sure we have a list for this fmr type
                if not fmrX.has_key(f):
                    fmrX[f] = list()
                # Add the value for this fmr/yr
                fmrX[f].append(getattr(d, f))


        # SciPi Linear Regression
        scipyLr = dict()
        for f in self.dataSet.fmrNames:
            scipyLr[f] = scipy_linearReg(years, fmrX[f])

        # What does this look like?
        fig = plt.figure()

        # Loop to plot each series
        plots = list()
        names = list()
        for f in self.dataSet.fmrNames:
            scipyLr0 = scipyLr[f]
            values = fmrX[f]
            linePlot, = plt.plot(years,
                        lineFunc(years, scipyLr0['B0'], scipyLr0['B1']),
                        '--', linewidth = 1)
            points, = plt.plot(years,
                        values,
                        '.', linewidth = 2)
            plots.append(linePlot)
            plots.append(points)
            names.append("{0} Bedroom LR (Slope: {1:.2f})".format(f[-1:], scipyLr0['B1']))
            names.append("{0} Bedroom Points".format(f[-1:]))

        plt.title("Fair Market Rent {0}, {1}".format(county, state))
        plt.xlabel('Year')
        plt.ylabel('Rent (USD)')
        plt.legend(plots, names, fontsize='x-small', loc='upper left')
        plt.show()

    def Map(self):
        m = Basemap(projection='cyl',  # stere, tmerc, lcc
                    lat_0=39.828127, lon_0=-98.579404,
                    urcrnrlon=-62.208289, urcrnrlat=51.342619,
                    llcrnrlon=-128.936426, llcrnrlat=19.06875)

        m.drawcoastlines()  # draw coastlines
        m.drawmapboundary()  # draw a line around the map region
        m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])  # draw parallels

        m.drawmeridians(np.arange(0., 420., 60.), labels=[0, 0, 0, 1])  # draw meridians

        m.drawstates()
        m.drawcountries()

        lon = list()
        lon.append(-80.633333)
        lon.append(-74.364684)
        lon.append(-75.387778)
        lon.append(-84.253333)

        lat = list()
        lat.append(28.116667)
        lat.append(40.715622)
        lat.append(40.043889)
        lat.append(30.455)

        m.scatter(lon, lat, latlon=True, c=np.random.rand(3))
        #m.pcolor(lon, lat, latlon=True)
        plt.title('United States Fair Market Rent')  # add a title
        plt.show()

    def MapData(self, year, fmrXBeds):
        """Using the specified data, this function will prepare and display a map of the United States
        which includes points on the map representing the data specified."""

        # Use a single figure for our map visualization
        if self.mapFigure == None:
            self.mapFigure = plt.figure()

        m = Basemap(projection='cyl',  # stere, tmerc, lcc
                    lat_0=39.828127, lon_0=-98.579404,
                    urcrnrlon=-62.208289, urcrnrlat=51.342619,
                    llcrnrlon=-128.936426, llcrnrlat=19.06875,
                    resolution="i")

        # Set up the basic map
        m.drawcoastlines()  # draw coastlines
        m.drawmapboundary()  # draw a line around the map region
        m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])  # draw parallels
        m.drawmeridians(np.arange(0., 420., 60.), labels=[0, 0, 0, 1])  # draw meridians

        m.drawstates()
        m.drawcountries()

        # prep data structures for mapping
        lon = list()
        lat = list()
        val = list()
        data = self.dataSet.yearData[year]

        # Convert data to structures, but skip where we don't have a lat/long
        for x in data:
            if x.latitude != None and x.longitude != None:
                lat.append(x.latitude)
                lon.append(x.longitude)
                val.append(getattr(x, fmrXBeds))

        m.scatter(lon, lat, latlon=True, c=val)
        #m.pcolor(lon, lat, latlon=True, data=val, tri=True)
        #m.contourf(lon, lat, val, latlon=True, tri=True)

        # Legend (remove if present, and add new)
        if self.colorbar != None:
            self.colorbar.remove()
        self.colorbar = plt.colorbar(orientation='vertical', shrink = 0.5)

        # Save for reuse.
        plt.title('United States Fair Market Rent - {0} Bedrooms - {1}'.format(fmrXBeds[-1:], year))
        plt.show()


def lineFunc(x, b0, b1):
    """Basic equation for a line."""
    y = list()
    for x1 in x:
        y.append(b0 + (b1 * x1))
    return y

def scipy_linearReg(x, y):
    """Calls the SciPy curve_fit function using a linear functional form"""
    popt, pcov = curve_fit(lineFunc, x, y)

    # Return the results in our standard dictionary structure
    results = {'n': float('nan'), 'xMean': float('nan'), 'yMean': float('nan'), 'B0': popt[0], 'B1':popt[1] }
    return results

def main():
    """Our main function."""
    root = Tk()

    app = App(root)
    root.mainloop()

    #root.destroy() # optional; see description below

# This is the main of the program.
if __name__ == "__main__":
    main()