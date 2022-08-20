import pandas as pd
from math import fabs




# set option to show all rows
pd.set_option('display.max_rows', None)

# set option to show all columns
pd.set_option('display.max_columns', None)



# index 0: SH_Codes
# index 1: DeclaredValues
# index 2: Tax_Codes
# index 3: Quantities
# index 4: Tax_Values

SH_Codes = 0
Quantities = 1
DeclaredValues = 2
CustomsDuty = 3
ForestTax = 4
PlasticTax = 5
ParafiscalTax = 6

# this function because : "if row[SH_Codes] in systemDF['SH_Codes']" is not working
def isIn(SH_Code, row):
    for i in row:
        if i == SH_Code:
            return True
    return False

def getMatches(ficheDF, systemDF, threshold):
    matches = []
    ("looking for matches...")
    # loop through each line in ficheDF and check if line is in systemDF
    for index, row in ficheDF.iterrows():

        #### check if SH_Code is in systemDF !! blocking in case of mismatched SH codes
        #if isIn(row[SH_Codes], systemDF['SH_Codes']):
            # get list of indexes of row in systemDF
            #indexList = systemDF[systemDF['SH_Codes'] == row[SH_Codes]].index
        #print(indexList)
        # loop through each index in indexList
        temp = []
        for i in range(len(systemDF)):
            if row[Quantities] == systemDF['Quantities'][i]:
                if fabs(row[DeclaredValues] - systemDF['Declared Values'][i]) < threshold:
                    # check for repeating matches[][0]
                    iList = [x[0] for x in matches]
                    if i in iList:
                        iPos = iList.index(i)
                        # get index of previous match
                        print(matches[iPos][1], index)
                        print("Checked",str(systemDF['SH_Codes'][i]), str(ficheDF['SH_Codes'][index]),i,index, "and", matches[iPos] ,matches[iPos][1])
                        if str(systemDF['SH_Codes'][i])[:4] == str(ficheDF['SH_Codes'][matches[iPos][1]])[:4]:
                            if str(systemDF['SH_Codes'][i])[:4] == str(ficheDF['SH_Codes'][index])[:4]:
                                # check declared values
                                alreadyDiff = fabs(ficheDF['Declared Values'][matches[iPos][1]] - systemDF['Declared Values'][i])
                                newDiff = fabs(ficheDF['Declared Values'][index] - systemDF['Declared Values'][i])
                                if  newDiff < alreadyDiff:
                                    matches[iPos][1] = index
                                    print("replaced:", iPos[1], index)
                        elif str(systemDF['SH_Codes'][i])[:4] == str(ficheDF['SH_Codes'][index])[:4]:
                            print(i, index)
                            matches[iPos]= [i, index]
                        else:
                            print("none of them matches HS code")

                    # check for repeating matches[][1]
                    iList = [x[1] for x in matches]
                    if index in iList:
                        iPos = iList.index(index)
                        # get index of previous match
                        print(matches[iPos][0], i)
                        #print("Checked",str(systemDF['SH_Codes'][i])[:4], str(ficheDF['SH_Codes'][index])[:4])
                        if str(ficheDF['SH_Codes'][index])[:4] == str(systemDF['SH_Codes'][matches[iPos][0]])[:4]:
                            if str(ficheDF['SH_Codes'][index])[:4] == str(systemDF['SH_Codes'][i])[:4]:
                                # check declared values
                                alreadyDiff = fabs(ficheDF['Declared Values'][matches[iPos][0]] - systemDF['Declared Values'][i])
                                newDiff = fabs(ficheDF['Declared Values'][index] - systemDF['Declared Values'][i])
                                if  newDiff < alreadyDiff:
                                    matches[iPos][0] = i
                        elif str(ficheDF['SH_Codes'][index])[:4] == str(systemDF['SH_Codes'][i])[:4]:
                                print(i, index)
                                matches[iPos]= [i, index]
                        else:
                            print("none of them matches HS code")
                    else:
                        matches.append([i, index])
                        print("added: ", i, index)
    return matches



