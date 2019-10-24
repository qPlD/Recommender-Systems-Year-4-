'''
This program will convert a CSV file to a text file.
The main purpose is to re-use the Movielens dataset and visualise it using
a graph and the tSNE software.

Quentin Deligny
'''

from pathlib import Path
#from spotlight.validator import Validator
import csv
import numpy as np


def assignSingleLabel(movieIdArray, file):
    '''
    movieIdArray: Array of integers with the IDs of Movies that need to be assigned labels.
    file: name of the file where the labels & movie IDs are stored independently.
    
    Returns movieGenreArray, an array of labels corresponding to the movieIdArray
    '''

    #List all 18 distinct genres for the movies
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    #Single Label Assignment will favour labels in the order they are listed
    possibleGenres = ['Action','Adventure','Animation','Children','Comedy','Crime',
                      'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
                      'Mystery','Romance','Sci-Fi','Thriller','War','Western']
    #This array will only contain the required labels
    movieGenreArray = []

    #Both arrays will have the same length, containing the entire data from the loaded file.
    arrayOfIds = []
    arrayOfGenres = []

    with open(file, "r",encoding = 'utf8') as outputFile:
        for row in csv.reader(outputFile):
            rowId = ''
            i = 0
            while (row[0][i]) in numbers:
                rowId += row[0][i]
                i+=1
            
            arrayOfIds += [rowId]

            for block in row:
                for genre in possibleGenres:
                    if genre in block:
                        rowgenre = genre
                        break

            arrayOfGenres += [genre]

        outputFile.close()
        
        for movieId in movieIdArray:
            idString = str(movieId)
            
            if idString in arrayOfIds:
                idIndex = arrayOfIds.index(idString)
                label = arrayOfGenres[idIndex]

            #Dataset IDs are not sequential, so the movieID may not be found
            else:
                label = "None"

            movieGenreArray += [label]

    return(movieGenreArray)
            
        
        
    

def csvToText(inputFile, outputFile):

    with open(txt_file1, "w",encoding = 'utf8') as my_output_file:
        with open(csv_file1, "r",encoding = 'utf8') as my_input_file:
            for row in csv.reader(my_input_file):
                my_output_file.write(" ".join(row)+'\n')
            
        print('File Successfully written.')
        my_output_file.close()

#data_folder = Path("ml-latest-small/")
csv_file1 = "ml-latest-small/movies.csv"
txt_file1 = "ml-latest-small/movielens_movies.txt"
#csvToText(csv_file1,txt_file1)

#testIds = [4,63,4460,216,34]
#print(testIds,assignSingleLabel(testIds,txt_file1))
    



