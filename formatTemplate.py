import pandas as pd

def formatTemplate():
    template = pd.read_excel("matching.xlsx")
    # delete first 7 rows
    template = template.drop(template.index[range(7)])
    # reset index
    template.reset_index(drop=True, inplace=True)
    # delete last row
    template = template.drop(template.index[-1])
    # rename columns
    template.columns = ["SH_Codes", "Customs Duty %", "Forest Tax %", "Plastic Tax %", "Dried Plants Tax %", "Parafiscal Tax %", "Quantities", "Declared Values", "Customs Duty", "Forest Tax", "Plastic Tax", "Sum of Dried Plants Tax Amount", "Parafiscal Tax"]

    # write to excel
    template.to_excel("outputsys.xlsx", index=False)
    print("Template formatted")


if __name__ == '__main__':
    formatTemplate()