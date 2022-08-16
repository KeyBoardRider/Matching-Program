import pandas as pd

dataset = pd.read_excel("matching.xlsx")

print(dataset)
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
    print("0: SH Codes, 1: Declared Value, 2: Tax Codes, 3: Tax Percentage, 4: Quantities")
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
Tax_Codes = []
Tax_Values = []
Quantities = []
Quantityvalues = []
articleCount = 0

for i in range(len(dataset)):
    SHvalue = dataset.iloc[i]['Unnamed: '+ str(columns[0] - 1)]
    # check if value is NAN
    if not pd.isna(SHvalue):
        articleCount += 1
        SH_Codes.append(SHvalue)
    print(SH_Codes)

    Declaredv = dataset.iloc[i]['Unnamed: ' + str(columns[1] - 1)]
    # check if value is NAN
    if not pd.isna(Declaredv):
        DeclaredValues.append(Declaredv)

    TaxCodevalues = dataset.iloc[i]['Unnamed: ' + str(columns[2] - 1)]
    # check if value is NAN
    if (not pd.isna(TaxCodevalues)) and (TaxCodevalues != '!'):
        Tax_Codes.append((TaxCodevalues, articleCount))

    Quantityvalues = dataset.iloc[i]['Unnamed: '+ str(columns[4] - 1)]
    # check if value is NAN
    if (not pd.isna(Quantityvalues)) and (Quantityvalues != '!'):
        Quantities.append((Quantityvalues))

    TaxPercentage = dataset.iloc[i]['Unnamed: ' + str(columns[3] - 1)]
    # check if value is NAN
    if (not pd.isna(TaxPercentage)) and (type(TaxPercentage) != str):
        Tax_Values.append((TaxPercentage, articleCount))

#SH_Codes = [x[1] for x in Tax_Values]
DFDeclaredValues = [DeclaredValues[x[1]-1] for x in Tax_Values]
DFQuantities = [Quantities[x[1]-1] for x in Tax_Values]

extractedData = pd.DataFrame({"SH_Codes": SH_Codes, "DeclaredValues": DFDeclaredValues, "Tax_Codes": [x[0] for x in Tax_Codes], "Quantities" : DFQuantities, "Tax_Values": [x[0] for x in Tax_Values]})
print(extractedData)

# output to excel
extractedData.to_excel("output.xlsx", index=False)