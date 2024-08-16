from models import PDFFile, CSVconstructor
import os

csvConstructor = CSVconstructor()

# iteramos en la carpeta donde se encuentran los pdfs
for root, dirs, files in os.walk('../data/pdf'):
    for file in files:
        if file.endswith('.pdf'):
            # creamos un objeto PDFFile por cada archivo
            pdf = PDFFile(os.path.join(root, file))            
            print(csvConstructor.add_rows(pdf.get_text()))