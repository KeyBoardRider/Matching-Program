import pandas as pd
import tabula as tab


# Read pdf into list of DataFrame

#dfs = tab.read_pdf(r'Fiche.pdf', pages='all')

#print(dfs)


SH_Codes = []
Dec_Values = []
Quantities = []
Taxes = []
Customs_Tax = [] #000110 000120 000130
Forest_Tax = [] #004400
Plastic_Tax = [] #004801
Parafiscal_Tax = [] #007217
Custom_V = []


#print dataframe

#extract text from dict file and save it in a list
def get_text(dfs):
    text = []
    for z in range (len(dfs)):
        for i in range(len(dfs[z]['data'])):
            for j in range(len(dfs[z]['data'][0])):
                text.append(dfs[z]['data'][i][j]["text"])

    

    #remove "!" from text
    for i in range(len(text)):
        for j in range(len(text[i])-3):
            #check if string includes ! and remove it
            if text[i][j:j+2] == "! ":
                text[i] = text[i][:j] + text[i][j+2:]


    return text



def filterExclamationPoints(text):
    if "!" in text:
        textList = list(text)
        textList.remove("!")
        text = "".join(textList)    
    return text

def sort(text):
    #check if string includes NUMERO SH 
    #if yes, sort the list
    #if no, sort the list

    for i in range(len(text)):
        if text[i].find("NUMERO SH") != -1:
            #Get SH Codes
            #find 9 digits after NUMERO SH
            Count = 0
            Temp=[]
            for j in range(len(text[i])):
                if Count != 11:
                    if text[i][j].isdigit():
                        Temp.append(text[i][j])
                        Count += 1
                        #print (Temp)
                    else:
                        Count = 0
                        Temp = []
                if len(Temp) == 10:
                    SH_Codes.append(''.join(Temp))

    #Get Declared Values
    
        if text[i].find("VALEUR :") != -1:
            #find digits after VALEUR :
            Count = int(text[i].index("VALEUR :"))
            Temp=[]
            
            while Count < len(text[i]):
                if text[i][Count].isdigit():
                    Temp.append(text[i][Count])
                    if text[i][Count+1] == ",":
                        Temp.append(".")
                        Count += 1
                Count += 1
                    

            if len(Temp) == 0:
                for j in range(len(text[i+1])-1):
                    if text[i+1][j] == ' ' or text[i+1][j] == '!':
                        text[i+1] = text[i+1].replace(text[i+1][j], '')
                        print("in the if: " , text[i+1])
                    #if text[i+1][j] == ',':
                    #    text[i+1][j] = text[i+1].replace(text[i+1][j], '.')
                                  
                Dec_Values.append(text[i+1])
            else:
                Dec_Values.append(''.join(Temp))

            
    #Get QUANTITE 
        if text[i].find("QUANTITE :") != -1:
            #find digits after QUANTITE :
            Count = int(text[i].index("QUANTITE :"))
            Temp=[]

            while Count < len(text[i]):
                #print(Count, len(text[i]))
                if text[i][Count] == ".":
                    Temp.append(text[i][Count])

                if text[i][Count].isdigit():
                    Temp.append(text[i][Count])

                Count += 1
            if len(Temp) != 0:
                Quantities.append(''.join(Temp))

    #Get Customs Tax
    ArticleCount=0
    i=0
    while text[i].find("RECAPITULATION") == -1:
        Temp = []
        if text[i].find("NUMERO SH") != -1:
            ArticleCount += 1
        if text[i].find("000110") != -1 or text[i].find("000120") != -1:
            Customs_Tax.append(ArticleCount)
            while text[i].find("-----------------------------------------------------------------------") == -1:
                
                for j in range(len(text[i])):
                    if text[i][j].isdigit():
                        Temp.append(text[i][j])
                    if text[i][j] == ".":
                        Temp.append(text[i][j])
                    if text[i][j] == ",":
                        Temp.append(".")
                    if text[i][j] == "!":
                        if len(Temp) != 0:
                            Customs_Tax.append(''.join(Temp))
                            Temp = []
                i+=1
        elif text[i].find("000110") != -1:
            print ("-------------------------------WARNING---------------------------------")
            print ("Article " + str(ArticleCount) + " in Fiche has a 0130 Tax.")
            print ("-----------------------------------------------------------------------")


        i+=1
        
    #Get Forest Tax
    ArticleCount=0
    i=0
    while text[i].find("RECAPITULATION") == -1:
        Temp = []
        if text[i].find("NUMERO SH") != -1:
            ArticleCount += 1
        if text[i].find("004400") != -1 :
            Forest_Tax.append(ArticleCount)
            while text[i].find("-----------------------------------------------------------------------") == -1:
                
                for j in range(len(text[i])):
                    if text[i][j].isdigit():
                        Temp.append(text[i][j])
                    if text[i][j] == ".":
                        Temp.append(text[i][j])
                    if text[i][j] == ",":
                        Temp.append(".")
                    if text[i][j] == "!":
                        if len(Temp) != 0:
                            Forest_Tax.append(''.join(Temp))
                            Temp = []
                i+=1
        i+=1

    
    #Get Plastic Tax
    ArticleCount=0
    i = 0
    while text[i].find("RECAPITULATION") == -1:
        Temp = []
        if text[i].find("NUMERO SH") != -1:
            ArticleCount += 1
        if text[i].find("004801") != -1:
            Plastic_Tax.append(ArticleCount)
            while i< len(text) and text[i].find("-----------------------------------------------------------------------") == -1:
                
                for j in range(len(text[i])):
                    if text[i][j].isdigit():
                        Temp.append(text[i][j])
                    if text[i][j] == ".":
                        Temp.append(text[i][j])
                    if text[i][j] == ",":
                        Temp.append(".")
                    if text[i][j] == "!":
                        if len(Temp) != 0:
                            Plastic_Tax.append(''.join(Temp))
                            Temp = []
                i+=1
        i+=1

    #Get Parafiscal Tax
    ArticleCount=0
    i = 0
    while text[i].find("RECAPITULATION") == -1:
        Temp = []
        if text[i].find("NUMERO SH") != -1:
            ArticleCount += 1
        if text[i].find("007217") != -1:
            Parafiscal_Tax.append(ArticleCount)
            while i< len(text) and text[i].find("-----------------------------------------------------------------------") == -1:
                
                for j in range(len(text[i])):
                    if text[i][j].isdigit():
                        Temp.append(text[i][j])
                    if text[i][j] == ".":
                        Temp.append(text[i][j])
                    if text[i][j] == ",":
                        Temp.append(".")
                    if text[i][j] == "!":
                        if len(Temp) != 0:
                            Parafiscal_Tax.append(''.join(Temp))
                            #print(Temp)
                            Temp = []
                i+=1
        i+=1
       

