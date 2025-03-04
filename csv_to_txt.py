'''
This program will convert a CSV file to a text file.
The main purpose is to re-use the Movielens dataset and visualise it using
a graph and the tSNE software.

Quentin Deligny
'''

from pathlib import Path
from utility_functions import *
from omdb import get_metadata
import csv
import numpy as np

#Some rows are poorly formatted an run over multiple lines
def concat_rows(rows):
    i = 0
    for row in rows:
        if(row[0].isnumeric()) is not True:
            rows[i-1] = rows[i-1] + rows[i]
            del rows[i]
        
        i += 1

    return(rows)

#Some rows are poorly formatted with multiple entries per line
def reduce_row(row):
    
    reduceRow = ''
    for i in range(len(row)):
        reduceRow += row[i]

    return([reduceRow])


def assignMovieTitle100kData(file,fileTitles,fileIds):

    listOfIds = []
    listOfTitles = []
    with open(file, "r") as outputFile:
        for row in csv.reader(outputFile):

            currentRowId = ''
            currentRowTitleYear = ''
            i = 0
            
            #each row is a list containing 1 string, however some contain multiple entries
            row = reduce_row(row)
            
            while (row[0][i] != '|'):
                currentRowId += row[0][i]
                i += 1

            i += 1
            while (row[0][i] != '|'):
                currentRowTitleYear += row[0][i]
                i += 1
                
            listOfIds += [int(currentRowId)]
            listOfTitles += [currentRowTitleYear]

    outputFile.close()
    
    listOfTitles = stripYears(listOfTitles)


    with open(fileTitles, 'w') as f:
        for item in listOfTitles:
            f.write("%s\n" % item)
    f.close()
                
    with open(fileIds, 'w') as d:
        for item in listOfIds:
            d.write("%s\n" % item)
    d.close()
    

    
def assignMovieGenre(fileOldFormat,fileTitles,fileGenres):
    
    #Stores all the rows within the dataset
    allRows = []
    #Only stores rows whose id is found in the movieIdArray
    with open(fileOldFormat, "r",encoding = 'utf8') as outputFile:
        for row in csv.reader(outputFile):
            
            if 'movieId title genres' in row:
                continue
            
            if(len(row)>1):
                row = reduce_row(row)

            allRows += row
            
    outputFile.close()
    
    rows = concat_rows(allRows)
    rowTitles, rowGenres = stripRows(rows)

    allTitles100k = []
    allGenres100k = []
    
    #We now load the rows from the 100k dataset to assign genres to them
    with open(fileTitles, "r") as outputFile:
        for row in csv.reader(outputFile):
            allTitles100k += row
    outputFile.close()    

    #If the genre is not in the 1M Dataset, we try to extract it from OMDb
    print("Extracting Genre Metadata...")
    for title in allTitles100k:
        if title in rowTitles:
            k = rowTitles.index(title)
            titleGenre = rowGenres[k]
        else:
            try:
                title = cleanString(title)
                metadata = get_metadata([title],True, False)
                titleGenre = metadata[0][3]
            except:
                titleGenre = "None"
        
        allGenres100k += [titleGenre]
    print("Finished Extracting Genre Metadata.\n")
    
    with open(fileGenres, 'w') as d:
        for item in allGenres100k:
            d.write("%s\n" % item)
    d.close()
    

def getMovieTitleGenre(file, file2,arrayOfIds,allSingleGenre):
    '''
    Returns arrays of titles and genres (only one genre per item).
    file: file containing all titles
    file2: file containing all ids
    arrayOfIds: array for which we want to return titles and genres
    allSingleGenre: array containing all genres for each item (one per item)
    '''
    #selectedTitles = []
    allTitles = []
    selectedGenres = []
    
    
    allIds = []
    with open(file2, "r") as outputFile:
        for row in csv.reader(outputFile):
            allIds += [row]
    outputFile.close()

    
    for currentId in arrayOfIds:
        k = allIds.index([currentId])
        #selectedTitles += allTitles[k]
        selectedGenres += [allSingleGenre[k]]
        
    return selectedGenres
        
                
