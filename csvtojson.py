#!/usr/bin/python3

import re
import os
import sys
import pprint
import json

# MAIN
# C:\dev\batch_engine\Batch\September2014\2014.5.1\Sep_2014_Set1.csv
if __name__ == "__main__":
    
    # Get the csv file.
    print(">>> csvtojson.py is used to generate a json from the .csv file generated in batch.py")
    print(">>> It is assumed here you already have run batch.py to make this .csv file.")
    inputCSV = (input(">>> Input Full Path to .csv File generated from batch.py: ")).strip()
    # searchList = ['ARTIST', 'TITLE', 'STEPARTIST']

    """
    For now just assume the following indices:
    0 - Folder Name (Useless)
    1 - Song Artist
    2 - Stepper
    3 - Song Title
    """
    fullPath = inputCSV
    fileDir = os.path.abspath(os.path.join(os.path.dirname(fullPath), '.'))
    csvFile = os.path.basename(os.path.normpath(fullPath))
    batchName = str(csvFile.split(".csv")[0])
    outputFile = batchName + ".json"

    # Data structure for the JSON is a dictionary.
    batchJson = {}
    batchJson[batchName] = [] # Batch Name will be key, Will be an array of objects

    # Parse the file
    os.chdir(fileDir)  # Change to csv file directory context
    with open(csvFile) as fileCSV:
        for line in fileCSV:
            if line.startswith('[FOLDER]'):
                continue
            songToAdd = {}
            lineValues = line.split(",")  # CSV file separates fields by commas
            songTitle = lineValues[3].strip()
            songArtist = lineValues[1].strip()
            stepArtist = lineValues[2].strip()
            if songTitle == "":
                songTitle = lineValues[0].strip()  # First CSV column is ALWAYS folder name
            if songArtist == "":
                songArtist = "UNKNOWN"  # this is a way of indicating files where artist names weren't parsed

            # Now time to add this to the dictionary as an object
            songToAdd['title'] = songTitle
            songToAdd['artist'] = songArtist
            songToAdd['stepper'] = stepArtist
            songToAdd['status'] = "unjudged"
            songToAdd['latest'] = "none"
            songToAdd['batch'] = batchName
            batchJson[batchName].append(songToAdd)
            
            # stringToPrint = "Title: " + songTitle + " >>> Artist: " + songArtist + " >>> Stepper: " + stepArtist
            # print(stringToPrint)
    fileCSV.close()

    # Print out the "JSON" for now
    # print(batchJson)

    # Write out the JSON.
    print(">>> Writing JSON file for " + batchName)
    with open(outputFile, 'w') as outFile:
        json.dump(batchJson, outFile, indent=4)
    outFile.close()
    print(">>> Successfully wrote JSON file.")













# nope
