'''
Fields needed:
For all:

Title: Person's Name
Subject:
- If MAIN table: same sentence for all women: "???"
Description:
- Leave empty for now
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
Tags: Last name of the associated women (for tables other than MAIN)

For Person:
Birth Date
Birthplace
Death Date
Occupation
Biographical Text: text in the Notes section for now.
Bibliography
- Empty for now
'''

import csv
import sys
import datetime

def main():
    inputFile = "input.csv" #input("What file do you want to convert? ")
    outputFile = "output.csv" #input("To what file do you want to write the converted csv file?")
    main = "input.csv" #input("File with the SUN_ID and the women associated with them")
    tableTypes = ["main", "relationships", "activities", "objects", "collections", "sources"]
    tableType = input("What table type is this? (Options:" + ' '.join(tableTypes) + "): ")
    while (str(tableType) not in tableTypes):
        tableType = input("Wrong input. Here are the options:" + ' '.join(tableTypes) + "): ")

    creator = input("Who is creating this file? ")

    with open(inputFile, "r") as file, open(main, "r") as main_d, open(outputFile, "w") as outFile:
        reader = csv.DictReader(file, delimiter = ',')
        main = csv.reader(main_d, delimiter = ",")
        writer = csv.writer(outFile, delimiter = ',')

        header = ['Dublin Core:Title', 'Dublin Core:Subject', 'Dublin Core:Description', 'Dublin Core:Creator', 'Dublin Core:Relation', 'Dublin Core:Language']

        writer.writerow(header)

        lineCount = 0

        for row in reader:
            rowVals = []
            fullName = ((row["First"] + ' ' + row["Middle"] + ' ' + row["Married Surname 1"] + ' ' + row["Married Surname 2"] + ' ' + row["Married Surname 3"]).replace("  ", " ").strip())
            rowVals.append(fullName)
            if (tableType == 'relationships'):
                rowVals.append(fullName + "'s" + row["Nature of Relationship"])
            else:
                rowVals.append('')
            rowVals.append(row["Notes"])
            rowVals.append(creator)
            rowVals.append(tableType)
            rowVals.append("English")
            lineCount += 1

            writer.writerow(rowVals)
            print(rowVals)

        print("Processed", lineCount, "names.")


if __name__ == '__main__':
    main()
