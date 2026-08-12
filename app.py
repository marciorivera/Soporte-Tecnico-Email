"""
Servicio de Soporte Técnico en la Nube
---------------------------------------
Aplicación Streamlit que permite a un usuario reportar una incidencia
técnica. Valida la información y envía automáticamente un correo al
administrador con los datos del reporte, usando Gmail vía SMTP.

IMPORTANTE: Esta aplicación NO utiliza base de datos ni almacena
los reportes en ningún archivo. Los datos ingresados se usan
únicamente para validar el formulario y enviar el correo.
"""

import re
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import streamlit as st

# ---------------------------------------------------------------------------
# Configuración de la página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Soporte Técnico en la Nube",
    page_icon="🛠️",
    layout="centered",
)

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

TIPOS_PROBLEMA = [
    "Selecciona una opción",
    "Problema de hardware",
    "Problema de software",
    "Problema de red / conectividad",
    "Acceso a cuenta / credenciales",
    "Correo electrónico",
    "Impresoras / periféricos",
    "Otro",
]

NIVELES_PRIORIDAD = ["Baja", "Media", "Alta", "Crítica"]


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------
def validar_formulario(nombre, correo, tipo_problema, prioridad, descripcion):
    """Valida los datos del formulario y regresa una lista de errores."""
    errores = []

    if not nombre or not nombre.strip():
        errores.append("El nombre del usuario es obligatorio.")

    if not correo or not correo.strip():
        errores.append("El correo electrónico es obligatorio.")
    elif not re.match(EMAIL_REGEX, correo.strip()):
        errores.append("El correo electrónico no tiene un formato válido.")

    if tipo_problema == TIPOS_PROBLEMA[0]:
        errores.append("Debes seleccionar un tipo de problema.")

    if prioridad not in NIVELES_PRIORIDAD:
        errores.append("Debes seleccionar un nivel de prioridad válido.")

    if not descripcion or not descripcion.strip():
        errores.append("La descripción del problema es obligatoria.")
    elif len(descripcion.strip()) < 10:
        errores.append("La descripción debe tener al menos 10 caracteres.")

    return errores


def construir_correo(remitente, destinatario, nombre, correo, tipo_problema, prioridad, descripcion):
    """Construye el mensaje de correo con los datos del reporte."""
    asunto = f"[Soporte Técnico] Nuevo reporte - Prioridad {prioridad}"

    cuerpo = f"""
Se ha recibido un nuevo reporte de soporte técnico:

Nombre del usuario: {nombre}
Correo del usuario: {correo}
Tipo de problema: {tipo_problema}
Nivel de prioridad: {prioridad}

Descripción del problema:
{descripcion}

---
Este correo fue generado automáticamente por la aplicación de
Soporte Técnico en la Nube. No almacena información en ninguna
base de datos ni archivo.
"""

    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(cuerpo, "plain"))
    return mensaje


def enviar_correo(mensaje, remitente, contrasena, destinatario, servidor_smtp, puerto_smtp):
    """Envía el correo utilizando SMTP con conexión segura (SSL)."""
    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL(servidor_smtp, puerto_smtp, context=contexto) as servidor:
        servidor.login(remitente, contrasena)
        servidor.sendmail(remitente, destinatario, mensaje.as_string())


# ---------------------------------------------------------------------------
# Interfaz
# ---------------------------------------------------------------------------
st.title("🛠️ Servicio de Soporte Técnico en la Nube - Marcio Rivera")
st.caption(
    "Reporta una incidencia técnica y nuestro equipo de administración "
    "recibirá automáticamente los detalles por correo electrónico."
)

st.divider()

with st.form("formulario_reporte", clear_on_submit=False):
    st.subheader("📋 Formulario de reporte")

    nombre = st.text_input("Nombre del usuario *")
    correo_usuario = st.text_input("Correo electrónico *", placeholder="usuario@correo.com")
    tipo_problema = st.selectbox("Tipo de problema *", TIPOS_PROBLEMA)
    prioridad = st.select_slider("Nivel de prioridad *", options=NIVELES_PRIORIDAD, value="Media")
    descripcion = st.text_area(
        "Descripción detallada del problema *",
        height=150,
        placeholder="Describe con el mayor detalle posible la incidencia...",
    )

    st.markdown("<small>* Campos obligatorios</small>", unsafe_allow_html=True)

    enviado = st.form_submit_button("📨 Enviar reporte", use_container_width=True)

if enviado:
    errores = validar_formulario(nombre, correo_usuario, tipo_problema, prioridad, descripcion)

    if errores:
        st.error("⚠️ Se encontraron los siguientes errores en el formulario:")
        for err in errores:
            st.markdown(f"- {err}")
    else:
        try:
            # Credenciales y configuración desde Secrets de Streamlit
            remitente = st.secrets["email"]["remitente"]
            contrasena = st.secrets["email"]["contrasena"]
            destinatario = st.secrets["email"]["administrador"]
            servidor_smtp = st.secrets["email"].get("smtp_server", "smtp.gmail.com")
            puerto_smtp = int(st.secrets["email"].get("smtp_port", 465))

            with st.spinner("Enviando reporte al administrador..."):
                mensaje = construir_correo(
                    remitente, destinatario, nombre, correo_usuario,
                    tipo_problema, prioridad, descripcion
                )
                enviar_correo(mensaje, remitente, contrasena, destinatario, servidor_smtp, puerto_smtp)

            st.success("✅ ¡Reporte enviado correctamente! Su reporte ha sido enviado al administrador.")
            st.balloons()

        except KeyError:
            st.error(
                "❌ No se encontraron las credenciales de correo configuradas. "
                "Verifica que el archivo de Secrets de Streamlit esté correctamente configurado."
            )
        except smtplib.SMTPAuthenticationError:
            st.error(
                "❌ Error de autenticación con el servicio de correo. "
                "Verifica el usuario y la contraseña de aplicación en los Secrets."
            )
        except Exception as e:
            st.error(f"❌ Ocurrió un error al enviar el correo: {e}")

