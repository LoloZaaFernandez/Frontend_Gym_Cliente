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
LOGO_PATH = r"C:\Sistema_Blessed_V2\Frontend_Gym_Cliente\frontend\img\logo.png" 
BG_PATH = r"C:\Sistema_Blessed_V2\Frontend_Gym_Cliente\frontend\img\gym.jpg"
BG_PATH_CLIENT = r"C:\Sistema_Blessed_V2\Frontend_Gym_Cliente\frontend\img\bg_gym_client.jpg" 
BG_PATH_ROL = r"C:\Sistema_Blessed_V2\Frontend_Gym_Cliente\frontend\img\BG_SEL_ROL.jpg"

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
TIMEZONE_OFFSET_HOURS = -5  # Perú (UTC-5)
