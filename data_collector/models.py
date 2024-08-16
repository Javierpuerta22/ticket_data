import pandas as pd
import re
from PyPDF2 import PdfReader

class PDFFile:
    def __init__(self, path):
        self.path = path
        self.pdf = PdfReader(path)
        
    def get_text(self):
        text = ''
        for page in self.pdf.pages:
            text += page.extract_text()
        return text
    


class CSVconstructor:
    def __init__(self):
        # construimos un dataframe vacio con las columas que necesitamos
        self.df = pd.DataFrame(columns=["id", "fecha", "hora", "clase", "descripcion", "cantidad", "importe", "total", "peso"])
        
    def add_rows(self, text:str):
        self.text = text.split('\n')
        cabecera = self.text[0:6]
        
        id, fecha, hora = self.detect_cabecera(cabecera)
        
        total_list = [row for row in self.text[7:] if "TOTAL" in row]
        total = total_list[0].split(' ')[-1]
        FINALIZED = False

        for row in self.text[7:]:
            if "TOTAL" not in row:
                print(row)
                row_separated = re.sub(r'^(\d+)', r'\1 ', row)
                
                cantidad = row_separated.split(' ')[0]
                
                if cantidad.isnumeric():
                    importe = row_separated.split(' ')[-1]
                    descripcion = row_separated.split(' ')[1:-1]
                    descripcion = ' '.join(descripcion)
                    descripcion = re.sub(r'[\d,]+', '', descripcion)

                    clase = "Otros"
                    
                    self.df.loc[self.df.shape[0]] =  {"id":id, "fecha":fecha, "hora":hora, "clase":clase, "descripcion":descripcion, "cantidad":cantidad, "importe":importe, "total": total, "peso": 0}
                    
                else:
                    pez = True if cantidad == "PEIX" else False
                    fruta = True if cantidad == "FRUITA" else False
                    break
            else:
                FINALIZED = True
                break
        
        if not FINALIZED:
            
            restante = self.text[(self.df.shape[0] + 7 + 1):]
            for desc, pesaje in zip(restante[::2], restante[1::2]):
                if "PEIX" in desc or "FRUITA" in desc:
                    break
                
                if "TOTAL" in desc:
                    FINALIZED = True
                    break
                
                clase = "Pescado" if pez else "Fruta"
                descripcion = desc
                peso = pesaje.split(' ')[0]
                importe = pesaje.split(' ')[-1]
                
                self.df.loc[self.df.shape[0]] =  {"id":id, "fecha":fecha, "hora":hora, "clase":clase, "descripcion":descripcion, "cantidad":0, "importe":importe, "total": total, "peso": peso}
                
            if not FINALIZED:
                restante = self.text[(self.df.shape[0] + 7 + 1):]
                for desc, pesaje in zip(restante[::2], restante[1::2]):
                    if "PEIX" in desc or "FRUITA" in desc:
                        break
                    
                    if "TOTAL" in desc:
                        FINALIZED = True
                        break
                    
                    clase = "Pescado" if pez else "Fruta"
                    descripcion = desc
                    peso = pesaje.split(' ')[0]
                    importe = pesaje.split(' ')[-1]
                    
                    self.df.loc[self.df.shape[0]] =  {"id":id, "fecha":fecha, "hora":hora, "clase":clase, "descripcion":descripcion, "cantidad":0, "importe":importe, "total": total, "peso": peso}
        
        # añadimos los datos al dataframe
        
        return self.df
        
        
    def detect_cabecera(self, text:list):
        # cojemos el ID
        id = text[-1].split(' ')[-1]
        #eliminamos los "-" del id
        id = id.replace('-', '')
        
        # cojemos la fecha
        fecha, hora = text[-2].split(' ')[0], text[-2].split(' ')[1]
        
        return id, fecha, hora
        
    
    
        