def getCorrected(ficheDF, systemDF):
    corrected = []
    # correct errors in DeclaredValues and Tax_Values and Quantities
    for index, row in ficheDF.iterrows():
        # check if SH_Code is in systemDF
        if isIn(row[SH_Codes], systemDF['SH_Codes']):
            # get list of indexes of row in systemDF
            indexList = systemDF[systemDF['SH_Codes'] == row[SH_Codes]].index
            # loop through each index in indexList
            for i in indexList:
                # check if Tax_Code is equal to systemTax_Code
                if row[Tax_Codes] == systemDF['Tax_Codes'][i]:
                    # replace systemDeclaredValue with ficheDeclaredValue
                    systemDF['DeclaredValues'][i] = row[DeclaredValues]
                    # replace systemTax_Value with ficheTax_Value
                    systemDF['Tax_Values'][i] = row[Tax_Values]
                    # replace systemQuantity with ficheQuantity
                    systemDF['Quantities'][i] = row[Quantities]
                    # save i and index into corrected list
                    #print("Corrected: " + str(index) + " " + str(i))
                    corrected.append([i, index])
                    break
    return corrected




def getGroups(ficheDF, systemDF, threshold):
    # the algorithm:
    # count number of lines left, each line is a bit for a binary number, loop through each number in binary and check if sumQuantity is equal to systemQuantity
    # if sumQuantity is equal to systemQuantity, check if sumDeclaredValue is close enough to systemDeclaredValue
    # then get current binary number and add it to matches list
    # if sumQuantity is not equal to systemQuantity, go to next binary

    # count number of lines left
    linesLeftFiche = ficheDF.shape[0]
    linesLeftSys = systemDF.shape[0]
    groups = []

    #print(linesLeftFiche)
    #print(2**linesLeftSys)

    # loop through each lineLeft in ficheDF
    # get even numbers smaller than 2**linesLeftFiche
    even = [1]
    odd = []
    for i in range(2, 2**linesLeftFiche):
        if i % 2 == 0:
            even.append(i)
        else:
            odd.append(i)
    path = even + odd
    i = 0

    linesLeftAfterFiche = linesLeftFiche
    while i < len(path) and linesLeftAfterFiche > 0:
        #if 
        ficheBinary = bin(path[i])[2:]
        while len(ficheBinary) < linesLeftFiche:
            ficheBinary = "0" + ficheBinary
        ficheSumQuantity = 0
        ficheSumDeclaredValue = 0
        for k in range(len(ficheBinary)):
            if ficheBinary[k] == "1":
                ficheSumQuantity += ficheDF['Quantities'][k]
                ficheSumDeclaredValue += ficheDF['Declared Values'][k]
        # loop through each binary number
        for j in range(1, 2**linesLeftSys):
            # get binary representation of j
            sysBinary = bin(j)[2:]
            while len(sysBinary) < linesLeftSys:
                sysBinary = '0' + sysBinary
            #print("Checking configuration: " , sysBinary)
            # get sumQuantity
            sumQuantity = 0
            for k in range(linesLeftSys):
                if sysBinary[k] == '1':
                    # add quantity to sumQuantity
                    sumQuantity += systemDF['Quantities'][k]
            # check if sumQuantity is equal to systemQuantity
            if sumQuantity == ficheSumQuantity:
                # get sumDeclaredValue
                sumDeclaredValue = 0
                for k in range(linesLeftSys):
                    if sysBinary[k] == '1':
                        # add quantity to sumDeclaredValue
                        sumDeclaredValue += systemDF['Declared Values'][k]
                # check if sumDeclaredValue is close enough to systemDeclaredValue
                if abs(sumDeclaredValue - ficheSumDeclaredValue) < threshold:
                    # get current sysBinary number
                    currentsysBinary = '0b' + sysBinary
                    # add currentsysBinary to matches list
                    groups.append([currentsysBinary, ficheBinary])
                    break
        i += 1



        print("Progress: " + str(i) + " / " + str(2 ** linesLeftFiche))
    return groups


