import pandas as pd
import re, calendar, locale

# Establecer la configuración regional a español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


class DataManipulator:
    def __init__(self, path:str):
        self.path = path
        self.df = pd.read_csv(path)
        self.isMonth = False
        
        self._traductor_month = {i :x for i,x in enumerate(calendar.month_name)}
        self._traductor_day = {i :x for i,x in enumerate(calendar.day_name)}
        self._traductor_day[2] = "miércoles"
        self._traductor_day[5] = "sábado"
        self.create_month()
        self.df_mes_actual = self.select_actual_month_db()
        
        
    def create_month(self):
        self.df['fecha'] = pd.to_datetime(self.df['fecha'], dayfirst=True)
        self.df['month'] = self.df['fecha'].dt.month
        self.df['year'] = self.df['fecha'].dt.year
        self.df['day'] = self.df['fecha'].dt.day
        #ponemos el numero de la semana
        self.df['week'] = self.df['fecha'].dt.isocalendar().week
        self.df['weekday'] = self.df['fecha'].dt.weekday
        self.df['weekday'] = self.df['weekday'].replace(self._traductor_day)
        self.df['month'] = self.df['month'].replace(self._traductor_month)
            

    def group_by_month(self):
        return self.formating_to_frontend_individual(self.df.groupby(['month']).agg({'importe':'sum', 'cantidad':'sum'}).reset_index().to_dict(orient='records'), is_month=True, tipo='line', name='Gasto mensual', variable='month')
    
    
    def group_by_weekday(self, with_importe:bool = True):
        if with_importe:
            return self.formating_to_frontend_individual(self.df.groupby(['week']).agg({'importe':'sum', 'cantidad':'sum'}).reset_index().to_dict(orient='records'), tipo='line', name='Gasto semanal', variable="week" , is_week=True)
        
        return self.formating_to_frontend_individual(self.df.groupby(['week']).agg({'id':'nunique'}).reset_index().to_dict(orient='records'), tipo='line', name='Visitas por semana', variable="week" , is_week=True, data_to_see='id')
        
    
    def group_by_tipo(self, db:pd.DataFrame):
        return self.formating_to_frontend_individual(db.groupby(['clase']).agg({'importe':'sum', 'cantidad':'sum'}).reset_index().to_dict(orient='records'), tipo='pie', name='Gasto por tipo de producto', variable='clase')
    
    
    def group_by_day(self, db:pd.DataFrame):
        return self.formating_to_frontend_individual(db.groupby(['weekday']).agg({'id':'nunique'}).reset_index().to_dict(orient='records'), tipo='bar', name='Visitas por dia', variable='weekday', data_to_see='id', is_weekday=True)
    
    def select_actual_month_db(self):
        #obtenemos el mes actual
        month = pd.Timestamp.now().month
        month = calendar.month_name[month]
   
        return self.df[self.df['month'] == month]
    
    
    
    def stadistics_actual_month(self):
        data =  {
            "importe": round(self.df_mes_actual['importe'].sum(),2),
            "visitas": self.df_mes_actual['id'].nunique(),
            "db_tipo": self.group_by_tipo(self.df_mes_actual),
            "db_visitas_dias": self.group_by_day(self.df_mes_actual)
            }
        
        diferencia_mes_anterior_porcentual = (self.df_mes_actual['importe'].sum() / self.df[self.df['month'] == self._traductor_month[pd.Timestamp.now().month - 1]]['importe'].sum()) * 100 -100
        
        data['diferencia_mes_anterior'] = round(diferencia_mes_anterior_porcentual, 2)
        
        return data
        
        
        
        
        
    
    
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