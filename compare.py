import pandas as pd
from math import fabs
from pandas import ExcelWriter





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

def getMatches(ficheDF, systemDF,acceptableVar):
    matches = []
    ("looking for matches...")
    # loop through each line in ficheDF and check if line is in systemDF
    for index, row in ficheDF.iterrows():
 
        # loop through each index in indexList
        temp = []
        for i in range(len(systemDF)):
            threshold = systemDF['Declared Values'][i] * acceptableVar
            if row[Quantities] == systemDF['Quantities'][i]:
                if fabs(row[DeclaredValues] - systemDF['Declared Values'][i]) < threshold:
                    # check for repeating matches[][0]
                    iList = [x[0] for x in matches]
                    if i in iList: 
                        if i in iList:
                            iPos = iList.index(i)
                            # get index of previous match
                            prevMatch = matches[iPos]
                            nextMatch = [i, index]
                            if str(systemDF['SH_Codes'][nextMatch[0]])[:4] == str(ficheDF['SH_Codes'][prevMatch[1]])[:4]:
                                if str(systemDF['SH_Codes'][nextMatch[0]])[:4] == str(ficheDF['SH_Codes'][nextMatch[1]])[:4]:
                                    # check declared values
                                    newDiff = fabs(ficheDF['Declared Values'][index] - systemDF['Declared Values'][i])
                                    alreadyDiff = fabs(ficheDF['Declared Values'][prevMatch[1]] - systemDF['Declared Values'][i])
                                    if  newDiff < alreadyDiff and index not in [x[1] for x in matches]:
                                        matches[iPos][1] = index
                            elif str(systemDF['SH_Codes'][nextMatch[0]])[:4] == str(ficheDF['SH_Codes'][nextMatch[1]])[:4]:
                                matches[iPos]= [i, index]
                            else:
                                print("none of them matches HS code")

                    elif index in [x[1] for x in matches]:
                        # check for repeating matches[][1]
                        iList = [x[1] for x in matches]
                        if index in iList:
                            iPos = iList.index(index)
                            # get index of previous match
                            prevMatch = matches[iPos]
                            nextMatch = [i, index]    
                            if str(ficheDF['SH_Codes'][nextMatch[1]])[:4] == str(systemDF['SH_Codes'][prevMatch[0]])[:4]:
                                if str(ficheDF['SH_Codes'][nextMatch[1]])[:4] == str(systemDF['SH_Codes'][nextMatch[0]])[:4]:
                                    # check declared values
                                    alreadyDiff = fabs(ficheDF['Declared Values'][prevMatch[0]] - systemDF['Declared Values'][nextMatch[0]])
                                    newDiff = fabs(ficheDF['Declared Values'][index] - systemDF['Declared Values'][i])
                                    if  newDiff < alreadyDiff and i not in [x[0] for x in matches]:
                                        matches[iPos][0] = i
                            elif str(ficheDF['SH_Codes'][nextMatch[1]])[:4] == str(systemDF['SH_Codes'][nextMatch[0]])[:4]:
                                    matches[iPos]= [i, index]
                            else:
                                print("none of them matches HS code")

                    else:
                        matches.append([i, index])
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
                    corrected.append([i, index])
                    break
    return corrected


def removeGroups(group, ficheDF, systemDF):
    # remove matches from ficheDF and systemDF
    
    for j in range(2, len(group[0])):
        if group[0][j] == "1":
            systemDF.drop(j - 2, inplace=True)

    for j in range(len(group[1])):
        if group[1][j] == "1":
            ficheDF.drop(j, inplace=True)
    # reset index
    ficheDF.reset_index(drop=True, inplace=True)
    systemDF.reset_index(drop=True, inplace=True)   
    return ficheDF, systemDF


def extractDataFromGroup2(group, ficheDF, systemDF):
    extractedData = [[], []]
    for i in range(2, len(group[0])):
        if group[0][i] == "1":
            extractedData[0].append(systemDF.iloc[i-2])

    for i in range(len(group[1])):
        if group[1][i] == "1":
            extractedData[1].append(ficheDF.iloc[i])
    
    return extractedData


