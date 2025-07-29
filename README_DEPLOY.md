# Despliegue en Render - Backend AG

## Archivos de Configuración Creados

### 1. `build.sh`
Script de construcción que Render ejecutará durante el despliegue:
- Instala las dependencias desde `requirements.txt`
- Ejecuta las migraciones de Django
- Recolecta archivos estáticos

### 2. `requirements.txt`
Lista de dependencias de Python incluyendo:
- Django y Django REST Framework
- Gunicorn (servidor WSGI para producción)
- Whitenoise (para servir archivos estáticos)
- dj-database-url (para configuración de base de datos)

### 3. `render.yaml`
Configuración de Render para despliegue automático:
- Define el servicio web
- Configura la base de datos PostgreSQL
- Establece variables de entorno

### 4. `.gitignore`
Excluye archivos innecesarios del repositorio

## Pasos para Desplegar en Render

### 1. Preparar el Repositorio
```bash
# Asegúrate de que todos los archivos estén en tu repositorio Git
git add .
git commit -m "Configuración para Render"
git push origin main
```

### 2. Crear Cuenta en Render
1. Ve a [render.com](https://render.com)
2. Crea una cuenta o inicia sesión
3. Conecta tu repositorio de GitHub

### 3. Desplegar el Servicio
1. En Render Dashboard, haz clic en "New +"
2. Selecciona "Web Service"
3. Conecta tu repositorio de GitHub
4. Configura el servicio:
   - **Name**: `backend-ag-api`
   - **Environment**: `Python 3`
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn tutorial.wsgi:application --bind 0.0.0.0:$PORT`

### 4. Configurar Variables de Entorno
En la sección "Environment" del servicio, agrega:
- `SECRET_KEY`: (Render lo generará automáticamente)
- `DEBUG`: `False` (para producción)
- `DATABASE_URL`: (se configurará automáticamente si usas la base de datos de Render)

### 5. Crear Base de Datos (Opcional)
Si quieres usar la base de datos de Render:
1. Ve a "New +" → "PostgreSQL"
2. Configura la base de datos
3. Render automáticamente conectará la base de datos al servicio web

## Comandos Útiles

### Verificar el Despliegue
```bash
# Ver logs en tiempo real
# (desde el dashboard de Render)

# Verificar que la API responde
curl https://tu-app.onrender.com/api/
```

### Comandos Locales para Desarrollo
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver
```

## Estructura del Proyecto
```
Backend-Ag-main/
├── api/                    # Aplicación Django
├── tutorial/              # Configuración del proyecto
├── manage.py             # Script de gestión de Django
├── requirements.txt      # Dependencias de Python
├── build.sh             # Script de construcción para Render
├── render.yaml          # Configuración de Render
├── .gitignore           # Archivos a ignorar
└── README_DEPLOY.md     # Este archivo
```

## Notas Importantes

1. **Base de Datos**: El proyecto está configurado para usar PostgreSQL. Si usas la base de datos de Render, se configurará automáticamente.

2. **Archivos Estáticos**: Whitenoise está configurado para servir archivos estáticos en producción.

3. **Seguridad**: 
   - `DEBUG=False` en producción
   - `SECRET_KEY` se genera automáticamente
   - `ALLOWED_HOSTS` incluye dominios de Render

4. **Logs**: Puedes ver los logs de la aplicación desde el dashboard de Render.

## Solución de Problemas

### Error de Migraciones
Si hay errores en las migraciones:
1. Ve a los logs de Render
2. Ejecuta manualmente: `python manage.py migrate`

### Error de Dependencias
Si hay problemas con las dependencias:
1. Verifica que `requirements.txt` esté en la raíz
2. Asegúrate de que todas las dependencias estén listadas

### Error de Base de Datos
Si hay problemas de conexión:
1. Verifica que `DATABASE_URL` esté configurada
2. Asegúrate de que la base de datos esté activa en Render 