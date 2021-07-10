'''
Fields needed:
For all:

Title: 
- Person's Name
Subject:
- If MAIN table: same sentence for all women: "???"
Description:
- Notes field + Biographical Note if one exists
Creator:
- Prompted by program. (ex: Pauline Arnoud)
Source:
- Empty for now
Publisher
- Empty for now
Date:
- Date at which the file was converted
Contributor:
- Empty for now
Rights:
- Empty for now
Relation:
Name of the table represented (MAIN, relationships, activities, etc...)
Format:
- Empty for now
Language:
English
Type Identifier
Coverage
Tags: 
- Last name of the associated women (for tables other than MAIN)
- Table type (ex: relationships, activities, collections, objects, etc...)

For Person (main and relationships tables):
    Birth Date
    Birthplace
    Death Date
    Occupation
    Biographical Text: text in the Notes section for now.
    Bibliography
    - Empty for now

For Event (activities tables):
Duration: 
- Start Date - End Date
Event Type:
- Type of Activity "as a" Position in "Location"

For Hyperlink (sources table):
URL: link to internet resource if it exists

'''

import csv
import sys
import datetime

def main():
    inputFile = input("What file do you want to convert? ")
    outputFile = input("To what file do you want to write the converted csv file? ")
    main = input("File with the SUN_ID and the women associated with them: ")
    tableTypes = ["main", "relationships", "activities", "objects", "collections", "sources"]
    tableType = input("What table type is this? (Options:" + ' '.join(tableTypes) + "): ")
    while (str(tableType) not in tableTypes):
        tableType = input("Wrong input. Here are the options:" + ' '.join(tableTypes) + ": ")

    creator = input("Who is creating this file? ")

    with open(inputFile, "r") as file, open(main, "r") as main_d, open(outputFile, "w") as outFile:
        reader = csv.DictReader(file, delimiter = ',')
        main = csv.DictReader(main_d, delimiter = ",")
        writer = csv.writer(outFile, delimiter = ',')

        header = ['Dublin Core:Title', 'Dublin Core:Subject', 'Dublin Core:Description', 'Dublin Core:Creator', 'Dublin Core:Relation', 'Dublin Core:Language', 'Dublin Core:tags']
        if (tableType == "relationships" or tableType == "main"):
            header.extend(["Item Type Metadata:Birth Date", "Item Type Metadata:Birthplace", "Item Type Metadata:Death Date", "Item Type Metadata:Occupation", "Item Type Metadata:Biographical Text"])
        if (tableType == "activities"):
            header.extend(["Item Type Metadata:Duration", "Item Type Metadata:Event Type"])
        if (tableType == "sources"):
            header.extend(["Item Type Metadata:URL", "Item Type Metadata:Publication Date", "Item Type Metadata:Citation"])

        writer.writerow(header)
        lineCount = 0

        #setting up the dictionary with the S_ID and their associated women
        s_id = {}
        for row in main:
            fullName = ((row["First"] + ' ' + row["Middle"] + ' ' + row["Surname"] + ' ' + row["Married Surname 1"] + ' ' + row["Married Surname 2"] + ' ' + row["Married Surname 3"]).replace("  ", " ").strip())
            s_id[row["S_ID"]] = fullName

        #reading through each line in the input file and converting it to a row for the output file.
        for row in reader:
            rowVals = []
            if (tableType == "main"):
                fullName = s_id[row["S_ID"]]
            elif (tableType == "relationships"):
                fullName = ((row["First"] + ' ' + row["Middle"] + ' ' + row["Last"]).replace("  ", " ").strip())
            elif (tableType == "activities"): 
                #fullName = ("Project of " + s_id[row["S_ID"]]).replace("  ", " ").strip()
                if row["Type of Activity"] == "Trip":
                    location = row["Location"].split(";")[-1]
                    fullName = ((row["Type of Activity"] + " as a " + row["Position"] + " to " + location).replace("  ", " ").strip())
                elif row["Type of Activity"] == "Job":
                    fullName = ((row["Type of Activity"] + " as " + row["Position"] + " at the " + row["Activity/Organization Name"]).replace("  ", " ").strip())
                elif row["Type of Activity"] == "Project":
                    fullName = ((row["Position"] + " for the " + row["Activity/Organization Name"] + ' ' + row["Type of Activity"]).replace("  ", " ").strip())
                elif row["Type of Activity"] == "Education":
                    fullName = ((row["Position"] + " at " + row["Activity/Organization Name"] + ' ' + row["Type of Activity"]).replace("  ", " ").strip())
                else:
                    fullName = ((row["Position"] + " of the " + row["Activity/Organization Name"]).replace("  ", " ").strip())
            elif (tableType == "sources"):
                fullName = row["Title"]
            else: 
                fullName = ""
            rowVals.append(fullName)
            if (tableType == 'relationships'):
                rowVals.append(s_id[row["S_ID"]] + "'s " + row["Nature of Relationship"])
            else:
                rowVals.append('')
            if (tableType == "main"):
                rowVals.append(row["Biographical Note"])
            if (tableType == 'sources'):
                if row["Type of Source"] != '' and row["Author"] != '' and row["Publication"] != '':
                    rowVals.append(row["Type of Source"] + " by " + row["Author"] + " (" + row["Publication"] + ")")
                elif row["Type of Source"] == '':
                    if row["Author"] != '' and row["Publication"] != '':
                        rowVals.append("by " + row["Author"] + " (" + row["Publication"] + ")")
                    elif row["Author"] == '':
                        rowVals.append("by " + row["Publication"])
                    else:
                        rowVals.append(" by " + row["Author"])
                elif row["Author"] == '':
                    if row["Publication"] != '':
                        rowVals.append(row["Type of Source"] + " by " + row["Publication"])
                    else:
                        rowVals.append(row["Type of Source"])
            else:
                rowVals.append("")  #for Biographical Text. We'll change this later once we have something to put.
            rowVals.append(creator)
            rowVals.append(tableType)
            rowVals.append("English")
            rowVals.append(row["S_ID"])

            if (tableType == "relationships" or tableType == "main"):
                rowVals.append(row["Date of Birth"])
                rowVals.append(row["Place of Birth"])
                rowVals.append(row["Date of Death"])
                rowVals.append(row["Profession"].replace("/", "+"))
                rowVals.append('')    #should be NOTES, but note field not yet ready

            if (tableType == "activities"):
                duration = row["Start Date"] + "-" + row["End Date"]
                if (duration == "-"):
                    duration = ""
                rowVals.append(duration)
               # eventType = row["Activity/Organization Name"] + " as a " + row["Position"] + " in " + row["Location"]
                eventType = row["Position"] + " of " + row["Activity/Organization Name"] + " (in " + row["Location"] + ")."
                rowVals.append(eventType)

            if (tableType == "sources"):
                URL = row["Link"]
                rowVals.append(URL)
                rowVals.append(row["Publication Date"])
                rowVals.append(row["Citations"])

            lineCount += 1

            writer.writerow(rowVals)
            print(rowVals)

        print("Processed", lineCount, "rows.")


if __name__ == '__main__':
    main()
