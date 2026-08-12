# Servicio de Soporte Técnico en la Nube

## 🎯 Objetivo

Aplicación web que permite a un usuario reportar una incidencia técnica mediante un formulario. La aplicación valida la información ingresada y, cuando es correcta, envía automáticamente un correo electrónico al administrador con los datos del reporte. La aplicación **no utiliza base de datos**: la información solo se usa para validar el formulario y enviar el correo, sin almacenarse en ningún archivo o sistema.

## 👥 Integrantes del equipo

- Marcio Rivera

## ⚙️ Funcionamiento de la aplicación

1. El usuario accede a la aplicación desde su navegador.
2. Completa el formulario con: nombre, correo electrónico, tipo de problema, nivel de prioridad y descripción de la incidencia.
3. Al presionar **"Enviar reporte"**, la aplicación valida:
   - Que todos los campos obligatorios estén completos.
   - Que el correo tenga un formato válido.
   - Que se haya seleccionado un tipo de problema.
   - Que exista una descripción de la incidencia (mínimo 10 caracteres).
4. Si hay errores, se muestran en pantalla y **no se envía el correo**.
5. Si la información es válida, la aplicación arma el mensaje y lo envía automáticamente por correo (SMTP con Gmail) al administrador.
6. El usuario ve un mensaje de confirmación: *"¡Reporte enviado correctamente! Su reporte ha sido enviado al administrador."*
7. Ningún dato del reporte se guarda en la aplicación; solo se usa en memoria durante el envío.

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Streamlit** — interfaz web y despliegue en la nube
- **smtplib / email (librería estándar de Python)** — envío de correo vía SMTP con conexión segura (SSL)
- **Gmail SMTP** (`smtp.gmail.com`, puerto 465) con **contraseña de aplicación (App Password)**
- **Streamlit Community Cloud** — hosting/despliegue

## ▶️ Procedimiento de ejecución

### Localmente

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/marciorivera/Soporte-Tecnico-Email.git
   cd TU-REPOSITORIO
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Crear el archivo `.streamlit/secrets.toml` (NO se sube al repositorio) usando como base `.streamlit/secrets.toml.example`, con tus credenciales reales de Gmail (ver sección de seguridad).
4. Ejecutar la aplicación:
   ```bash
   streamlit run app.py
   ```
5. Abrir el navegador en `http://localhost:8501`.

### En Streamlit Community Cloud

1. Subir el proyecto a un repositorio de GitHub (sin incluir `secrets.toml`).
2. Crear una nueva app en [share.streamlit.io](https://share.streamlit.io) apuntando al repositorio y a `app.py`.
3. En **App → Settings → Secrets**, pegar el contenido de `secrets.toml` con las credenciales reales.
4. Desplegar y verificar el funcionamiento desde un navegador distinto al usado en el desarrollo.

## 🔐 Gestión segura de credenciales

- Las credenciales del correo (usuario y contraseña de aplicación de Gmail) **nunca se escriben en el código fuente**.
- Se almacenan y se leen mediante `st.secrets`, el mecanismo de **Secrets de Streamlit**:
  - En local: archivo `.streamlit/secrets.toml` (incluido en `.gitignore`, nunca se sube a GitHub).
  - En la nube: configurado directamente en el panel de **Streamlit Community Cloud** (App → Settings → Secrets).
- Se usa una **contraseña de aplicación (App Password)** de Gmail en lugar de la contraseña real de la cuenta, siguiendo las buenas prácticas de Google para acceso de aplicaciones de terceros.
- El repositorio solo incluye `secrets.toml.example` como plantilla, sin datos reales.
- No se comparten capturas de pantalla donde se observen contraseñas, tokens o claves.

### Cómo generar la contraseña de aplicación de Gmail (una sola vez)

1. Activar la verificación en 2 pasos en la cuenta de Gmail que enviará los correos (Cuenta de Google → Seguridad).
2. Ir a [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
3. Crear una nueva contraseña de aplicación (nombre sugerido: "Streamlit Soporte Técnico").
4. Google genera una contraseña de 16 caracteres — copiarla y pegarla en `secrets.toml` como `contrasena` (no la contraseña normal de la cuenta).
5. Completar también `remitente` (la misma cuenta de Gmail) y `administrador` (correo que recibirá los reportes), siguiendo la estructura de `.streamlit/secrets.toml.example`.

## 🚫 Restricciones respetadas

- La aplicación **no utiliza base de datos**.
- Los reportes **no se almacenan** en archivos, hojas de cálculo ni ningún otro sistema; la información solo se usa en memoria para validar el formulario y enviar el correo.

## 🔗 Enlaces

Ver `documentacion/enlace_aplicacion.txt` para el enlace de la aplicación desplegada y del repositorio.
