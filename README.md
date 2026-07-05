# Instagram Analytics — Followers, Following & Unfollowers Tracker

Herramienta en Python que analiza el archivo de descarga de datos de Instagram para detectar quién no te sigue de vuelta, quién dejó de seguirte y quién es nuevo en tus listas de seguidores/seguidos. Guarda un historial local en archivos de texto para comparar cada corrida contra la anterior.

## ¿Qué hace?

1. Descomprime automáticamente el `.zip` que exporta Instagram con tu información.
2. Lee los archivos JSON de `followers` y `following` de esa exportación.
3. Compara los datos actuales contra la última corrida guardada y muestra en consola:
   - Cantidad total de seguidores y seguidos (con la variación respecto a la corrida anterior).
   - Usuarios que dejaron de seguirte (**unfollowers**), indicando si vos seguís a esa persona o no.
   - Usuarios nuevos que empezaste a seguir o que te empezaron a seguir.
   - Un listado de los últimos registros guardados, a modo de referencia.
4. Persiste los resultados en archivos `.txt` (`users_followers.txt`, `users_following.txt`, `users_unfollowers.txt`) para poder comparar en la próxima ejecución.

Todo el análisis corre localmente: no se sube información a ningún servidor externo.

## Estructura del repositorio

| Archivo | Descripción |
|---|---|
| `conn_unzip.py` | Busca el `.zip` de Instagram en la carpeta del proyecto, borra la carpeta `connections` de una corrida anterior (si existe) y descomprime el nuevo archivo. |
| `conn_manage.py` | Contiene la lógica principal: importa followers/following desde el JSON, compara contra el historial guardado y muestra/guarda los resultados. |
| `main.ipynb` | Notebook que orquesta todo el proceso (descomprimir + analizar) y muestra los resultados de forma más legible. |
| `requirements.txt` | Dependencias del proyecto. |

## Requisitos

- Python 3.10+ (recomendado)
- Jupyter (para ejecutar `main.ipynb`)
- Dependencias listadas en `requirements.txt`:
  - `pandas==2.2.3`
  - `colorama==0.4.6`
  - `ipykernel==6.29.5`

## Instalación

```bash
git clone https://github.com/eli-carri/instagram-analytics.git
cd instagram-analytics
pip install -r requirements.txt
```

## Cómo obtener tus datos de Instagram

1. Entrá a **Instagram → Configuración → Centro de cuentas → Tu información y permisos → Exportar tu información**.
2. Elegí la opción de **descargar al dispositivo**.
3. Seleccioná únicamente el rubro **"Followers and following"** (no hace falta pedir toda tu información).
4. Configurá el rango de fechas, formato **JSON** y calidad de medios (no importa para este proyecto, ya que no se usan imágenes ni videos).
5. Instagram tarda entre 15 y 20 minutos (a veces más) en preparar el archivo. Vas a recibir una notificación cuando esté listo.
6. Descargá el `.zip` y colocalo en la raíz de este repositorio (junto a `main.ipynb`), sin descomprimirlo manualmente.

## Uso

1. Colocá el `.zip` descargado de Instagram en la carpeta del proyecto.
2. Abrí y ejecutá todas las celdas de `main.ipynb`.
3. El notebook va a:
   - Descomprimir el `.zip` (creando la carpeta `connections/`).
   - Analizar followers y following.
   - Mostrar en la salida un resumen con nuevos seguidores, unfollowers y estadísticas generales.
4. En corridas posteriores, simplemente reemplazá el `.zip` por una exportación más reciente y volvé a correr el notebook: el script compara automáticamente contra los archivos `.txt` generados la vez anterior.

Alternativamente, podés correr la lógica directamente desde la terminal:

```bash
python conn_unzip.py     # descomprime el zip de Instagram
python conn_manage.py    # analiza followers, following y unfollowers
```

## Archivos generados

Después de cada corrida vas a encontrar en la raíz del proyecto:

- `users_followers.txt` — lista de tus seguidores actuales.
- `users_following.txt` — lista de las cuentas que seguís.
- `users_unfollowers.txt` — cuentas que seguís (o seguiste) pero que no te siguen de vuelta.

Estos archivos son el "historial" que se usa para detectar cambios en la próxima ejecución, así que no conviene borrarlos entre corridas.

## Notas

- El proyecto no interactúa con la API de Instagram ni hace scraping: todo el análisis se hace sobre el export oficial de datos que provee la plataforma.
- No se almacena información sensible fuera de tu propia máquina.
- Si es la primera vez que corrés el script, no vas a tener archivo de historial previo, así que no habrá comparación de "nuevos" o "unfollowers" en esa primera corrida — solo se generará el snapshot inicial.