def output():
    #table = [["SH_Codes"],["Quantities"],["Declared Value"],["Customs Duty"],["Forest Tax"],["Plastic Tax"],["Parafiscal Tax"]]
    table = [[],[],[],[],[],[],[]]
    #add SH Codes to table
    for i in range(len(SH_Codes)):
        table[0].append(SH_Codes[i])
    #add Quantities to table
    for i in range(len(Quantities)):
        table[1].append(Quantities[i])
    #add Declared Value to table
    for i in range(len(Dec_Values)):
        table[2].append(Dec_Values[i])
    
    #add Customs Tax to table
    for i in range(len(SH_Codes)):
        Temp = []
        for j in range(len(Customs_Tax)):
            if i+1 == Customs_Tax[j]:
                Temp.append(Customs_Tax[j+4])
        if len(Temp) == 0:
            table[3].append('0')
        else:
            table[3].append(Temp[0])
    
    #print(Custom_V)

    #add Forest Tax to table
    for i in range(len(SH_Codes)):
        Temp = []
        for j in range(len(Forest_Tax)):
            if i+1 == Forest_Tax[j]:
                Temp.append(Forest_Tax[j+4])
        if len(Temp) == 0:
            table[4].append('0')
        else:
            table[4].append(Temp[0])

    #add Plastic Tax to table
    for i in range(len(SH_Codes)):
        Temp = []
        for j in range(len(Plastic_Tax)):
            if i+1 == Plastic_Tax[j]:
                Temp.append(Plastic_Tax[j+4])
                print(Plastic_Tax[j+4])
        if len(Temp) == 0:
            table[5].append('0')
        else:
            table[5].append(Temp[0])


    #add Parafiscal Tax to table
    
    for i in range(len(SH_Codes)):
        Temp = []
        for j in range(len(Parafiscal_Tax)):
            if i+1 == Parafiscal_Tax[j]:
                Temp.append(Parafiscal_Tax[j+4])

        if len(Temp) == 0:
            table[6].append('0')
        else:
            table[6].append(Temp[0])

    for i in range(len(table[2])):
        table[2][i] = filterExclamationPoints(table[2][i])


    for i in range(len(table[2])):
        # replace comma with dot
        table[2][i] = float(table[2][i].replace(",","."))

    
    #table = [["SH_Codes"],["Quantities"],["Declared Value"],["Customs Duty"],["Forest Tax"],["Plastic Tax"],["Parafiscal Tax"]]
    extractedData = pd.DataFrame({"SH_Codes": table[0], "Quantities": table[1], "Declared Values": table[2], "Customs Duty": table[3], "Forest Tax" : table[4], "Plastic Tax" : table[5], "Parafiscal Tax": table[6]})

    extractedData.to_excel("output.xlsx", index=False)

    return table



def sortFiche():
    dfs = tab.read_pdf(r'C:\Users\Oussama\Desktop\Excel-Matching-master\Fiche.pdf', output_format= 'json', encoding='cp1252', guess = False,pages = 'all')

    text = get_text(dfs)
    sort(text)

    output()
    print("Fiche Sorted")


if __name__ == "__main__":
    sortFiche()