def getDeviationFromSavedData(save):
    dCustomsDuty = 0
    dForestTax = 0
    dPlasticTax = 0
    dParafiscalTax = 0
    dTotal = 0


    leftSide = save[0]
    rightSide = save[1]

    for x in leftSide:
        dCustomsDuty += x['Customs Duty']
        dForestTax += x['Forest Tax']
        dPlasticTax += x['Plastic Tax']
        dParafiscalTax += x['Parafiscal Tax']
    
    for x in rightSide:
        dCustomsDuty -= x['Customs Duty']
        dForestTax -= x['Forest Tax']
        dPlasticTax -= x['Plastic Tax']
        dParafiscalTax -= x['Parafiscal Tax']

    return [dCustomsDuty, dForestTax, dPlasticTax, dParafiscalTax]


def getDeviationFromGroups(save):
    groupDeviations = []
    for group in save:
        groupDeviations.append(getDeviationFromSavedData(group))

    #print("---------------------- Devation from groups ----------------------------")
    #print("dCustomsDuty: ", groupDeviations[0][0])
    #print("dForestTax: ", groupDeviations[0][1])
    #print("dPlasticTax: ", groupDeviations[0][2])
    #print("dParafiscalTax: ", groupDeviations[0][3])
    #print("-----------------------------------------------------------------------")

    return groupDeviations

def getGroups(ficheDF, systemDF, threshold):
    # the algorithm:
    # count number of lines left, each line is a bit for a binary number, loop through each number in binary and check if sumQuantity is equal to systemQuantity
    # if sumQuantity is equal to systemQuantity, check if sumDeclaredValue is close enough to systemDeclaredValue
    # then get current binary number and add it to matches list
    # if sumQuantity is not equal to systemQuantity, go to next binary

    sumCustomDuty = 0
    sumForestTax = 0
    sumPlasticTax = 0
    sumParafiscalTax = 0
    # count number of lines left
    linesLeftFiche = ficheDF.shape[0]
    linesLeftSys = systemDF.shape[0]
    groups = []
    deviation = 0

    save = []

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
        linesLeftFiche = ficheDF.shape[0]
        linesLeftSys = systemDF.shape[0]

        # loop through each lineLeft in ficheDF
        # get even numbers smaller than 2**linesLeftFiche
        #even = [1]
        #odd = []
        #for j in range(2, 2**linesLeftFiche):
        #    if i % 2 == 0:
        #        even.append(j)
        #    else:
        #        odd.append(j)
        #path = even + odd

        linesLeftAfterFiche = linesLeftFiche
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
                    print(groups)
                    # save data from current group
                    #save.append(extractDataFromGroup(groups[-1], ficheDF, systemDF))
                    save.append(extractDataFromGroup2(groups[-1], ficheDF, systemDF))
                    #getDeviationFromSavedData(save[-1], groups, ficheDF, systemDF)

                    ficheDF, systemDF = removeGroups(groups[-1], ficheDF, systemDF)

                    linesLeftAfterFiche = ficheDF.shape[0]
                    i = 0
                    
                    break
        i += 1



        #print("Group Data: \n", save[-1])
        print("Progress: " + str(i) + " / " + str(2 ** linesLeftFiche))
    return groups, ficheDF, systemDF, deviation , save


def removeMatches(matches, ficheDF, systemDF):
    # remove matches from ficheDF and systemDF
    print (matches)
    for i in matches:
        ficheDF = ficheDF.drop(i[1])
        systemDF = systemDF.drop(i[0])

    # reset index
    ficheDF.reset_index(drop=True, inplace=True)
    systemDF.reset_index(drop=True, inplace=True)
    return ficheDF, systemDF


