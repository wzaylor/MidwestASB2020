"""
The purpose of this script is to parse the file that was exported from formstack.

Follow these steps before running this script:
    1) Export an Excel file from formstack
    2) Open the file in excel, and 'save as' a .csv file
        - Specify that tabs are the delimiter for the file.
"""
import numpy as np

def main():
    fileName = 'ASB2020_RegistrationForm_Data_1583770019.csv'
    parseFormstackCsvFile(fileName)
    return

def parseFormstackCsvFile(fileName):
    """
    Parse the given .csv file.

    This function parses the given .csv file into a dictionary.
    The first row of this file defines the file defines the keys to the dictionary.
    The remaining rows define the values that go into the entries.

    ..NOTE:: If an entry is empty, then '' will be the value.

    :param fileName: string, The name of the .csv file that is being parsed.
    :return: dict, A dictionary with the parsed data
    """
    with open(fileName, mode='r') as fl:
        lines = fl.readlines()


    headings = lines[0].replace('"', '') # Remove double quotation marks from the headings.
    headings = headings.split('\t') # Separate the headings into a list, using a comma as a delimiter.
    data = {}

    for i in range(len(headings)): # Iterate over the headings
        data[headings[i]] = [] # Initilize the entry in 'data' as an empty list

    for i in range(1, len(lines)):
        line = lines[i].replace('"', '')  # Remove double quotation marks from the entries.
        line = line.split('\t') # Separate the line into a list, using a comma as a delimiter.
        for j in range(len(headings)): # Iterate over the headings
            data[headings[j]].append(line[j]) # Append the value to the appropriate entry in 'data'
    return data

if __name__ == '__main__':
    main()