"""
Configuración global de la aplicación - Frontend Cliente (Tablet)
"""

# --- COLORES BASADOS EN EL DISEÑO DE BLESSED GYM ---
PRIMARY_COLOR = "#9FFF33"      # Verde Lima de BLESSED
SECONDARY_COLOR = "#FFFFFF"    # Blanco para texto
ACCENT_COLOR = "#9FFF33"       # Verde Lima para acentos
BACKGROUND_DARK = "#0A0A0A"    # Fondo negro
CARD_BG = "#1A1A1A"           # Fondo de tarjetas oscuro
TEXT_PRIMARY = "#FFFFFF"       # Texto principal blanco
TEXT_SECONDARY = "#CCCCCC"     # Texto secundario gris claro

# --- CONFIGURACIÓN DE LA APLICACIÓN ---
APP_TITLE = "BLESSED GYM - Cliente"
# Tamaño optimizado para tablets landscape (16:10 aspect ratio)
APP_WIDTH = 1280  # Tablet landscape (mejor resolución)
APP_HEIGHT = 800  # Tablet landscape (16:10 ratio)

# --- BACKEND API ---
API_BASE_URL = "http://localhost:8000"  # URL del backend
API_TIMEOUT = 30  # segundos

# --- CONFIGURACIÓN DE USUARIO SISTEMA ---
USUARIO_SISTEMA = "tablet_gym"  # Usuario que registra desde la tablet

# --- CONFIGURACIÓN DE RECURSOS ---
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, "img")
BACKGROUND_IMAGE = os.path.join(IMG_DIR, "BG.jpg")
