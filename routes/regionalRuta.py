from flask import render_template
from models.regional import Regional
from app import app

@app.route("/formulario")
def mostrar_formulario():
    regionales = Regional.objects()  # Trae todas las regionales de la colección
    return render_template("login.html", regionales=regionales)
