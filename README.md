# despotify_helper

> **Versión en español más abajo / Spanish version below**

---

## English

Command-line script to build a local MP3 library from a Spotify playlist exported to CSV. It reads the CSV, searches each track on YouTube, downloads the best available audio, and saves it as MP3 organized by `Artist/Album/Track.mp3`.

### Why this exists

Music doesn't belong to platforms. It belongs to the people who make it and the people who listen to it. Streaming has spent a decade convincing us otherwise — that "access" is the same as having, that a monthly fee is the natural state of things, that our libraries should evaporate the moment we stop paying. It isn't, and they shouldn't.

despotify_helper is a small act of refusal. It exists to help you rebuild a music collection that is *yours*: files on your disk, playable offline, that no algorithm reshuffles, no licensing dispute removes overnight, and no company can take away when you cancel a subscription.

### About Spotify specifically

Spotify is the dominant player in music streaming, and the case against it has only grown. Music critic Frankie Pizá has written one of the sharpest recent analyses of why a boycott is both warranted and structurally difficult — recommended reading: ["¿Boicot a Spotify?... ¿Es justo? ¿Es imposible?"](https://www.zonafranka.es/boicot-a-spotify-es-justo-es-imposible/) (Franka, June 2025). The framing below leans on that piece.

- **It was never the heroic Swedish underdog.** The dominant origin story — pirates turn legit, save the industry from Napster — hides that the deal with the major labels (Universal, Sony, Warner) was locked in from day one, including equity stakes and editorial control of playlists. Spotify isn't competing with the majors; it's their algorithmic operating arm. A pact to preserve old privileges in new forms.
- **Artist exploitation.** Spotify's per-stream payouts are a fraction of a cent. Independent and mid-tier musicians describe the platform as structurally hostile to making a living from recorded music. The 2024 demonetization of tracks under 1,000 streams pushed the situation further: most working artists now earn literally nothing from a significant share of their catalog. Independent labels participate in the model believing it's neutral, but the design rewards volume and majority ownership — the share that reaches them is minuscule and uneven.
- **The business is the archive, not the music.** In 2023 Spotify sold two-thirds of its stake in DistroKid for $167M, after investing $18M five years earlier. DistroKid controls 30–40% of global DIY music uploads. Spotify understood early that profitability no longer depends on a song being heard, valued, or remembered — only on it being uploaded, indexed, and ready to be monetized. The platform is a cultural rentier: it doesn't produce, doesn't represent, doesn't create — it extracts.
- **The product is passive listening.** Spotify's own marketing ("there's no vroom-vroom without a playlist") treats music as a trigger for vegetative consumption. The strategic horizon is bland, predictable, mood-coded music — increasingly ghost artists and AI-generated tracks — that fills time without demanding attention. The catalog gets bigger and more homogeneous at once. Context, authorship, and cultural weight are the things being stripped out, on purpose.
- **Lock-in by design.** Your playlists, your listening history, the years you spent curating taste — none of it is portable. Spotify doesn't offer a built-in export. The fact that a third-party tool like Exportify has to exist at all is the point: your data is held hostage to keep you subscribed.
- **Daniel Ek's investments in military AI.** Spotify's CEO has personally invested hundreds of millions of euros — through his investment vehicle Prima Materia — into Helsing, a European defense company building AI-driven battlefield software, drones, and targeting systems. He led a €600M funding round in 2025 and chairs the company. Every Spotify Premium subscription contributes to the wealth that bankrolls this. Artists including Deerhoof, King Gizzard & the Lizard Wizard, Hotline TNT, and Xiu Xiu have pulled their music from the platform in protest.
- **Complicity in genocide.** Human rights organizations and a growing number of musicians have called out Spotify for continuing to operate normally, host state-aligned content, and platform Israeli military and government messaging during the ongoing genocide in Gaza — while artists who speak out face shadowbanning and reduced reach. The combination of Ek's defense-tech investments and the platform's editorial conduct has made "boycott Spotify" a real and growing movement.

You don't have to accept any of these specific framings to recognize the underlying point: handing your entire listening life to a single private company, run by people whose other investments you may find indefensible, is a choice — and it's a choice you can revisit.

### What this tool does, concretely

despotify_helper is for personal use: migrating off Spotify to a library you actually own, without depending on any streaming service.

### How it fits with Exportify

Spotify doesn't let you export your playlists. [Exportify](https://watsonbox.github.io/exportify/) is a small open-source web app that, via OAuth against your account, dumps a playlist to CSV with all its metadata (Track Name, Artist Name(s), Album Name, Track URI, etc.).

despotify_helper consumes exactly that CSV. The full flow:

1. Open Exportify in your browser and grant access to your Spotify account.
2. Pick the playlist (or "Liked Songs", or "Followed Albums") and download the CSV.
3. Pass that CSV to despotify_helper.

No intermediate step: the Exportify format is the input format.

### Requirements

- macOS, Linux, or Windows (each with its own script — see below).
- `python3` (3.9 or higher; only uses stdlib).
- `yt-dlp` in PATH.
- `ffmpeg` in PATH (used by yt-dlp to extract and transcode to MP3).

### Which script do I run?

- **macOS / Linux** → `despotify_helper.py`
- **Windows** → `despotify_helper_windows.py` (same logic, with adjustments for Windows: hides the `yt-dlp` console window via `CREATE_NO_WINDOW`, handles reserved filenames like `CON`, `PRN`, `NUL`, strips trailing dots/spaces from folder names, and reads UTF-8 CSV with BOM via `utf-8-sig`).

### Installation

On macOS with Homebrew:

```sh
brew install yt-dlp ffmpeg
```

On Linux, use your package manager (`apt install yt-dlp ffmpeg`, `pacman -S yt-dlp ffmpeg`, etc.).

On Windows with [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/):

```powershell
winget install yt-dlp.yt-dlp
winget install Gyan.FFmpeg
```

Or with [Chocolatey](https://chocolatey.org/):

```powershell
choco install yt-dlp ffmpeg
```

Then clone or copy this repo wherever you like. There are no Python dependencies to install: the script only imports stdlib modules and calls `yt-dlp` via subprocess.

> Note: installing `yt-dlp` from a system package manager (Homebrew, winget, Chocolatey) instead of `pip install yt-dlp` brings the binary with its own embedded Python and updates with the package manager. YouTube extractors change often, so keeping the version up to date matters.

### Usage

macOS / Linux:

```sh
python3 despotify_helper.py <path_to_csv>
```

Example:

```sh
python3 despotify_helper.py ~/Downloads/Favorite_albums.csv
```

Windows (PowerShell or `cmd`):

```powershell
python despotify_helper_windows.py <path_to_csv>
```

Example:

```powershell
python despotify_helper_windows.py %USERPROFILE%\Downloads\Favorite_albums.csv
```

The script prints track-by-track progress and, at the end, a summary with downloaded / already existing / failed, plus the list of failures with their reason.

If you want to save a log to review failures later:

```sh
python3 despotify_helper.py ~/Downloads/my_playlist.csv 2>&1 | tee ~/Music/despotify_helper/despotify_helper.log
```

#### Resumable

The script checks whether each final `.mp3` already exists before downloading. You can stop it with Ctrl-C at any time and relaunch: it will pick up where it left off without redownloading anything.

#### Retries

If a song fails the first time (typically due to a transient YouTube error), just relaunch the same command: the ones already on disk are skipped and only the missing ones are retried.

### Output structure

macOS / Linux:

```
~/Music/despotify_helper/
  <Artist>/
    <Album>/
      <Track>.mp3
```

Windows:

```
%USERPROFILE%\Music\despotify_helper\
  <Artist>\
    <Album>\
      <Track>.mp3
```

Naming rules:

- Folder artist: if the `Artist Name(s)` field has multiple comma-separated artists, only the first one is used (avoids duplicate folders like `Artist A, Artist B`). The YouTube search does use the full list, to improve matching.
- Invalid filename characters (`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`, NUL) are replaced with `_`.
- On Windows, trailing dots/spaces are stripped and reserved names (`CON`, `PRN`, `AUX`, `NUL`, `COM1`–`COM9`, `LPT1`–`LPT9`) are prefixed with `_`.
- Accents, ñ, apostrophes and other Unicode are preserved.

MP3s are generated at 192 kbps. If you want different quality, change `--audio-quality 192K` in the script you're using.

### Common errors and how to solve them

#### `yt-dlp is not in PATH` / `ffmpeg is not in PATH`

The script checks both at startup. Install them with `brew install yt-dlp ffmpeg`.

#### `HTTP Error 403: Forbidden` when downloading

YouTube periodically changes how it serves audio and old extractors stop working. If this happens:

```sh
brew upgrade yt-dlp
```

If it persists after updating, it's usually resolved by passing browser cookies to yt-dlp. Edit the `download` function in `despotify_helper.py` and add to `cmd`:

```python
"--cookies-from-browser", "chrome",   # or "firefox", "safari", "brave"...
```

#### `Missing columns in CSV: {...}`

The script expects exactly the columns produced by Exportify: `Track Name`, `Album Name`, `Artist Name(s)`. If you exported with another tool (TuneMyMusic, Soundiiz, etc.), open the CSV and rename the headers to those three names.

#### `timeout (>5min)` on some song

A stuck download. Relaunch the script: it will only retry the missing ones. If a specific track always gets stuck, raise the timeout in `DOWNLOAD_TIMEOUT_S` inside the script, or look it up by hand on YouTube and use it as an exception.

#### The downloaded song is not the right one

`ytsearch1` takes the first YouTube result for `"<artists> - <title>"`. On obscure songs or those with many covers/remixes, it can pick the wrong one. Solutions:

- Delete the wrong `.mp3` and relaunch the script with a modified version of the query (for example, adding `audio` or `official` in `build_query` / `download`).
- Or download that track manually with `yt-dlp -x --audio-format mp3 "VIDEO_URL"` and place it in its folder.

#### `Track Name`, `Album Name` or `Artist Name(s)` empty

Appears as `SKIPPED (incomplete data)` in the log and counts 1 toward failures. Edit the CSV to complete the row and relaunch.

#### `Python version 3.9 has been deprecated` (when using `yt-dlp` as pip library)

Doesn't affect this script, which calls `yt-dlp` via subprocess (the Homebrew binary brings its own Python 3.14). You'd only see that warning if you once installed `yt-dlp` with `pip` on Python 3.9. Uninstall that pip version and use the Homebrew one.

### Legal considerations

YouTube's terms of service prohibit downloading content without permission. The legality of downloading for personal use varies by jurisdiction (in some, there are private-copy exceptions; in others, not). This tool is offered only for personal use on music you already have the right to listen to. Responsibility for use lies with the user.

We'd also note: many of the same companies that aggressively enforce these terms are the ones whose business models we're stepping away from in the first place. The moral picture is not as one-sided as the EULA suggests. Decide for yourself.

### How it works inside

`despotify_helper.py` is a ~100-line script. For each row in the CSV:

1. Sanitizes the fields for use as a file path.
2. Builds the final path `~/Music/despotify_helper/<Artist>/<Album>/<Track>.mp3`.
3. If that path already exists, skips.
4. If not, launches `yt-dlp ytsearch1:"<artists> - <title>"` with `-x --audio-format mp3 --audio-quality 192K` and the output template pointing to the destination.
5. Captures return code and stderr to report failures without aborting the batch.

There is no persistent state beyond the downloaded files; the "state" of the job is the contents of the output directory.

---

## Español

Script de línea de comandos para construir una fonoteca local en MP3 a partir de una playlist de Spotify exportada a CSV. Lee el CSV, busca cada canción en YouTube, descarga el mejor audio disponible y lo guarda como MP3 ordenado por `Artista/Álbum/Canción.mp3`.

### Por qué existe esto

La música no pertenece a las plataformas. Pertenece a la gente que la hace y a la gente que la escucha. El streaming lleva una década convenciéndonos de lo contrario: que "acceder" es lo mismo que tener, que una cuota mensual es el orden natural de las cosas, que nuestras bibliotecas deberían evaporarse en el momento en que dejemos de pagar. No es así, y no debería ser así.

despotify_helper es un pequeño gesto de negativa. Existe para ayudarte a reconstruir una colección de música que es *tuya*: ficheros en tu disco, reproducibles sin conexión, que ningún algoritmo reordena, que ninguna disputa de licencias retira de un día para otro, y que ninguna empresa puede quitarte cuando canceles una suscripción.

### Sobre Spotify en concreto

Spotify es el actor dominante del streaming musical, y los argumentos en su contra solo se han ido acumulando. El crítico Frankie Pizá ha escrito uno de los análisis recientes más afilados sobre por qué un boicot está justificado y a la vez es estructuralmente difícil — lectura muy recomendada: ["¿Boicot a Spotify?... ¿Es justo? ¿Es imposible?"](https://www.zonafranka.es/boicot-a-spotify-es-justo-es-imposible/) (Franka, junio de 2025). El planteamiento que sigue se apoya en ese texto.

- **Nunca fue el heroico underdog sueco.** El relato dominante — piratas que se legalizan y salvan a la industria de Napster — esconde que el acuerdo con las majors (Universal, Sony, Warner) estaba cerrado desde el principio, con participación accionarial y control editorial de las playlists. Spotify no compite con las majors: es su brazo operativo algorítmico. Un pacto para preservar viejos privilegios bajo nuevas formas.
- **Explotación de artistas.** Lo que Spotify paga por reproducción es una fracción de céntimo. Músicos independientes y de tamaño medio describen la plataforma como estructuralmente hostil a ganarse la vida con la música grabada. La desmonetización en 2024 de las pistas con menos de 1.000 reproducciones empeoró la situación: la mayoría de artistas profesionales ya no cobra literalmente nada por una parte significativa de su catálogo. Los sellos independientes participan en el modelo creyendo que es neutral, pero el diseño premia volumen y propiedad mayoritaria — la porción que les llega es ínfima y desigual.
- **El negocio es el archivo, no la música.** En 2023 Spotify vendió dos tercios de su participación en DistroKid por 167M$, tras haber invertido 18M$ cinco años antes. DistroKid controla entre el 30% y el 40% de los uploads DIY a nivel global. Spotify entendió pronto que la rentabilidad ya no depende de que una canción sea escuchada, valorada o recordada — basta con que sea subida, indexada y esté lista para ser rentabilizada. La plataforma funciona como un rentista cultural: no produce, no representa, no crea — extrae.
- **El producto es la escucha pasiva.** El propio marketing de Spotify ("sin playlist no hay vroom-vroom") trata la música como disparador de un consumo vegetativo. El horizonte estratégico es música blanda, predecible, codificada por mood — cada vez más artistas fantasma y pistas generadas por IA — que rellena el tiempo sin pedir atención. El catálogo se hace más grande y más homogéneo a la vez. Lo que se está despojando, a propósito, es el contexto, la autoría y el peso cultural.
- **Encerrona por diseño.** Tus playlists, tu historial de escucha, los años que dedicaste a cultivar tu gusto: nada de eso es portable. Spotify no ofrece exportación nativa. El hecho de que tenga que existir una herramienta externa como Exportify *es* el problema: tus datos están secuestrados para mantenerte suscrito.
- **Las inversiones de Daniel Ek en IA militar.** El CEO de Spotify ha invertido personalmente cientos de millones de euros — a través de su vehículo de inversión Prima Materia — en Helsing, una empresa europea de defensa que construye software de combate basado en IA, drones y sistemas de selección de objetivos. Lideró una ronda de financiación de 600M€ en 2025 y preside la empresa. Cada suscripción a Spotify Premium contribuye a la riqueza que financia esto. Artistas como Deerhoof, King Gizzard & the Lizard Wizard, Hotline TNT y Xiu Xiu han retirado su música de la plataforma en señal de protesta.
- **Complicidad con un genocidio.** Organizaciones de derechos humanos y un número creciente de músicos han señalado a Spotify por seguir operando con total normalidad, alojar contenidos alineados con un Estado y dar altavoz a mensajes del gobierno y el ejército israelíes durante el genocidio en curso en Gaza, mientras que artistas que se posicionan en contra sufren shadowban y pérdida de alcance. La combinación de las inversiones en tecnología militar de Ek y la conducta editorial de la plataforma ha convertido el "boycott Spotify" en un movimiento real y al alza.

No hace falta asumir ninguno de estos encuadres concretos para reconocer el punto de fondo: entregar toda tu vida como oyente a una sola empresa privada, dirigida por personas cuyas otras inversiones puedes considerar indefendibles, es una elección — y es una elección que puedes revisar.

### Lo que hace esta herramienta, en concreto

Pensado para uso personal: migrar de Spotify a una biblioteca propia sin depender de ningún servicio en streaming.

### Cómo encaja con Exportify

Spotify no permite exportar tus playlists. [Exportify](https://watsonbox.github.io/exportify/) es una pequeña app web open-source que, vía OAuth contra tu cuenta, vuelca una playlist a CSV con todos sus metadatos (Track Name, Artist Name(s), Album Name, Track URI, etc.).

despotify_helper consume exactamente ese CSV. El flujo completo es:

1. Abres Exportify en el navegador y le das acceso a tu cuenta de Spotify.
2. Eliges la playlist (o "Liked Songs", o "Followed Albums") y descargas el CSV.
3. Le pasas ese CSV a despotify_helper.

No hay paso intermedio: el formato Exportify es el formato de entrada.

### Requisitos

- macOS, Linux o Windows (cada uno con su propio script — ver abajo).
- `python3` (3.9 o superior; solo usa la stdlib).
- `yt-dlp` en el PATH.
- `ffmpeg` en el PATH (lo usa yt-dlp para extraer y transcodificar a MP3).

### ¿Qué script ejecuto?

- **macOS / Linux** → `despotify_helper.py`
- **Windows** → `despotify_helper_windows.py` (misma lógica, con ajustes propios de Windows: oculta la ventana de consola de `yt-dlp` mediante `CREATE_NO_WINDOW`, gestiona nombres reservados como `CON`, `PRN`, `NUL`, recorta puntos y espacios al final de los nombres de carpeta, y lee el CSV en UTF-8 con BOM mediante `utf-8-sig`).

### Instalación

En macOS con Homebrew:

```sh
brew install yt-dlp ffmpeg
```

En Linux, con el gestor de paquetes correspondiente (`apt install yt-dlp ffmpeg`, `pacman -S yt-dlp ffmpeg`, etc.).

En Windows con [winget](https://learn.microsoft.com/es-es/windows/package-manager/winget/):

```powershell
winget install yt-dlp.yt-dlp
winget install Gyan.FFmpeg
```

O con [Chocolatey](https://chocolatey.org/):

```powershell
choco install yt-dlp ffmpeg
```

Después clona o copia este repo donde quieras. No hay dependencias Python que instalar: el script solo importa módulos de la biblioteca estándar y llama a `yt-dlp` por subprocess.

> Nota: instalar `yt-dlp` desde un gestor de paquetes del sistema (Homebrew, winget, Chocolatey) en lugar de `pip install yt-dlp` trae el binario con su propio Python embebido y se actualiza con el gestor. Los extractors de YouTube cambian a menudo, por lo que tener la versión al día es importante.

### Uso

macOS / Linux:

```sh
python3 despotify_helper.py <ruta_al_csv>
```

Ejemplo:

```sh
python3 despotify_helper.py ~/Downloads/Discos_favoritos.csv
```

Windows (PowerShell o `cmd`):

```powershell
python despotify_helper_windows.py <ruta_al_csv>
```

Ejemplo:

```powershell
python despotify_helper_windows.py %USERPROFILE%\Downloads\Discos_favoritos.csv
```

El script imprime el progreso pista a pista y, al final, un resumen con descargadas / ya existentes / fallidas, más la lista de fallos con su motivo.

Si quieres guardar log para revisar fallos a posteriori:

```sh
python3 despotify_helper.py ~/Downloads/mi_playlist.csv 2>&1 | tee ~/Music/despotify_helper/despotify_helper.log
```

#### Resumible

El script comprueba si cada `.mp3` final ya existe antes de descargar. Puedes pararlo con Ctrl-C en cualquier momento y volver a lanzarlo: retomará por donde iba sin rebajar nada.

#### Reintentos

Si una canción falla la primera vez (típicamente por un error transitorio de YouTube), basta con relanzar el mismo comando: las que estén en disco se saltan y solo se reintentan las que faltan.

### Estructura de salida

macOS / Linux:

```
~/Music/despotify_helper/
  <Artista>/
    <Álbum>/
      <Canción>.mp3
```

Windows:

```
%USERPROFILE%\Music\despotify_helper\
  <Artista>\
    <Álbum>\
      <Canción>.mp3
```

Reglas de nombrado:

- Artista de la carpeta: si el campo `Artist Name(s)` tiene varios artistas separados por coma, se usa solo el primero (evita carpetas duplicadas tipo `Artista A, Artista B`). La búsqueda en YouTube sí usa la lista completa, para mejorar el matching.
- Caracteres inválidos en nombre de fichero (`/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`, NUL) se reemplazan por `_`.
- En Windows, además se recortan puntos/espacios al final del nombre y los nombres reservados (`CON`, `PRN`, `AUX`, `NUL`, `COM1`–`COM9`, `LPT1`–`LPT9`) se prefijan con `_`.
- Se preservan acentos, eñes, apóstrofes y demás Unicode.

Los MP3 se generan a 192 kbps. Si quieres otra calidad, cambia `--audio-quality 192K` en el script que estés usando.

### Errores frecuentes y cómo resolverlos

#### `yt-dlp no está en el PATH` / `ffmpeg no está en el PATH`

El script comprueba ambos al arrancar. Instálalos con `brew install yt-dlp ffmpeg`.

#### `HTTP Error 403: Forbidden` al descargar

YouTube cambia periódicamente la forma de servir el audio y los extractors antiguos dejan de funcionar. Si te pasa:

```sh
brew upgrade yt-dlp
```

Si persiste tras actualizar, suele resolverse pasando cookies de tu navegador a yt-dlp. Edita la función `download` en `despotify_helper.py` y añade al `cmd`:

```python
"--cookies-from-browser", "chrome",   # o "firefox", "safari", "brave"...
```

#### `Faltan columnas en el CSV: {...}`

El script espera exactamente las columnas que produce Exportify: `Track Name`, `Album Name`, `Artist Name(s)`. Si exportaste con otra herramienta (TuneMyMusic, Soundiiz, etc.), abre el CSV y renombra las cabeceras a esos tres nombres.

#### `timeout (>5min)` en alguna canción

Una descarga colgada. Relanza el script: solo reintentará las que falten. Si una pista concreta se queda siempre colgada, sube el timeout en `DOWNLOAD_TIMEOUT_S` dentro del script, o búscala a mano en YouTube y úsala como excepción.

#### La canción descargada no es la correcta

`ytsearch1` toma el primer resultado de YouTube para `"<artistas> - <título>"`. En canciones poco conocidas o con muchos covers/remixes, puede coger el equivocado. Soluciones:

- Borra el `.mp3` mal descargado y relanza el script con una versión modificada de la query (por ejemplo, añadiendo `audio` u `official` en `build_query` / `download`).
- O descarga esa pista a mano con `yt-dlp -x --audio-format mp3 "URL_DEL_VÍDEO"` y colócala en su sitio.

#### `Track Name`, `Album Name` o `Artist Name(s)` vacío

Aparece como `SALTADA (datos incompletos)` en el log y suma 1 a fallidas. Edita el CSV para completar la fila y relanza.

#### `Python version 3.9 has been deprecated` (al usar `yt-dlp` como librería pip)

No afecta a este script, que llama a `yt-dlp` por subprocess (el binario de Homebrew trae su propio Python 3.14). Solo verías ese aviso si en su día instalaste `yt-dlp` con `pip` sobre Python 3.9. Desinstala esa versión pip y usa la de Homebrew.

### Consideraciones legales

Las condiciones de servicio de YouTube prohíben descargar contenido sin permiso. La legalidad de descargar para uso personal varía por jurisdicción (en algunas, hay excepciones por copia privada; en otras, no). Esta herramienta se ofrece solo para uso personal sobre música que ya tienes derecho a escuchar. La responsabilidad del uso es del usuario.

Añadiríamos también: muchas de las mismas empresas que aplican estos términos de forma agresiva son aquellas cuyos modelos de negocio estamos abandonando precisamente con esto. El cuadro moral no es tan unilateral como sugiere el EULA. Decide por ti mismo.

### Cómo funciona por dentro

`despotify_helper.py` es un script de ~100 líneas. Para cada fila del CSV:

1. Sanitiza los campos para uso como ruta de fichero.
2. Construye la ruta final `~/Music/despotify_helper/<Artista>/<Álbum>/<Canción>.mp3`.
3. Si esa ruta ya existe, salta.
4. Si no, lanza `yt-dlp ytsearch1:"<artistas> - <título>"` con `-x --audio-format mp3 --audio-quality 192K` y la plantilla de salida apuntando al destino.
5. Captura código de retorno y stderr para reportar fallos sin abortar el lote.

No hay estado persistente más allá de los ficheros descargados; el "estado" del trabajo es el contenido del directorio de salida.