def removeMatches(matches, ficheDF, systemDF):
    # remove matches from ficheDF and systemDF
    for i in matches:
        #print(i)
        print("removing: ", i[0], i[1])
        ficheDF = ficheDF.drop(i[1])
        systemDF = systemDF.drop(i[0])

    # reset index
    ficheDF.reset_index(drop=True, inplace=True)
    systemDF.reset_index(drop=True, inplace=True)
    return ficheDF, systemDF


def removeCorrected(corrected, ficheDF, systemDF):
    # remove corrected from ficheDF and systemDF
    for i in corrected:
        ficheDF = ficheDF.drop(i[1])
        systemDF = systemDF.drop(i[0])
    # reset index
    ficheDF.reset_index(drop=True, inplace=True)
    systemDF.reset_index(drop=True, inplace=True)
    return ficheDF, systemDF

def removeGroups(ficheDF, systemDF):
    # remove matches from ficheDF and systemDF
    for i in groups:
        for c in i[0]:
            if c == "1":
                systemDF.drop(i[0].index(c) - 2, inplace=True)
        ficheDF.drop(i[1], inplace=True)
    # reset index
    ficheDF.reset_index(drop=True, inplace=True)
    systemDF.reset_index(drop=True, inplace=True)
    return ficheDF, systemDF


def getDeviationFromGroups(groups, ficheDF, systemDF):
    deviation = 0
    for i in groups:
        # get binary representation of group
        binary = i[0][2:]
        sumTaxValue = 0
        for j in range(len(binary)):
            if binary[j] == '1':
                # add quantity to sumTaxValue
                sumTaxValue += ficheDF['Tax_Values'][j]
        # get systemTaxValue
        systemTaxValue = systemDF['Tax_Values'][i[1]]
        # calculate deviation
        deviation += abs(sumTaxValue - systemTaxValue)
    return deviation


# is this function needed?
def getDeviationFromFicheAndSystem(ficheDF, systemDF):
    deviation = 0
    for i in range(ficheDF.shape[0]):
        # get sumTaxValue
        sumTaxValue = ficheDF['Tax_Values'][i]
        # get systemTaxValue
        systemTaxValue = systemDF['Tax_Values'][i]
        # calculate deviation
        deviation += abs(sumTaxValue - systemTaxValue)
    return deviation


def calculateDeviation(ficheDF, systemDF, groups):
    # get deviation from groups
    deviation = getDeviationFromGroups(groups, ficheDF, systemDF)
    print("Deviation: " + str(deviation))


def main():
    ficheDF = pd.read_excel("output.xlsx")
    systemDF = pd.read_excel("outputsys.xlsx")

    print(ficheDF)

    # drop columns from systemDF
    systemDF.drop(['Dried Plants Tax %', 'Customs Duty %', 'Forest Tax %', 'Plastic Tax %', 
        'Parafiscal Tax %', 'Sum of Dried Plants Tax Amount'], axis=1, inplace=True)

    # print number of rows in systemDF
    print("Number of rows in systemDF: " + str(systemDF.shape[0]))

    matches = getMatches(ficheDF, systemDF, 200)
    print("Matches: ", matches)

    ficheDF, systemDF = removeMatches(matches, ficheDF, systemDF)
    print(ficheDF)
    print(systemDF)


    corrected = [] #getCorrected(ficheDF, systemDF)
    print("Corrected: ", corrected)
    #ficheDF, systemDF = removeCorrected(corrected, ficheDF, systemDF)

    #print("FicheDF: ", ficheDF)
    #print("SystemDF: ", systemDF)

    groups = getGroups(ficheDF, systemDF, 100)
    print("Groups: ", groups)
    #removeGroups(groups, ficheDF, systemDF)

    print("FicheDF: ", ficheDF)
    print("SystemDF: ", systemDF)

    print("Number of rows in systemDF: " + str(systemDF.shape[0]))
    
    matches2 = getMatches(ficheDF, systemDF, 200)
    print("Matches: ", matches2)


    #calculateDeviation(ficheDF, systemDF, groups)
    
main()