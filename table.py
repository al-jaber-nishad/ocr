from tabula import read_pdf 

#reads the table from pdf file 

df = read_pdf("file2.pdf",pages="all") #address of pdf file
print(df)
