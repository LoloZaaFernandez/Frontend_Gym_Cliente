"""
Gestor de Configuración - Almacenamiento persistente de configuración de API
Permite guardar y cargar la IP y puerto del servidor API
"""
import json
import os


class ConfigManager:
    """Gestor de configuración de la aplicación"""

    def __init__(self, config_file: str = "app_config.json"):
        """
        Inicializar gestor de configuración

        Args:
            config_file: Nombre del archivo de configuración
        """
        # Ruta del archivo de configuración (en el directorio raíz del proyecto)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(base_dir, config_file)

        # Configuración por defecto
        self.default_config = {
            "api_host": "localhost",
            "api_port": 8000,
            "api_timeout": 30
        }

        # Cargar configuración existente o crear nueva
        self.config = self.load_config()

    def load_config(self) -> dict:
        """
        Cargar configuración desde archivo

        Returns:
            Diccionario con la configuración
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    print(f"✓ Configuración cargada desde {self.config_path}")
                    return config
            except Exception as e:
                print(f"⚠ Error al cargar configuración: {e}")
                print("  Usando configuración por defecto")
                return self.default_config.copy()
        else:
            print(f"ℹ Archivo de configuración no encontrado. Usando valores por defecto.")
            return self.default_config.copy()

    def save_config(self) -> bool:
        """
        Guardar configuración en archivo

        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            print(f"✓ Configuración guardada en {self.config_path}")
            return True
        except Exception as e:
            print(f"✗ Error al guardar configuración: {e}")
            return False

    def get_api_base_url(self) -> str:
        """
        Obtener URL base del API

        Returns:
            URL completa (ej: http://192.168.1.100:8000)
        """
        host = self.config.get("api_host", "localhost")
        port = self.config.get("api_port", 8000)
        return f"http://{host}:{port}"

    def get_api_timeout(self) -> int:
        """
        Obtener timeout del API

        Returns:
            Timeout en segundos
        """
        return self.config.get("api_timeout", 30)

    def set_api_config(self, host: str, port: int, timeout: int = 30) -> bool:
        """
        Establecer configuración del API

        Args:
            host: IP o hostname del servidor
            port: Puerto del servidor
            timeout: Timeout en segundos

        Returns:
            True si se guardó correctamente
        """
        self.config["api_host"] = host
        self.config["api_port"] = port
        self.config["api_timeout"] = timeout
        return self.save_config()

    def reset_to_default(self) -> bool:
        """
        Resetear configuración a valores por defecto

        Returns:
            True si se guardó correctamente
        """
        self.config = self.default_config.copy()
        return self.save_config()

    def get_config_summary(self) -> str:
        """
        Obtener resumen de la configuración actual

        Returns:
            String con resumen de configuración
        """
        return (
            f"Host: {self.config.get('api_host', 'N/A')}\n"
            f"Puerto: {self.config.get('api_port', 'N/A')}\n"
            f"URL: {self.get_api_base_url()}\n"
            f"Timeout: {self.config.get('api_timeout', 'N/A')}s"
        )


# Instancia global del gestor de configuración
_config_manager = None

def get_config_manager() -> ConfigManager:
    """
    Obtener instancia global del gestor de configuración (Singleton)

    Returns:
        Instancia de ConfigManager
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
