"""
The purpose of this script is to download abstract .pdf files from the given urls and place them in the appropriate directory.
"""

import requests
import os

# Custom functions
import ParseFormstackExportFile


def main():
    fileName = 'ASB2020_RegistrationForm_Data_1583770019.csv' # The formstack file with '\t' as the delimiter.
    parsedData = ParseFormstackExportFile.parseFormstackCsvFile(fileName) # Parse the formstack file/
    abstractDirectory = 'Abstracts' # The directory that will contain the folders of the downloaded abstract files

    numEntries = len(parsedData['Time']) # Define the number of rows in the parsedData dictionary entries.

    for i in range(numEntries):
        abstractUrl = parsedData['Abstract'][i]
        uniqueId = parsedData['Unique ID'][i]

        # Check if an abstract exists for the ith entry.
        if 'http' not in abstractUrl: # Check if the entry is not empty. If so, then continue to the next iteration
            continue
        if parsedData['No Presentation'][i] == 'Yes': # Check if the person specified 'Yes' for the 'No Presentation' option. If so, then continue to the next iteration
            continue

        uniqueAbstractDirectory = f'{abstractDirectory}{os.sep}{uniqueId}' # Define a new directory based in the 'uniqueId'
        abstractFileName = fixAbstractFileName(abstractUrl.split("/")[-1]) # Get the abstract's filename from the url
        downloadFileName = f'{uniqueAbstractDirectory}{os.sep}{abstractFileName}' # Define the abstract file's name that includes the path to 'uniqueAbstractDirectory'

        if os.path.exists(uniqueAbstractDirectory) is False: # Check if the 'uniqueAbstractDirectory' exists
            os.mkdir(uniqueAbstractDirectory)
        else: # If the directory exists, then throw an error and exit.
            raise AssertionError(f'ERROR, directory {uniqueAbstractDirectory} already exists!')
        downloadAndWriteFile(abstractUrl, downloadFileName)
    return

def fixAbstractFileName(originalFileName):
    """
    Remove any periods '.' from the file name (except the extension), and replace them with underscores '_'

    :param originalFileName: string, The abstract's orignal fileName
    :return: string, The abstract's filename with the periods replaced with underscores (except the extension)
    """
    fileName0 = originalFileName.split('.')
    fileNameWithoutExtension = '_'.join(fileName0[:-1])
    fixedFileName = f'{fileNameWithoutExtension}.{fileName0[-1]}'
    return fixedFileName

def downloadAndWriteFile(fileUrl, fileName):
    """
    Download the file that is located at the given url and download it to the given fileName
    :param fileUrl: string, The URL to the file that is being downloaded
    :param fileName: string, The name of the file that is being downloaded. This usually includes the path to the file name
    :return:
    """
    response = requests.get(fileUrl)  # create HTTP response object

    # send a HTTP request to the server and save
    # the HTTP response in a response object called 'response'
    with open(fileName, 'wb') as f: # Saving received content binary format
        # write the contents of the response (response.content) to a new file in binary mode.
        f.write(response.content)

    return

if __name__ == '__main__':
    main()