# Carpeta de Imágenes

## Instrucciones para QR de Yape

Para que el sistema muestre el código QR de Yape durante el proceso de registro:

1. **Genera tu código QR de Yape** (desde la app de Yape o tu banco)
2. **Guarda la imagen con el nombre**: `yape_qr.png`
3. **Coloca el archivo en esta carpeta**: `C:\FRONTEND V4\FRONTEND PARA CLIENTE\img\`

### Ruta completa del archivo:
```
C:\FRONTEND V4\FRONTEND PARA CLIENTE\img\yape_qr.png
```

### Formatos soportados:
- PNG (recomendado)
- JPG/JPEG
- Si usas otro formato, renombra la extensión en `views/registro_view.py` línea 584

### Comportamiento:
- ✅ **Si el archivo existe**: Se mostrará el QR cuando el cliente seleccione "Yape" como método de pago
- ⚠️ **Si NO existe**: Se mostrará un mensaje indicando que debe pagar con el personal del gimnasio

---

## Otras imágenes

Puedes agregar otras imágenes que necesite la aplicación en esta carpeta:
- Logos
- Banners
- Iconos personalizados
- Etc.
