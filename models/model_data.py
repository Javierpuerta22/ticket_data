import pandas as pd
import re, calendar


class DataManipulator:
    def __init__(self, path:str):
        self.path = path
        self.df = pd.read_csv(path)
        self.isMonth = False
        
    def create_month(self):
        if not self.isMonth:
            self.df['fecha'] = pd.to_datetime(self.df['fecha'], dayfirst=True)
            self.df['month'] = self.df['fecha'].dt.month
            self.df['year'] = self.df['fecha'].dt.year
            self.df['day'] = self.df['fecha'].dt.day
            #ponemos el numero de la semana
            self.df['week'] = self.df['fecha'].dt.isocalendar().week
            self.df['weekday'] = self.df['fecha'].dt.weekday
            self.df['weekday'] = self.df['weekday'].replace({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'})
            self.df['month'] = self.df['month'].replace({1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'})
            self.isMonth = True

    def group_by_month(self):
        self.create_month()
        return self.formating_to_frontend_individual(self.df.groupby(['month']).agg({'importe':'sum', 'cantidad':'sum'}).reset_index().to_dict(orient='records'), is_month=True, tipo='line', name='Gasto mensual', variable='month')
    
    
    def group_by_weekday(self, with_importe:bool = True):
        self.create_month()
        if with_importe:
            return self.formating_to_frontend_individual(self.df.groupby(['week']).agg({'importe':'sum', 'cantidad':'sum'}).reset_index().to_dict(orient='records'), tipo='line', name='Gasto semanal', variable="week" , is_week=True)
        
        return self.formating_to_frontend_individual(self.df.groupby(['week']).agg({'id':'nunique'}).reset_index().to_dict(orient='records'), tipo='line', name='Visitas por semana', variable="week" , is_week=True, data_to_see='id')
        
    
    def group_by_tipo(self):
        return self.formating_to_frontend_individual(self.df.groupby(['clase']).agg({'importe':'sum', 'cantidad':'sum'}).reset_index().to_dict(orient='records'), tipo='pie', name='Gasto por tipo de producto', variable='clase')
    
    
    def formating_to_frontend_individual(self, data:list, variable:str = "" ,tipo:str = "line", name:str = "",  is_month:bool = False, is_week:bool = False, data_to_see:str = 'importe'):
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
        
        
        labels = [item[variable] for item in data]
        datasets = [
            {
                'label': data_to_see,
                'data': [item[data_to_see] for item in data]
            }
        ]
        return {'labels': labels, 'datasets': datasets, 'type': tipo, 'name': name}