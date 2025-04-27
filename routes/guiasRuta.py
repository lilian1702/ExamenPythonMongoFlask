import os
from flask import request, jsonify, render_template, session, flash, redirect
from app import app
from models.guias import Guias
from models.instructores import Instructores
from models.regional import Regional
from werkzeug.utils import secure_filename
from datetime import datetime, date
from bson import ObjectId


@app.route("/guias")
def get_guias():
    try:
        guias = Guias.objects()
        return jsonify(guias), 200
    except Exception as e:
        print("hubo un Error al obtener las guías:", e)
        return jsonify({"error": "hubo un Error al obtener las guías"}), 500


@app.route("/guiasRegister", methods=["POST"])
def create_guia():
    try:
        data = request.get_json(force=True)
        instructor = Instructores.objects(email=data.get("email")).first()
        print("Instructor encontrado exitosamente:", instructor)
        if instructor is None:
            return jsonify({"error": "el Instructor no ha sido encontrado"}), 404
        data["instructor"] = instructor.id  # Guardar el ID del instructor en lugar del email
        data["instructor"] = str(data["instructor"])  # Convertir a string para MongoDB
        guia = Guias(**data)
        guia.save()
        return jsonify({"message": "la guia ha sido guardada con exito"}), 201
    except Exception as e:
        print("Error al crear la guia:", e)
        return jsonify({"error": "Error al crear la guia"}), 500

@app.route("/guiasvista", methods=["GET"])
def guiasvista():
    if 'nombre' not in session:
        flash("No olvies Iniciar sesión para acceder a la pagina")
        return render_template('login.html')
    try:
        guias = Guias.objects.select_related()
        instructores = Instructores.objects.select_related()
        regionales = Regional.objects()
        return render_template('guia2.html', guias=guias, instructores=instructores, regionales=regionales), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@app.route("/agregarGuiaVista", methods=["GET"])
def agregarGuiaVista():
    try:
        guias = Guias.objects()
        return render_template('agregarGuia.html', guias=guias), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route("/agregarGuia", methods=["POST"])
def agregarGuia():
    try:
        data = request.form.to_dict() if request.form else request.get_json(force=True)

        docPDF = request.files.get("txtGuiaPDF")
        
        id_instructor = session.get("id")
        
        if not id_instructor:
            return jsonify({"error": "no ha iniciado sesion el instructor"}), 401
        
        try:
            instructor = Instructores.objects(id=ObjectId(id_instructor)).first()
        except Exception as e:
            return jsonify({"error": "ID de instructor no es válido"}), 400

        
        if not instructor:
            return jsonify({"message": "El Instructor no ha sido encontrado"}), 404

        if not docPDF:
            return jsonify({"error": "adjunte un PDF"}), 400

        if not instructor:
            return jsonify({"error": "el Instructor no ha sido encontrado"}), 404

        data["instructor"] = instructor
        data["fecha"] = date.today()
        
        nombre_pdf = secure_filename(docPDF.filename)
        ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombre_pdf)
        docPDF.save(ruta)
        data["documento_pdf"] = nombre_pdf
        
        guia = Guias(**data)
        guia.save()
        
        guias = Guias.objects()
        instructores = Instructores.objects()
        regionales = Regional.objects()
        return render_template('guia2.html', guias=guias, instructores=instructores, regionales=regionales), 200
    except Exception as e:
        print("hubo un Error al crear la guía:", e)
        return jsonify({"error": str(e)}), 500
    


