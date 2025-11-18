# Configuración de API - Guía de Uso

## Descripción

La aplicación ahora incluye un sistema de configuración flexible que permite establecer dinámicamente la dirección IP y puerto del servidor API. Esto es especialmente útil cuando:

- El servidor está en una laptop en la red local
- La IP del servidor cambia frecuentemente
- Necesitas conectar a diferentes servidores (desarrollo, producción, etc.)

## Características

✅ **Configuración Persistente**: La configuración se guarda en un archivo JSON local
✅ **Interfaz Visual**: Vista amigable para configurar IP, puerto y timeout
✅ **Prueba de Conexión**: Verifica la conectividad antes de guardar
✅ **Ícono de Acceso Rápido**: Tuerca en la esquina superior derecha de la pantalla inicial
✅ **Valores por Defecto**: localhost:8000 como configuración inicial

## Acceso a la Configuración

### Desde la Pantalla Inicial

1. En la pantalla inicial, busca el **ícono de tuerca (⚙️)** en la esquina superior derecha
2. Haz clic en el ícono para abrir la vista de configuración

### Desde Pantalla de Error de Conexión

Si no se puede conectar al servidor, aparecerá un botón **"Configurar"** junto a **"Reintentar"**.

## Cómo Configurar la IP del Servidor

### Paso 1: Obtener la IP de tu Laptop

En la laptop donde corre el backend:

**Windows:**
```bash
ipconfig
```
Busca "Dirección IPv4" (ej: `192.168.1.100`)

**Linux/Mac:**
```bash
ifconfig
# o
ip addr show
```
Busca la IP en la interfaz de red activa (ej: `192.168.1.100`)

### Paso 2: Configurar en la Tablet

1. Abre la configuración (ícono de tuerca)
2. Ingresa los siguientes datos:
   - **IP o Hostname**: La IP de tu laptop (ej: `192.168.1.100`)
   - **Puerto**: `8000` (o el puerto que uses)
   - **Timeout**: `30` segundos (recomendado)

3. Presiona **"Probar Conexión"** para verificar
   - ✅ Si ve "Conexión exitosa", todo está bien
   - ❌ Si falla, verifica:
     - La IP esté correcta
     - El servidor esté corriendo
     - Ambos dispositivos estén en la misma red

4. Presiona **"Guardar"** para almacenar la configuración

### Paso 3: Usar la Aplicación

La aplicación ahora usará la nueva configuración. No necesitas reiniciarla.

## Ejemplos de Configuración

### Laptop en Red Local
```
IP: 192.168.1.100
Puerto: 8000
Timeout: 30
```

### Servidor en la Misma Máquina (Desarrollo)
```
IP: localhost
Puerto: 8000
Timeout: 30
```

### Servidor con IP Estática
```
IP: 10.0.0.50
Puerto: 8000
Timeout: 30
```

## Validaciones

La vista de configuración valida automáticamente:

- ✅ **IP**: Formato válido de IPv4 o hostname
- ✅ **Puerto**: Entre 1 y 65535
- ✅ **Timeout**: Entre 5 y 300 segundos

## Archivo de Configuración

La configuración se guarda en:
```
frontendApk/app_config.json
```

**Formato del archivo:**
```json
{
    "api_host": "192.168.1.100",
    "api_port": 8000,
    "api_timeout": 30
}
```

⚠️ **Nota**: Este archivo está en `.gitignore` y no se sube al repositorio (es específico de cada tablet).

## Restablecer Configuración

Si necesitas volver a los valores por defecto:

1. Abre la configuración
2. Presiona **"Restablecer valores por defecto"**
3. Los valores volverán a:
   - IP: `localhost`
   - Puerto: `8000`
   - Timeout: `30`

## Solución de Problemas

### "No se pudo conectar"

**Posibles causas:**

1. **IP incorrecta**: Verifica que la IP sea la correcta
   ```bash
   # En la laptop
   ping 192.168.1.100
   ```

2. **Puerto bloqueado**: Verifica que el puerto 8000 esté abierto
   ```bash
   # En la laptop (Windows)
   netstat -an | findstr :8000

   # En la laptop (Linux/Mac)
   lsof -i :8000
   ```

3. **Firewall**: Permite el puerto 8000 en el firewall de la laptop
   ```bash
   # Windows: Agregar regla en Windows Defender Firewall
   # Linux: sudo ufw allow 8000
   ```

4. **Diferentes redes**: Asegúrate de que la tablet y la laptop estén en la misma red Wi-Fi

### "IP o hostname inválido"

- Verifica el formato: `192.168.1.100` (4 números separados por puntos)
- Cada número debe estar entre 0 y 255
- No uses espacios ni caracteres especiales

### Configuración no se guarda

- Verifica permisos de escritura en el directorio de la aplicación
- Revisa la consola para errores

## Tips de Red Local

### Para Conexión Estable:

1. **Asigna IP Estática a la Laptop**:
   - En el router, reserva la IP para la MAC de la laptop
   - O configura IP estática en la laptop

2. **Usa Hostname** (si está configurado):
   ```
   IP: laptop-blessed-gym
   Puerto: 8000
   ```

3. **Verifica Conectividad**:
   ```bash
   # Desde la tablet (si tienes terminal)
   ping 192.168.1.100

   # Desde la tablet (navegador)
   http://192.168.1.100:8000/health
   ```

## Archivos Modificados

La funcionalidad de configuración incluye:

- **utils/config_manager.py**: Gestor de configuración persistente
- **views/configuracion_view.py**: Vista de configuración de API
- **views/pantalla_inicial.py**: Ícono de configuración agregado
- **main.py**: Integración de configuración dinámica
- **.gitignore**: Excluye `app_config.json`

## Seguridad

⚠️ **Importante**:
- La configuración se guarda en texto plano
- No incluyas credenciales sensibles
- Solo funciona en redes locales confiables
- No expongas el servidor a internet sin autenticación

## Soporte

Si tienes problemas:
1. Verifica los logs en la consola
2. Prueba con `localhost` primero
3. Usa "Probar Conexión" antes de guardar
4. Consulta con el personal técnico
