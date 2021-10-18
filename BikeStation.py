import time

class BikeStation:

    #Initiate the Bike Station class
    def __init__(self, StationData):

        self.BikeStationID = StationData['id']
        self.Date = StationData['Date']
        self.Time = StationData['Time']
        self.StationName = StationData['station_name']
        self.TotalDocks = int(StationData['total_docks'])
        self.DockInService = int(StationData['docks_in_service'])
        #self.AvailableDocks = int(StationData['available_docks'])
        self.AvailableBikes = int(StationData['available_bikes'])
        self.Status = StationData['status']

        #Setter
        self.__RecordNo = StationData['record']

        #create position object for latitude and longtude
        self.Position = Position(StationData['latitude'], StationData['longitude'])

    @property
    def RecordNo(self):
        return self.__RecordNo

    @RecordNo.setter
    def RecordNo(self, RecordNo):
        try:
            Rec = str(RecordNo)
            if (Rec != ''):
                self.__RecordNo = Rec
            else:
                print('Invalid Record Field')
        except:
            return -1

    # Return the rounded percentage of docks available as an integer
    def PercentFull(self):
        try:
            TotalDocksInt = int(self.TotalDocks)
            AvailableBikesInt = int(self.AvailableBikes)
            PercentFull = AvailableBikesInt/TotalDocksInt * 100
            PercentFull = round(PercentFull)
            return PercentFull
        except:
            print('Invalid variable conversion to integer')

    # Return the number of available bikes in integer format
    def NumOfAvailableDocks(self):
        return self.DockInService - self.AvailableBikes

    #Return a string representation of the object
    def __str__(self):
        return self.StationName+" had "+str(self.AvailableBikes)+ " bikes on "+self.Date+' '+self.Time

# Class Position for Storage Latitude and Longitude
class Position:

    def __init__(self, latitude, longitude):
        self.Latitude = latitude
        self.Longitude = longitude

#Class to parse file data bdata.txt, Returns a list of bike objects
#Extra Feature that enhances Modularity by creating a FileParserMethod
class FileParser:

    # Argument is an open file handle
    def __init__(self, fh):
        self.fh = fh

    # Can take a custom list to search for any bike station. List contained in BikeStationIDs
    def ParseFile(self, BikeStationIDs):

        BikeStations = list()

        #Parse the file data and extract the data for bike stations 80, 88, 217, 346, 654, or custom list
        for line in self.fh:
            splitline = line.split('"')

            try:
                #Check if the bike station is in the list
                if (splitline[3] in BikeStationIDs):
                        bikedata = dict()
                        #Bike Station ID
                        bikedata[splitline[1]] = splitline[3]

                        #Parse Date and Time from TimeStamp
                        #bikedata[splitline[5]] = splitline[7]
                        DateTime = splitline[7].split('T')
                        bikedata['Date'] = DateTime[0]
                        bikedata['Time'] = DateTime[1].strip('.000')

                        #StationName
                        bikedata[splitline[9]] = splitline[11]
                        #TotalDocks
                        bikedata[splitline[13]] = splitline[15]
                        #DocksInService
                        bikedata[splitline[17]] = splitline[19]
                        #AvailableDocks
                        bikedata[splitline[21]] = splitline[23]
                        #AvailableBikes
                        bikedata[splitline[25]] = splitline[27]
                        #Status
                        bikedata[splitline[33]] = splitline[35]
                        #latitude
                        bikedata[splitline[37]] = splitline[39]
                        #longitude
                        bikedata[splitline[41]] = splitline[43]
                        #record number
                        bikedata[splitline[53]] = splitline[55]

                        #Create BikeStation object by passing a dictionary argument and appending the object it to the bikes lists
                        BikeStations.append(BikeStation(bikedata))
            except:
                continue

        self.fh.close()
        return(BikeStations)
    
def main():

    # Read Input from the file and parse the data for bike stations 80, 88, 217, 346, 654
    # Extra Feature, continues to ask for the filename if invalid. -1 to exit
    while(True):
        fname = input("Enter file name (-1 to exit): ")
        if(fname == '-1'):
            exit()
        if len(fname) < 1:
            fname = "bdata.txt"

        #Attempt to open the file and return an error if invalid
        try:
            fh = open(fname)
            break
        except:
            print('Please enter a valid filename')

    #Create FileParser object. Pass in file handle
    FileParserObj = FileParser(fh)
    BikeStationIDs = list()

    #Extra Feature to search for a custom bike station value. Increases the flexibility and modularity of the program
    while(True):
        try:
            CustomBikeStation = input('Input a station to search for (press enter to search the default assigned list): ')
            if(CustomBikeStation != ''):
                CustomBikeStationInt = int(CustomBikeStation)
                BikeStationIDs.append(CustomBikeStation)
                break
            else:
                BikeStationIDs = ['80', '88', '217', '346', '654']
                break
        except:
            print('Please enter an integer or press enter')

    #Pass File Handle to file parser with a list of custom or default BikeStationIDs
    BikeStations = FileParserObj.ParseFile(BikeStationIDs)

    if(len(BikeStations) == 0):
        print('Invalid bike station ID number')
        exit()

    TotalNumOfBikesAvail = 0
    TotalNumOfDocksAvail = 0
    StationIds = ''

    #Added print for formatting
    print()

    # Calculate the total number of bikes and docks available by iterating through the bike stations list
    for index in BikeStations:

        #Print string representation of Bike Station object
        print(index)
        TotalNumOfBikesAvail = index.AvailableBikes + TotalNumOfBikesAvail
        TotalNumOfDocksAvail = index.NumOfAvailableDocks() + TotalNumOfDocksAvail

        #Concatenate the Station IDs into one string for output
        if(StationIds != ''):
            StationIds = StationIds+', '+index.BikeStationID
        else:
            StationIds = index.BikeStationID

    #print the number of bikes available and their IDs.
    print('\nStation(s): ['+StationIds+'] Bikes Available '+str(TotalNumOfBikesAvail)+' Docks Available '+str(TotalNumOfDocksAvail))

    #Alternative method to print the string using print f
    #print(f'Station(s): [{StationIds}] Bikes Available {TotalNumOfBikesAvail} Docks Available {TotalNumOfDocksAvail}')

#Time of execution
#start_time = time.time()

if __name__ == "__main__":
    main()