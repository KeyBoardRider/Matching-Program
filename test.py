import pandas as pd

dataset = pd.read_excel("matching.xlsx")

# set option to show all rows
pd.set_option('display.max_rows', None)

# set option to show all columns
pd.set_option('display.max_columns', None)

# display dataframe
#print(dataset)

columns = []

print("Default settings are: ")
# open default.txt file
with open("default.txt", "r") as f:
    # read each line
    for line in f:
        # remove newline character
        line = line.rstrip()
        # add to list
        columns.append(int(line))
        # print each line

print(columns)

inputQuestion = input("Keep default settings ? (y/n) ")

if inputQuestion == "n":
    # ask user to input columns
    print("0: SH Codes, 1: Declared Value, 2: Customs Du, 3: Tax Percentage, 4: Quantities, 5: ")
    print("Example: 10 11 12 13 14")
    inputColumns = input("Enter columns: ")
    # split input columns into list
    columns = inputColumns.split(" ")
    # print list
    columns = [int(x) for x in columns]
    print(columns)
    # open default.txt file
    with open("default.txt", "w") as f:
        # write each column to file
        for column in columns:
            f.write(str(column) + "\n")

elif inputQuestion == "y":
    print("Loading default settings...")

else:
    print("Invalid input")
    exit()

SH_Codes = []
DeclaredValues = []
Customs_Tax = []
Forest_Tax = []
Quantities = []
Plastic_Tax = []
Parafiscal_Tax = []
Tax_Codes = []
articleCount = 0

for i in range(len(dataset)):
    SHvalue = dataset.iloc[i]['Column'+ str(columns[0])]
    print (SHvalue)
    # check if value is NAN
    if not pd.isna(SHvalue):
        articleCount += 1
        SH_Codes.append(SHvalue)

    Declaredv = dataset.iloc[i]['Column' + str(columns[1])]
    # check if value is NAN
    if not pd.isna(Declaredv):
        DeclaredValues.append(Declaredv)

    CustomsT = dataset.iloc[i]['Column' + str(columns[2])]
    # check if value is NAN
    if (not pd.isna(CustomsT)) and (CustomsT != '!'):
        Customs_Tax.append((CustomsT, articleCount))

    PlasticT = dataset.iloc[i]['Column'+ str(columns[4])]
    # check if value is NAN
    if (not pd.isna(PlasticT)) and (PlasticT != '!'):
        Plastic_Tax.append((PlasticT))

    Quant = dataset.iloc[i]['Column'+ str(columns[4])]
    # check if value is NAN
    if (not pd.isna(Quant)) and (Quant != '!'):
        Quantities.append((PlasticT))

    ForestT = dataset.iloc[i]['Column' + str(columns[3])]
    # check if value is NAN
    if (not pd.isna(ForestT)) and (type(ForestT) != str):
        Forest_Tax.append((Forest_Tax, articleCount))

    TaxC = dataset.iloc[i]['Column' + str(columns[3])]
    # check if value is NAN
    if (not pd.isna(TaxC)) and (type(TaxC) != str):
        Tax_Codes.append((TaxC, articleCount))

SH_Duplicates = [SH_Codes[i] for i in [x[1] for x in Tax_Codes]]
SH_Codes = [x[1] for x in Tax_Codes]
DFDeclaredValues = [DeclaredValues[x[1]-1] for x in Forest_Tax]
DFQuantities = [Quantities[x[1]-1] for x in Forest_Tax]

print(SH_Codes)
#print(SH_Duplicates)
#print(DFDeclaredValues)
#print(Customs_Tax)
#print(Forest_Tax)
#print(DFQuantities )
#print(Plastic_Tax)
#print(Parafiscal_Tax )
#print(Tax_Codes )


extractedData = pd.DataFrame({"SH_Codes": SH_Duplicates, "DeclaredValues": DFDeclaredValues, "Customs_Tax": Customs_Tax, "Tax_Codes" : [x[0] for x in Tax_Codes], "Quantities" : DFQuantities, "Forest_Tax": [x[0] for x in Forest_Tax]})
print(extractedData)

# output to excel
extractedData.to_excel("output.xlsx", index=False)