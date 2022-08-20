import pandas as pd

# set option to show all rows
pd.set_option('display.max_rows', None)

# set option to show all columns
pd.set_option('display.max_columns', None)

ficheDF = pd.read_excel("output.xlsx")
systemDF = pd.read_excel("outputsys.xlsx")

# drop columns from systemDF
systemDF.drop(['Dried Plants Tax %', 'Customs Duty %', 'Forest Tax %', 'Plastic Tax %', 
    'Parafiscal Tax %', 'Sum of Dried Plants Tax Amount'], axis=1, inplace=True)

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

def isIn(SH_Code, row):
    for i in row:
        if i == SH_Code:
            return True
    return False

def dvCheck():
    temp1=0
    for i in range(len(ficheDF[2])):
        temp1 += ficheDF[2][i]
    print (temp1)
    
    temp2=0
    for i in range(len(ficheDF[2])):
        temp2 += systemDF[2][i]
    print (temp2)



dvCheck()