def getDeviationFromFicheAndSystem(ficheDF, systemDF):
    ficheTotalDeclaredValue = 0
    sumCustomDuty = 0
    sumForestTax = 0
    sumPlasticTax = 0
    sumParafiscalTax = 0

    totalDeviation = 0
    matchesDeviation = 0

    # get system total declared value
    #systemTotalDeclaredValue = int(systemDF['Declared Values']).sum()


    # get fiche total declared value
    for i in range(len(ficheDF)):
        ficheTotalDeclaredValue += int(ficheDF['Declared Values'][i])
    
    print ("ficheTotalDeclaredValue: " + str(ficheTotalDeclaredValue))

    # get taxes from system
    for i in range(systemDF.shape[0]):
        sumCustomDuty += systemDF['Customs Duty'][i]
        sumForestTax += systemDF['Forest Tax'][i]
        sumPlasticTax += systemDF['Plastic Tax'][i]
        sumParafiscalTax += systemDF['Parafiscal Tax'][i]
        
    #get taxes from fiche
    for i in range(ficheDF.shape[0]):
        # get sumTaxValue
        sumCustomDuty -= ficheDF['Customs Duty'][i]
        sumForestTax -= ficheDF['Forest Tax'][i]
        sumPlasticTax -= ficheDF['Plastic Tax'][i]
        sumParafiscalTax -= ficheDF['Parafiscal Tax'][i]


    # calculate total deviation
    totalDeviation = sumCustomDuty + sumForestTax + sumPlasticTax + sumParafiscalTax
    
    print("Deviation: " + str(totalDeviation))
    print("Customs Duty: " + str(sumCustomDuty))
    print("Forest Tax: " + str(sumForestTax))
    print("Plastic Tax: " + str(sumPlasticTax))
    print("Parafiscal Tax: " + str(sumParafiscalTax))

    return totalDeviation, sumCustomDuty, sumForestTax, sumPlasticTax, sumParafiscalTax

def getDeviationFromMatches(match,ficheDF,systemDF):
    devMatch = []
    #Get deviation from matches and store the matches with deviation in a list:
        # Calculate allowable variation threshold
    CDThreshold = 0.04 * (ficheDF['Declared Values'][match[1]] + systemDF['Declared Values'][match[0]]) / 2
    FTThreshold = 0.04 * (ficheDF['Declared Values'][match[1]] + systemDF['Declared Values'][match[0]]) / 2
    PTThreshold = 0.04 * (ficheDF['Declared Values'][match[1]] + systemDF['Declared Values'][match[0]]) / 2
    PFThreshold = 0.025 * (ficheDF['Declared Values'][match[1]] + systemDF['Declared Values'][match[0]]) / 2

    # Get system tax values

    devFlag = 0
    # get difference in tax rate
    CDDevRate = systemDF['Customs Duty'][match[0]]/systemDF['Declared Values'][match[0]] - ficheDF['Customs Duty'][match[1]] / ficheDF['Declared Values'][match[1]]
    FTDevRate = systemDF['Forest Tax'][match[0]]/systemDF['Declared Values'][match[0]] - ficheDF['Forest Tax'][match[1]] / ficheDF['Declared Values'][match[1]]
    PTDevRate = systemDF['Plastic Tax'][match[0]]/systemDF['Declared Values'][match[0]] - ficheDF['Plastic Tax'][match[1]] / ficheDF['Declared Values'][match[1]]
    PFDevRate = systemDF['Parafiscal Tax'][match[0]]/systemDF['Declared Values'][match[0]] - ficheDF['Parafiscal Tax'][match[1]] / ficheDF['Declared Values'][match[1]]

    CDDev = systemDF['Customs Duty'][match[0]]- ficheDF['Customs Duty'][match[1]]
    FTDev = systemDF['Forest Tax'][match[0]] - ficheDF['Forest Tax'][match[1]]
    PTDev = systemDF['Plastic Tax'][match[0]] - ficheDF['Plastic Tax'][match[1]]
    PFDev = systemDF['Parafiscal Tax'][match[0]] - ficheDF['Parafiscal Tax'][match[1]]

    if fabs(CDDevRate) > 0.001 and abs(CDDev) > CDThreshold:
        devFlag = 1

    if fabs(FTDevRate) > 0.001 and abs(FTDev) > FTThreshold:
        devFlag = 1

    if fabs(PTDevRate) > 0.001 and abs(PTDev) > PTThreshold:
        devFlag = 1

    if  fabs(PFDevRate) > 0.001 and abs(PFDev) > PFThreshold:
        devFlag = 1
    if devFlag == 1:
        devMatch.append(match)
        devMatch.append(CDDev)
        devMatch.append(FTDev)
        devMatch.append(PTDev)
        devMatch.append(PFDev)

    return devMatch 

    #return deviation #, sumCustomDuty, sumForestTax, sumPlasticTax, sumParafiscalTax

