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
# Tamaño optimizado para Redmi Pad SE 8.7" (800x1340 nativos)
# Configuración en modo horizontal (landscape) para mejor UX
APP_WIDTH = 1340  # Redmi Pad SE 8.7" en horizontal
APP_HEIGHT = 800  # Redmi Pad SE 8.7" en horizontal

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
