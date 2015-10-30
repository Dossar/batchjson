#!/usr/bin/python3

import pprint
import json
import os
import sys
import time

# MAIN
# C:\dev\batch_engine\Batch\September2014\jsons
if __name__ == "__main__":

    # Create prettyprinter object
    pp = pprint.PrettyPrinter(indent=4)

    # Prompt the user for the jsons directory.
    print(">>> combinejsons.py looks through a jsons directory that has individual "
          "json files representing song batch sets and combines all of them into "
          "one big json.")

    # Retrieve the list of json files in the directory.
    jsonsDirectory = ""
    jsons = []
    overallTime = 0.0
    while True:
        try:
            
            # Retrieve json directory from user
            jsonsDirectory = (input(">>> Input full path to jsons directory: ")).strip()
            outputJson = os.path.join(jsonsDirectory, "batches.json")
            try:
                os.remove(outputJson)
            except:
                pass
            jsonsFiles = os.listdir(jsonsDirectory)
            break
        except:
            print(">>> combinejsons.py: {0}: {1}".format(sys.exc_info()[0].__name__,
                                                         str(sys.exc_info()[1])))

    # For every listed json file, add it to the jsons list.
    print(">>> combinejsons.py: ASSIGN: Assigning Id's to " + str(len(jsonsFiles))+ " batches.")
    start = time.time()
    idCounter = 0 # Id's start at zero to make indexing easier.
    for jsonPath in jsonsFiles:
        jsonFilePath = os.path.join(jsonsDirectory, jsonPath)
        with open(jsonFilePath) as jsonFile:
            
            # Load in JSON contents.
            data = json.load(jsonFile)
            batch = data.keys()

            # Before appending this json data, assign id's to every chart.
            for key in batch:
                for song in data[key]:
                    song['idNum'] = idCounter
                    idCounter += 1

            # Now append the json.
            jsons.append(data)
            
        jsonFile.close()
    end = time.time()
    elapsed = end - start
    overallTime += elapsed
    print(">>> combinejsons.py: ASSIGN: Successfully assigned " + (str(idCounter)) + " Id's in " + str(round(elapsed,3)) + " seconds.")

    # Now combine the jsons by getting each song pack and having the pack name as a key.
    print(">>> combinejsons.py: COMBINE: Combining Batch JSONs together...")
    start = time.time()
    allBatchesJson = {}
    for jsonBatch in jsons:
        try:
            batch = jsonBatch.keys()
            for key in batch:
                data = jsonBatch[key]
                batchName = data[0]['batch']
                allBatchesJson[batchName] = data
            # batchName = jsonBatch[0]['batch']
            # allBatchesJson[batchName] = jsonBatch
        except:
            print(">>> combinejsons.py: COMBINE: {0}: {1}".format(sys.exc_info()[0].__name__,
                                                                  str(sys.exc_info()[1])))
    end = time.time()
    elapsed = end - start
    overallTime += elapsed
    print(">>> combinejsons.py: COMBINE: Combining took " + str(round(elapsed,3)) + " seconds.")

    # Now that we've got all the keys for the song packs and each has its song charts, write out the json.
    print(">>> combinejsons.py: WRITE: Attempting to write all batches JSON...")
    start = time.time()
    with open(outputJson, 'w') as jsonOut:
        json.dump(allBatchesJson, jsonOut, indent=4) # Uncomment this line if you want a nicely formatted JSON.
        ## json.dump(allBatchesJson, jsonOut) # No nice spacing for JSON, results in smaller file size
    jsonOut.close()
    end = time.time()
    elapsed = end - start
    overallTime += elapsed
    print(">>> combinejsons.py: WRITE: JSON written succesfully in " + str(round(elapsed,3)) + " seconds.")
    print(">>> combinejsons.py: Total Elapsed Time: " + str(round(overallTime,3)) + " seconds.")
    






# NOPE
