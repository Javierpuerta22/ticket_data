import flask, pandas as pd
from flask import request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config.config import app, db

from routes.monthly import monthly
from routes.prices import prices
app.register_blueprint(monthly)
app.register_blueprint(prices)


with app.app_context():
    db.create_all()


from models.model_data import DataManipulator
from models.model_csv import CSVconstructor, PDFFile



CSVConstrucorObject = CSVconstructor(db)
DataClass = DataManipulator(db)

@app.route('/get_month', methods=['GET'])
def get_month():
    return jsonify(DataClass.group_by_month())

@app.route('/get_week', methods=['GET'])
def get_weekday():
    return jsonify(DataClass.group_by_weekday())

@app.route('/get_tipo', methods=['GET'])
def get_tipo():
    return jsonify(DataClass.group_by_tipo(DataClass.select_all_db()))


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
            
            
    return {"message":"Archivos subidos exitosamente"}

if __name__ == '__main__':
    app.run(debug=True, port=8000)