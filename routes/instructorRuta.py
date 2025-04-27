from flask import request, jsonify, render_template, session, flash, redirect, url_for
from app import app
from models.instructores import Instructores
import yagmail
import threading
import requests
import random
import string
from models.regional import Regional
email = yagmail.SMTP('quiraconstanza@gmail.com','cqzdobsjaynbjuzi',encoding='utf-8')

@app.route("/instructores")
def get_instructores():
    try:
        instructores = Instructores.objects()
        return jsonify(instructores), 200
    except Exception as e:
        print("Error en la peticion obtener instructores:", e)
        return jsonify({"error": "Error en la peticion obtener instructores"}), 500

def enviarCorreo(destinatario, asunto, mensaje):
    email.send(to=destinatario, subject=asunto, contents=mensaje)
    

@app.route("/instructorRegister", methods=["POST"])
def create_instructor():
    try:
        nombre = request.form.get("nombre")
        password = request.form.get("password")
        email = request.form.get("email")
        regional_id = request.form.get("regional")
        regional = Regional.objects(id=regional_id).first()#consltar la regional por id a la bd
        
        if not regional:
            flash('Regional no encontrada.', 'danger')
            return redirect('/')

        if not all([nombre, password, email, regional]):
            return jsonify({"message": "Faltan datos"}), 400
        
        instruc = Instructores(
            nombre=nombre,
            password=password,
            email=email,
            regional=regional
        )
        
        instruc.save()

        mensaje = f'registro exitoso en la aplicación. tus datos son: correo: {email}, password: {password}'
        destinatarios = [email]

        hilo = threading.Thread(target=enviarCorreo, args=(destinatarios, 'Registro exitoso', mensaje))
        hilo.start()

        flash('Instructor registrado exitosamente.', 'success')
        return redirect(url_for('inicio'))
    except Exception as e:
        print("Error al crear el instructor:", e)
        return jsonify({"error": "Error al crear el instructor"}), 500

@app.route("/instructorLogin", methods=["POST"])
def login_instructor():
    try:
        data = request.get_json(force=True)
        correo=data.get("email")
        passw=data.get("password")
        instructor = Instructores.objects(email=correo).first()
        
        if not instructor:
            return jsonify({"message": "el Correo no esta registrado"}), 404
        
        if instructor.password != passw:
            return jsonify({"message": " la Contraseña es incorrecta"}), 401
        #sesion y correo
        session["id"] = str(instructor.id)
        session["email"] = instructor.email
        session["nombre"] = instructor.nombre
        session["password"] = instructor.password
        session["autenticado"] = True
        return jsonify({"message": "Login exitoso"}), 200
    except Exception as e:
        print("Error al iniciar sesion:", e)
        return jsonify({"error": "Error al iniciar sesion"}), 500
    
@app.route('/usuarios/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({"message": "Sesión cerrada"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