def assignMovieIds (ratings,titleFile,idFile):
    
    userRatings = np.asarray(ratings)
    titles = userRatings[0::2]
    ratedIds = []
    allRowTitles = []
    allIds = []
    
    with open(titleFile, "r") as outputFile:
        for row in csv.reader(outputFile):
            allRowTitles += row
    outputFile.close()
    with open(idFile, "r") as outputFile2:
        for row in csv.reader(outputFile2):
            allIds += row
    outputFile2.close()

    for title in titles:
        k = allRowTitles.index(title)
        movieId = allIds[k]
        ratedIds += [movieId]

    return (ratedIds,userRatings[1::2])

def assignSingleLabel(movieIdArray,idFile, fileGenres,showNone):
    '''
    movieIdArray: Array of integers with the IDs of Movies that need to be assigned labels.
    file: name of the file where the labels & movie IDs are stored independently.
    showNone: if True, show movies with no corresponding label in the movielens dataset.
    showMultiple: if True, plot will show movies with multiple labels by assigning them only one label.
    
    Returns movieGenreArray, an array of labels corresponding to the movieIdArray
    '''

    #List all 18 distinct genres for the movies
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    #Single Label Assignment will favour labels in the order they are listed
    possibleGenres = ['Action','Adventure','Animation','Children','Comedy','Crime',
                      'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
                      'Mystery','Romance','Sci-Fi','Thriller','War','Western']

    genresToColours = {'Action':'cornflowerblue',
                       'Adventure':'darkgrey',
                       'Animation':'lightcoral',
                       'Children':'red',
                       'Comedy':'orangered',
                       'Crime':'saddlebrown',
                       'Documentary':'orange',
                       'Drama':'darkgoldenrod',
                       'Fantasy':'gold',
                       'Film-Noir':'darkkhaki',
                       'Horror':'yellow',
                       'Musical':'yellowgreen',
                       'Mystery':'lawngreen',
                       'Romance':'aqua',
                       'Sci-Fi':'darkblue',
                       'Thriller':'indigo',
                       'War':'violet',
                       'Western':'deeppink',
                       'None':'black'}
    #This array will only contain the required labels
    idsToReturn = []
    movieGenreArray = []
    genresAsColours = []

    #Both arrays will have the same length, containing the entire data from the loaded file.
    movieIdArray = []
    with open(idFile, "r") as outputFile2:
        for row in csv.reader(outputFile2):
            movieIdArray += row
    outputFile2.close()

    arrayOfGenres = []
    with open(fileGenres, "r") as outputFile2:
        for row in csv.reader(outputFile2):
            arrayOfGenres += [row]
    outputFile2.close()

    print(len(arrayOfGenres))
    for i in range(len(arrayOfGenres)):
        if(len(arrayOfGenres[i])>1):
            arrayOfGenres[i]=reduce_row(arrayOfGenres[i])
            
        currentGenres = arrayOfGenres[i][0]

        #used to add the first genre in the possible genres
        alphabeticalOrder = True
        for genre in possibleGenres:
            if genre in currentGenres and (alphabeticalOrder):
                arrayOfGenres[i] = genre
                alphabeticalOrder = False
            elif(currentGenres=="N/A") or (currentGenres=="Short"):
                arrayOfGenres[i] = "None"

    for i in range(len(arrayOfGenres)):
        elem = arrayOfGenres[i]
        if(type(elem)==list):
            arrayOfGenres[i] = "None"
                            
    #Array no longer contains multiple genres
    for label in arrayOfGenres:
        genresAsColours += [genresToColours[label]]

        
    return(genresAsColours, movieIdArray, arrayOfGenres)
            
        
        
    

def csvToText(inputFile, outputFile):
    csv_file1 = "ml-latest-small/movies.csv"
    txt_file1 = "ml-latest-small/movielens_movies.txt"

    with open(txt_file1, "w",encoding = 'utf8') as my_output_file:
        with open(csv_file1, "r",encoding = 'utf8') as my_input_file:
            for row in csv.reader(my_input_file):
                my_output_file.write(" ".join(row)+'\n')
            
        print('File Successfully written.')
        my_output_file.close()



