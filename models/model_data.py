import pandas as pd
import re, calendar, locale
from sqlalchemy import extract
from .database import Ticket

# Establecer la configuración regional a español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')



class DataManipulator:
    def __init__(self, db):
        self.db = db
        self.isMonth = False
        
        self._traductor_month = {i :x for i,x in enumerate(calendar.month_name)}
        self._traductor_day = {i :x for i,x in enumerate(calendar.day_name)}
        self._traductor_day[2] = "miércoles"
        self._traductor_day[5] = "sábado"        
        
    def create_month(self, df:pd.DataFrame):
        df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)
        df['month'] = df['fecha'].dt.month
        df['year'] = df['fecha'].dt.year
        df['day'] = df['fecha'].dt.day
        df["year_month"] = df['year'].astype(str) + "-" + df['month'].astype(str)
        df['year_month_day'] = df['year'].astype(str) + "-" + df['month'].astype(str) + "-" + df['day'].astype(str)
        #ponemos el numero de la semana
        
        df['week'] = df['fecha'].dt.isocalendar().week
        df['weekday'] = df['fecha'].dt.weekday
        df['weekday'] = df['weekday'].replace(self._traductor_day)
        df['month'] = df['month'].replace(self._traductor_month)
        return df
            

    def group_by_month(self):
        df = self.select_all_db()
        df = self.create_month(df)
        
        return self.formating_to_frontend_individual(df.groupby(['month']).agg({'importe':'sum', 'cantidad':'sum'}).reset_index().to_dict(orient='records'), is_month=True, tipo='line', name='Gasto mensual', variable='month')
    
    
    def group_by_weekday(self ,with_importe:bool = True):
        df = self.select_all_db()
        df = self.create_month(df)
        
        if with_importe:
            return self.formating_to_frontend_individual(df.groupby(['week']).agg({'importe':'sum', 'cantidad':'sum'}).reset_index().to_dict(orient='records'), tipo='line', name='Gasto semanal', variable="week" , is_week=True)
        
        return self.formating_to_frontend_individual(df.groupby(['week']).agg({'id':'nunique'}).reset_index().to_dict(orient='records'), tipo='line', name='Visitas por semana', variable="week" , is_week=True, data_to_see='id')
        
    
    def group_by_tipo(self,db:pd.DataFrame):
        return self.formating_to_frontend_individual(db.groupby(['clase']).agg({'importe':'sum', 'cantidad':'sum'}).reset_index().to_dict(orient='records'), tipo='pie', name='Gasto por tipo de producto', variable='clase')
    
    
    def group_by_day(self, db:pd.DataFrame):
        return self.formating_to_frontend_individual(db.groupby(['weekday']).agg({'id':'nunique'}).reset_index().to_dict(orient='records'), tipo='bar', name='Visitas por dia', variable='weekday', data_to_see='id', is_weekday=True)
    
    def select_actual_month_db(self):
        #obtenemos el mes actual
        month = pd.Timestamp.now().month -1
        print(month)
        data =  self.db.session.query(Ticket).filter(extract(
            "month", Ticket.fecha) == month).all()
   
        return pd.DataFrame([x.to_dict() for x in data])
    
    
    def select_all_db(self):
        data = self.db.session.query(Ticket).all()
        return pd.DataFrame([x.to_dict() for x in data])
    
    def stadistics_actual_month(self):
        
        df_mes_actual = self.select_actual_month_db()
        self.df_mes_actual = self.create_month(df_mes_actual)
        
        data =  {
            "importe": round(self.df_mes_actual['importe'].sum(),2),
            "visitas": self.df_mes_actual['id'].nunique(),
            "db_tipo": self.group_by_tipo(self.df_mes_actual),
            "db_visitas_dias": self.group_by_day(self.df_mes_actual)
            }
        
        
        # seleccionamos el la suma del importe del mes anterior
        gasto_anterior = self.db.session.query(Ticket).filter(extract(
            "month", Ticket.fecha) == pd.Timestamp.now().month - 2).all()
        
        gasto_anterior = pd.DataFrame([x.to_dict() for x in gasto_anterior])
        
        
        diferencia_mes_anterior_porcentual = (self.df_mes_actual['importe'].sum() / gasto_anterior['importe'].sum()) * 100 -100
        
        data['diferencia_mes_anterior'] = round(diferencia_mes_anterior_porcentual, 2)
        
        return data
    
    
    def select_prices_timeline_by_product(self, product:str):
        df_individual = Ticket.query.filter(Ticket.descripcion == product).all()
        df_individual = pd.DataFrame([x.to_dict() for x in df_individual])
        df_individual = self.create_month(df_individual)
        
        df_individual = df_individual.sort_values(by='year_month_day')
        
        if df_individual["peso"].sum() > 0:
            df_individual["unitary_price"] = round(df_individual['importe'] / df_individual['peso'], 2)
        else:
            df_individual["unitary_price"] = round(df_individual['importe'] / df_individual['cantidad'].replace(0,1), 2) 
            
        df_individual = df_individual.to_dict(orient='records')
        
        return self.formating_to_frontend_individual(df_individual, tipo='line', name=f'Precio de {product} en el tiempo', variable='year_month_day', data_to_see="unitary_price")
        
    def get_types_of_products(self):
        
        # Seleccionamos los tipos de productos únicos de la columna 'clase' de la base de datos
        data = self.db.session.query(Ticket.clase).distinct().all()
        
        return [x[0] for x in data]
    
    def get_subtypes_of_products(self, product:str):
        
        data = self.db.session.query(Ticket.descripcion).filter(Ticket.clase == product).distinct().all()
        return [x[0] for x in data]
    
    def formating_to_frontend_individual(self, data:list, variable:str = "" ,tipo:str = "line", name:str = "",  is_month:bool = False, is_week:bool = False, data_to_see:str = 'importe', is_weekday:bool = False):
        """
        La estructura para el frontend es la siguiente: 
        {
            labels: [lista de valores del eje X]
            datasets: [
                {
                    label: 'label',
                    data: [lista de valores del eje Y]
                }
            ]
        }
        
        teniendo en cuenta que data es una lista de diccionarios en formato records de pandas. Además debe estar ordenado ele eje Y para que coincida con el eje X
        """
        
        #ordenamos la lista de diccionarios por su variable independiente
        if is_month:
            data = sorted(data, key=lambda x: list(calendar.month_name).index(x['month']))
            
        elif is_week:
            data = sorted(data, key=lambda x: x['week'])
            
        elif is_weekday:
            data = sorted(data, key=lambda x: list(self._traductor_day.values()).index(x['weekday']))
        
                
        labels = [item[variable] for item in data]
        datasets = [
            {
                'label': data_to_see,
                'data': [item[data_to_see] for item in data]
            }
        ]
        return {'labels': labels, 'datasets': datasets, 'type': tipo, 'name': name}
    


        
   