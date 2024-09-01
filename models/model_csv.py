import pandas as pd
import re, datetime
from PyPDF2 import PdfReader
from .database import Ticket

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
    def __init__(self, db):
        # construimos un dataframe vacio con las columas que necesitamos
        self.db = db
        self.pez_detected = False
        self.fruta_detected = False
        self.finalized = False
        
    def add_rows(self, text:str):
        self.finalized = False
        self.pez_detected = False
        self.fruta_detected = False
        
        self.text = text.split('\n')
        cabecera = self.text[0:6]
        
        id, fecha, hora = self.detect_cabecera(cabecera)
        for i, row in enumerate(self.text):
            if "TOTAL" in row:
                total = row.split(' ')[-1]
                total = total.replace(',', '.')
                total = float(total)
                index = i
                break
        
        self.text = self.text[7:(index)]
        
        for i, row in enumerate(self.text): 
            row_separated = re.sub(r'^(\d+)', r'\1 ', row)
           
            if "PÀRQUING" not in row_separated.split(" "):
                
                cantidad = row_separated.split(' ')[0]
                
                if not self.detect_pez(row_separated) and not self.detect_fruta(row_separated):
                    importe = row_separated.split(' ')[-1]
                    importe = importe.replace(',', '.')
                    importe = float(importe)
                    
                    descripcion = row_separated.split(' ')[1:-1]
                    descripcion = ' '.join(descripcion)
                    descripcion = re.sub(r'[\d,]+', '', descripcion)
                    if descripcion == " OUS FRESC":
                        cantidad = str(cantidad)
                        cantidad = cantidad.replace('24', '')
                        cantidad = cantidad.replace('12', '')
                        cantidad = cantidad.replace('6', '')
                        cantidad = int(cantidad)

                    clase = self.detect_category_in_description(descripcion)
                    
                    # convertimos la fecha y la hora en datetime
                    
                    self.db.session.add(Ticket(id=id, fecha=fecha, clase=clase, descripcion=descripcion.strip(), cantidad=int(cantidad), importe=importe, total=total, peso=0))
                    
                elif self.detect_pez(row_separated):
                    self.pez_detected = True
                    self.add_pez_rows(id, fecha, hora, total, i)
                    break
                
                elif self.detect_fruta(row_separated):
                    self.fruta_detected = True
                    self.add_fruta_rows(id, fecha, hora, total, i)
                    break
            else:
                self.finalized = True
                break
            
        self.db.session.commit()                
        
        
    def detect_cabecera(self, text:list):
        # cojemos el ID
        id = text[-1].split(' ')[-1]
        #eliminamos los "-" del id
        id = id.replace('-', '')
        
        # cojemos la fecha
        fecha, hora = text[-2].split(' ')[0], text[-2].split(' ')[1]
        fecha = datetime.datetime.strptime(fecha, '%d/%m/%Y')
        hora = fecha.strftime('%Y-%m-%d') + ' ' + hora
        hora = datetime.datetime.strptime(hora, '%Y-%m-%d %H:%M')
        fecha = hora
        return id, fecha, hora
    
    def detect_fruta(self, row:str):
        
        if "PÀRQUING" in row.split(' '):
            return False
        
        
        importe_total = row.split(' ')[-1]
        
        importe_total = importe_total.replace(',', '.')
        
        
        
        try:
            importe_total = float(importe_total)
            return False
        except:
            importe_total = 0
            if row.startswith('1'):
                return True
            return False
        
    def detect_pez(self, row:str):
        if "PEIX" in row.split(' ') and len(row.split(' ')) == 1:
            return True
        
        return False
    
    
    def detect_category_in_description(self, row:str):
        CARNE = ["CARN", "POLLASTRE", "POLLO", "GALL", "GALLINA", "SALSITXES" "SALCHICHON", "FUET", "BURG", "PERNIL", "BACÓ" ,"LLOM", "COSTELLES", "PORC", "BOTIFARRA", "JAMÓN", "FILET", "BISTEC"]
        VERDURA = ["XAMPINYÓ", "ICEBERG", "BROCOLI", "BROCOL", "MONGETES", "COGOMBRE", "PEBROT"]
        PAN = ["PA", "XAPATA"]
        AGUA = ["AIGUA"]
        
        row_splitted = row.split(' ')
        for carne in CARNE:
            if carne in row_splitted:
                return "Carne"
        
        for verdura in VERDURA:
            if verdura in row_splitted:
                return "Verdura"
            
        for pan in PAN:
            if pan in row_splitted:
                return "Pan"
            
        for agua in AGUA:
            if agua in row_splitted:
                return "Agua"
        
        
        return "Otros"
        
    
    def add_pez_rows(self, id, fecha, hora, total, index):
        restante = self.text[(index +1):]
        index_add = 0
        for desc, pesaje in zip(restante[::2], restante[1::2]):
            desc = re.sub(r'^(\d+)', r'\1 ', desc)
            
            if self.detect_pez(desc):
                self.pez_detected = True
                self.add_pez_rows(id, fecha, hora, total, index + (index_add*2) + 1)
                break
            
            if self.detect_fruta(desc):
                self.fruta_detected = True
                self.add_fruta_rows(id, fecha, hora, total, index + (index_add*2) + 1)
                break

            if "PÀRQUING" in desc.split(" "):
                self.finalized = True
                break
            
            clase = "Pescado"
            descripcion = desc
            peso = pesaje.split(' ')[0]
            peso = peso.replace(',', '.')
            peso = float(peso)
            importe = pesaje.split(' ')[-1]
            importe = importe.replace(',', '.')
            importe = float(importe)
          
            
            self.db.session.add(Ticket(id=id, fecha=fecha, clase=clase, descripcion=descripcion.strip(), cantidad=0, importe=importe, total=total, peso=peso))
            index_add += 1
            
        self.db.session.commit()
            
    def add_fruta_rows(self, id, fecha, hora, total, index):
        restante = self.text[index:]
        index_add = 0
        for desc, pesaje in zip(restante[::2], restante[1::2]):
            desc = re.sub(r'^(\d+)', r'\1 ', desc)

            if "PÀRQUING" in desc.split(" "):
                self.finalized = True
                break
            
            if "PEIX" in desc.split(" "):
                self.pez_detected = True
                self.add_pez_rows(id, fecha, hora, total, index + (index_add*2) +1)
                break
            
            clase = "Fruta"
            descripcion = desc
            descripcion = descripcion.split(' ')[1:]
            descripcion = ' '.join(descripcion)
            peso = pesaje.split(' ')[0]
            peso = peso.replace(',', '.')
            peso = float(peso)
            importe = pesaje.split(' ')[-1]
            importe = importe.replace(',', '.')
            importe = float(importe)
            
            
            self.db.session.add(Ticket(id=id, fecha=fecha, clase=clase, descripcion=descripcion.strip(), cantidad=0, importe=importe, total=total, peso=peso))
            
            index_add += 1
            
        self.db.session.commit()