#report the mismatched SH Codes
#def SHMismatch()

# show mismatched SH Codes in matches and groups
def showMismatches1(matches, ficheDF, systemDF):
    print("-------------------Mismatched SH Codes (one to one):-------------------")
    for i in matches:
        if ficheDF['SH_Codes'][i[1]] != systemDF['SH_Codes'][i[0]]:
            print(systemDF['SH_Codes'][i[0]], " ",  ficheDF['SH_Codes'][i[1]])
    print("-----------------------------------------------------------------------")

def showMismatches2(save, ficheDF, systemDF):

    print("---------------------Mismatched SH Codes (n to n'):---------------------")
    for group in save:
        for element in group[0]: 
            for j in range(2, len(element)):
                if str(element)[j] == 1:
                    for k in range(len(group[1])):
                        if str(group[1])[k] == 1:
                            if ficheDF['SH_Codes'][j-2] != systemDF['SH_Codes'][k]:
                                print(systemDF['SH_Codes'][j-2], " ",  ficheDF['SH_Codes'][k])
    print("-----------------------------------------------------------------------")

def groupsToExcel(save):
    startrow = None
    # create excel file
    writer = pd.ExcelWriter('Deviation.xlsx', mode = 'a',engine="openpyxl",if_sheet_exists="replace")
    # write to excel file
    # blank dataframe
    groupsDeviation = getDeviationFromGroups(save)
    system = ["Invoice data"]
    fiche = ["Fiche data"]
    deviation = ["Deviation"]
    space = [" "]
    groupDFfinal = pd.DataFrame()
    count = 0
    for group in save: 
        groupDFfinal = groupDFfinal.append(["-------------------------------------------------------"])
        groupDFfinal = groupDFfinal.append(system)
        groupDFfinal = groupDFfinal.append(group[0])
        groupDFfinal = groupDFfinal.append(fiche)
        groupDFfinal = groupDFfinal.append(group[1])
        groupDFfinal = groupDFfinal.append(deviation)
        groupDeviationDF = pd.DataFrame(groupsDeviation[count])
        groupDeviationDF = groupDeviationDF.transpose()
        # rename columns of groupDeviationDF
        groupDeviationDF.columns = ['Customs Duty', 'Forest Tax', 'Plastic Tax', 'Parafiscal Tax']
        groupDFfinal = groupDFfinal.append(groupDeviationDF)
        count += 1
        # append blank line
        groupDFfinal = groupDFfinal.append(pd.DataFrame())

        # try to open an existing workbook

    groupDFfinal.to_excel(writer, sheet_name="Combinations Deviation" , index=False)
    writer.save()
    writer.close()
    print("Excel file updated")
    return

