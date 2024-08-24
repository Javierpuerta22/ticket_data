import flask
from flask import request, jsonify
from flask_cors import CORS

from models.model_data import DataManipulator
from models.model_csv import CSVconstructor, PDFFile



app = flask.Flask(__name__, template_folder='templates', static_folder='static', static_url_path='')
CORS(app)
app.config["DEBUG"] = True


DataClass = DataManipulator('./data/csv/data.csv')
CSVConstrucorObject = CSVconstructor()
CSVConstrucorObject.df = DataClass.df

@app.route('/get_month', methods=['GET'])
def get_month():
    return jsonify(DataClass.group_by_month())

@app.route('/get_week', methods=['GET'])
def get_weekday():
    return jsonify(DataClass.group_by_weekday())

@app.route('/get_tipo', methods=['GET'])
def get_tipo():
    return jsonify(DataClass.group_by_tipo())


@app.route('/get_week_count', methods=['GET'])
def get_week_count():
    return jsonify(DataClass.group_by_weekday(with_importe=False))

@app.route('/add_ticket', methods=['GET', 'POST'])
def upload_files():
    # Obtener la lista de archivos subidos
    uploaded_files = request.files.getlist('files')
    
    for file in uploaded_files:
        if file and file.filename.endswith('.pdf'):
            # Aquí puedes guardar el archivo, procesarlo, etc.
            file.save(f"./data/pdf/{file.filename}")
            pdf = PDFFile(f"./data/pdf/{file.filename}")            
            CSVConstrucorObject.add_rows(pdf.get_text())
            CSVConstrucorObject.save_csv('./data/csv/data.csv')
            
    DataClass.df = CSVConstrucorObject.df
            
            
            
    
    return {"message":"Archivos subidos exitosamente"}

if __name__ == '__main__':
    app.run(debug=True, port=8000)