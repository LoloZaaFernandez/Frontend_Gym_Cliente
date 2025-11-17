"""
Configuración global de la aplicación
"""
#config/settings.py
import os

# --- DIRECTORIO BASE DEL PROYECTO ---
# Obtiene el directorio del archivo actual (config/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Directorio de imágenes
IMG_DIR = os.path.join(BASE_DIR, 'img')

# --- COLORES BASADOS EN EL DISEÑO DE BLESSED GYM ---
PRIMARY_COLOR = "#F05D23"      # Naranja de BLESSED
SECONDARY_COLOR = "#FFFFFF"    # Blanco para texto
ACCENT_COLOR = "#F05D23"       # Naranja para acentos
BACKGROUND_DARK = "#0A0A0A"    # Fondo negro
CARD_BG = "#1A1A1A"           # Fondo de tarjetas oscuro
TEXT_PRIMARY = "#FFFFFF"       # Texto principal blanco
TEXT_SECONDARY = "#CCCCCC"     # Texto secundario gris claro

# --- RUTAS DE ARCHIVOS ---
# Rutas dinámicas que se ajustan automáticamente según la ubicación del proyecto
LOGO_PATH = os.path.join(IMG_DIR, 'logo.png')
BG_PATH = os.path.join(IMG_DIR, 'gym.jpg')
BG_PATH_CLIENT = os.path.join(IMG_DIR, 'bg_gym_client.jpg')
BG_PATH_ROL = os.path.join(IMG_DIR, 'BG_SEL_ROL.jpg')
ADMIN_ICON_PATH = os.path.join(IMG_DIR, 'ICO_ADMIN.png')
ADMIN_ICON_HOVER_PATH = os.path.join(IMG_DIR, 'ICO_ADMIN_2.png')
CLIENT_ICON_PATH = os.path.join(IMG_DIR, 'ICO_CLIENT.png')
CLIENT_ICON_HOVER_PATH = os.path.join(IMG_DIR, 'ICO_CLIENT_2.png')

# --- CONFIGURACIÓN DE LA APLICACIÓN ---
APP_TITLE = "BLESSED GYM"
APP_WIDTH = 1200
APP_HEIGHT = 800

# --- CONFIGURACIÓN DE BASE DE DATOS ---
DB_NAME = 'gimnasio.db'

# --- BACKEND API (para futuro uso) ---
API_BASE_URL = "http://localhost:8000"  # URL del backend cuando esté disponible
API_TIMEOUT = 30  # segundos

# --- CONFIGURACIÓN DE ZONA HORARIA ---
# El sistema detecta automáticamente la zona horaria del sistema operativo
# No es necesario configurar manualmente la zona horaria