def matchesToExcel(matches, ficheDF, systemDF):
    writer = pd.ExcelWriter('Deviation.xlsx')
    writeDF = pd.DataFrame()

    for match in matches:
        tempFiche = pd.DataFrame(ficheDF.loc[match[1]])
        tempSys = pd.DataFrame(systemDF.loc[match[0]])

        ficheDFToWrite = pd.DataFrame(ficheDF.loc[match[1]])
        systemDFToWrite = pd.DataFrame(systemDF.loc[match[0]])
        deviation = getDeviationFromMatches(match, ficheDF, systemDF)
        if deviation == []:
            deviationDF = pd.DataFrame({'Description': ['No deviation']})

        else:
            writeDF = writeDF.append(["-------------------------------------------------------"])
            deviationDF = pd.DataFrame({'Description': ['Deviation']})
            deviationDF['Customs Duty'] = deviation[1]
            deviationDF['Forest Tax'] = deviation[2]
            deviationDF['Plastic Tax'] = deviation[3]
            deviationDF['Parafiscal Tax'] = deviation[4]

            # turn rows into columns
            ficheDFToWrite = ficheDFToWrite.transpose()
            systemDFToWrite = systemDFToWrite.transpose()
            # add columns named Description to ficheDFToWrite and systemDFToWrite
            ficheDescription = ["Fiche Data: "]
            systemDescription = ["System Data: "]

            print(ficheDFToWrite)

            ficheDFToWrite.insert(0, 'Description', ficheDescription, True)
            systemDFToWrite.insert(0, 'Description', systemDescription, True)

            # write Invoice Data in Description column
            writeDF = writeDF.append(ficheDFToWrite)
            writeDF = writeDF.append(systemDFToWrite)
            # concat deviation
            writeDF = pd.concat([writeDF, deviationDF])


    writeDF.to_excel(writer, sheet_name="One to One Deviation")
    writer.save()
    writer.close()


def compare():
    ficheDF = pd.read_excel("output.xlsx")
    systemDF = pd.read_excel("outputsys.xlsx")
    devMatches = []


    print("Fiche: ", ficheDF)
    print("System: ", systemDF)

    # drop columns from systemDF
    systemDF.drop(['Dried Plants Tax %', 'Customs Duty %', 'Forest Tax %', 'Plastic Tax %', 
        'Parafiscal Tax %', 'Sum of Dried Plants Tax Amount'], axis=1, inplace=True)

    # print number of rows in systemDF
    print("Number of rows in systemDF: " + str(systemDF.shape[0]))

    print("--------------------------Total Deviation--------------------------")
    print("totalDeviation, sumCustomDuty, sumForestTax, sumPlasticTax, sumParafiscalTax")
    print(getDeviationFromFicheAndSystem(ficheDF, systemDF))
    print("-------------------------------------------------------------------")

    matches = getMatches(ficheDF, systemDF, 0.25)
    matchesToExcel(matches,ficheDF,systemDF)

    # Display matches deviation
    count = 0
    for i in range(len(matches)):
        if getDeviationFromMatches(matches[i],ficheDF,systemDF) != []:
            devMatches.append(getDeviationFromMatches(matches[i],ficheDF,systemDF))


            print("-------------------Deviation from Matches--------------------")

            print("Deviation: ", devMatches[count])
            print("System side: ", (systemDF.loc[devMatches[count][0][0]]))
            print("Fiche side: ", ficheDF.loc[devMatches[count][0][1]])

            print("-------------------------------------------------------------")
            count += 1
    

    #ficheDF, systemDF = removeCorrected(corrected, ficheDF, systemDF)

    # output mismatched SH Codes in matches  
    showMismatches1(matches, ficheDF, systemDF)

    ficheDF, systemDF = removeMatches(matches, ficheDF, systemDF)

    groups, ficheDF, systemDF , groupsDeviation, save= getGroups(ficheDF, systemDF, 500)

    # output mismatched SH Codes in groups
    showMismatches2(save, ficheDF, systemDF)

    print("Fiche: ", ficheDF)
    print("System: ", systemDF)

    print("-------------------Deviation from Remaining--------------------")
    print(getDeviationFromFicheAndSystem(ficheDF, systemDF))
    print("---------------------------------------------------------------")

    print("Number of rows in systemDF: " + str(systemDF.shape[0]))

    #Output mismatched SH Codes in matches and groups
    #showMismatches(matches, groups, ficheDF, systemDF, save)

    #Output groups to excel file
    groupsToExcel(save)

    #calculateDeviation(ficheDF, systemDF, groups)
    