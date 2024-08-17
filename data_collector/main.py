from models import PDFFile, CSVconstructor
import os

csvConstructor = CSVconstructor()

# iteramos en la carpeta donde se encuentran los pdfs
for root, dirs, files in os.walk('../data/pdf'):
    for file in files:
        if file.endswith('.pdf'):
            # creamos un objeto PDFFile por cada archivo
            print(file)
            pdf = PDFFile(os.path.join(root, file))            
            csvConstructor.add_rows(pdf.get_text())
            
            
csvConstructor.save_csv('./../data/csv/data.csv')