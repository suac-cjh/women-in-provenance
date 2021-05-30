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
    if (len(sys.argv) < 5):
        print("Not enough arguments. Please enter: input file, output file, main file, table type (ex: input.csv, output.csv, MAIN.csv, relationships")
    args = sys.argv[1:]
    input = args[0]
    output = args[1]
    main = args[2]
    tableType = args[3]

    with open(input, "r") as file, open(main, "r") as main_d, open(output, "w") as outFile:
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
            rowVals.append("Pauline Arnoud")
            rowVals.append(tableType)
            rowVals.append("English")
            lineCount += 1

            writer.writerow(rowVals)
            print(rowVals)

        print("Processed", lineCount, "names.")


if __name__ == '__main__':
    main()
