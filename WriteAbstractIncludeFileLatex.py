"""
The purpose of this script is to write a latex file that includes the abstracts located in the specified directory.
"""
import os

# Custom functions
import ParseFormstackExportFile
import GetAbstractFiles

def main():
    latexOutputFileName = 'AbstractBook/AbstractInclude.tex' # The name of the latex file that is output by this script

    formstackExportFileName = 'ASB2020_RegistrationForm_Data_1583770019.csv' # The formstack file with '\t' as the delimiter.
    parsedData = ParseFormstackExportFile.parseFormstackCsvFile(formstackExportFileName) # Parse the formstack file/
    abstractDirectory = 'Abstracts' # The directory that contains the folders of the downloaded abstract files

    numEntries = len(parsedData['Time'])  # Define the number of rows in the parsedData dictionary entries.

    latexTxt = '%%%%%%%%%%\n' # Initialize the string that will be written to a latex file

    for i in range(numEntries):
        abstractUrl = parsedData['Abstract'][i]
        uniqueId = parsedData['Unique ID'][i]
        authorName = f'{parsedData["Name (Last)"][i]}, {parsedData["Name (First)"][i]}'

        # Check if an abstract exists for the ith entry.
        if 'http' not in abstractUrl: # Check if the entry is not empty. If so, then continue to the next iteration
            continue
        if parsedData['No Presentation'][i] == 'Yes': # Check if the person specified 'Yes' for the 'No Presentation' option. If so, then continue to the next iteration
            continue

        abstractFileNameFixed = GetAbstractFiles.fixAbstractFileName(abstractUrl.split("/")[-1]) # Removed extra periods '.' from the filename
        abstractFileName = f'{abstractDirectory}{os.sep}{uniqueId}{os.sep}{abstractFileNameFixed}' # Define the abstract file's name that includes the path to 'uniqueAbstractDirectory'

        if os.path.exists(abstractFileName) is True: # Check if the 'downloadFileName' exists
            if '.pdf' not in abstractFileNameFixed: # Usually the person uploaded a .docx file
                latexTxt += f'% \index{{{authorName}}}\n% \includepdf[pages=1-, pagecommand={{}}]{{../{abstractFileName}}}\n\n'
            else:
                latexTxt += f'\index{{{authorName}}}\n\includepdf[pages=1-, pagecommand={{}}]{{../{abstractFileName}}}\n\n'

    with open(latexOutputFileName, mode='w') as fl:
        fl.write(latexTxt)

    return

if __name__ == '__main__':
    main()