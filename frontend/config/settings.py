"""
Configuración global de la aplicación
"""
#config/settings.py
# --- COLORES BASADOS EN EL DISEÑO DE BLESSED GYM ---
PRIMARY_COLOR = "#F05D23"      # Naranja de BLESSED
SECONDARY_COLOR = "#FFFFFF"    # Blanco para texto
ACCENT_COLOR = "#F05D23"       # Naranja para acentos
BACKGROUND_DARK = "#0A0A0A"    # Fondo negro
CARD_BG = "#1A1A1A"           # Fondo de tarjetas oscuro
TEXT_PRIMARY = "#FFFFFF"       # Texto principal blanco
TEXT_SECONDARY = "#CCCCCC"     # Texto secundario gris claro

# --- RUTAS DE ARCHIVOS ---
LOGO_PATH = r"C:\FRONTEND V4\frontend\img\logo.png" 
BG_PATH = r"C:\FRONTEND V4\frontend\img\gym.jpg"
BG_PATH_CLIENT = r"C:\FRONTEND V4\frontend\img\bg_gym_client.jpg" 
BG_PATH_ROL = r"C:\FRONTEND V4\frontend\img\BG_SEL_ROL.jpg"
ADMIN_ICON_PATH = r"C:\FRONTEND V4\frontend\img\ICO_ADMIN.png"
ADMIN_ICON_HOVER_PATH = r"C:\FRONTEND V4\frontend\img\ICO_ADMIN_2.png"
CLIENT_ICON_PATH = r"C:\FRONTEND V4\frontend\img\ICO_CLIENT.png"
CLIENT_ICON_HOVER_PATH = r"C:\FRONTEND V4\frontend\img\ICO_CLIENT_2.png"

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
