<div align="center">

```
                             ███████╗ ██████╗ ██████╗      ██╗ █████╗ ██╗  ██╗
                             ██╔════╝██╔═══██╗██╔══██╗     ██║██╔══██╗╚██╗██╔╝
                            █████╗  ██║   ██║██████╔╝     ██║███████║ ╚███╔╝
                            ██╔══╝  ██║   ██║██╔══██╗██   ██║██╔══██║ ██╔██╗
                             ██║     ╚██████╔╝██║  ██║╚█████╔╝██║  ██║██╔╝╚██╗
                             ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
```

🔥 **Empaquetador y ofuscador multi-lenguaje** 🔥

![Version](https://img.shields.io/badge/version-2.0.0-orange)
![Python](https://img.shields.io/badge/python-3.7+-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Author](https://img.shields.io/badge/by-XorSvn-red)

</div>

---

## ¿Qué es ForjaX?

**ForjaX** es una herramienta de línea de comandos desarrollada en Python que permite empaquetar scripts de múltiples lenguajes de programación en archivos ejecutables, así como ofuscar su código fuente para protegerlo de miradas no autorizadas. Presenta una interfaz interactiva con colores ANSI, menús guiados y detección automática de herramientas disponibles en el sistema.

---
## 🛡️ Enfoque en ciberseguridad

Como parte del proyecto, desarrollé un entorno de pruebas donde utilizo ForjaX en escenarios controlados de pentesting. En el video adjunto muestro una simulación en laboratorio donde, a través de un ejecutable generado, se obtiene acceso remoto a una máquina Windows 11.

El objetivo de esta demostración NO es el uso malicioso, sino evidenciar:

→ Qué tan fácil puede ser ejecutar archivos sin verificar su origen

→ Cómo operan ciertas técnicas reales utilizadas en ataques

→ La importancia de la concienciación en seguridad ofensiva y defensiva

ForjaX incluye una sección de pruebas (reverse shells) pensada exclusivamente para entornos de laboratorio y aprendizaje en ciberseguridad.

>⚠️ Este proyecto está orientado a uso ético: pentesting, investigación y educación

---
## ✨ Características

- 🔥 Empaqueta scripts a ejecutables `.exe`, `.jar`, `.phar` o `.bat`
- 🔒 Ofusca el código fuente con técnicas específicas por lenguaje
- 🌐 Soporta **8 lenguajes** de programación
- 🤖 Detecta automáticamente las herramientas instaladas
- 🪟 Genera wrappers `.bat` como fallback si la herramienta no está disponible
- 🎨 Interfaz con colores ANSI y menús interactivos
- 🐧 Compatible con Windows, Linux y Mac

---

## 🌐 Lenguajes soportados

| # | Lenguaje | Extensión | Empaquetado | Ofuscación |
|---|----------|-----------|-------------|------------|
| 1 | Bash | `.sh` | SHC / wrapper .bat | eval + Base64 |
| 2 | C | `.c` | GCC / MinGW | Array de bytes embebido |
| 3 | Go | `.go` | go build | Base64 + go run en runtime |
| 4 | Java | `.java` | javac + JAR + Launch4j | Base64 + ScriptEngine |
| 5 | JavaScript | `.js` | pkg / nexe | Base64 + eval |
| 6 | PHP | `.php` | PHAR / wrapper .bat | eval + base64_decode |
| 7 | PowerShell | `.ps1` | ps2exe / wrapper .bat | IEX + UTF-16 Base64 |
| 8 | Python | `.py` | PyInstaller | zlib + Base64 + exec |

---

## 📁 Estructura del proyecto

```
forjax/
├── forjax.py                 # Software principal
├── requirements.txt          # Dependencias del proyecto
├── install.bat               # Instalador automático (Windows)
├── install.sh                # Instalador automático (Linux / macOS)
│
├── reverse_shells/           # Colección de reverse shells por lenguaje
│   ├── bash/
│   │   └── clasic1.sh
│   │
│   ├── c/
│   │   └── clasic1.c
│   │
│   ├── go/
│   │   └── clasic1.go
│   │
│   ├── java/
│   │   └── clasic1.java
│   │
│   ├── javascript/
│   │   └── clasic1.js
│   │
│   ├── php/
│   │   └── clasic1.php
│   │
│   ├── powershell/
│   │   └── clasic1.ps1
│   │
│   └── python/
│   │   └── clasic1.py
│   │
└── README.md
```

> 📂 La carpeta `ReverShell/` contiene scripts simples listos para usar y probar que ForjaX empaqueta y ofusca correctamente cada lenguaje.

---

## 🚀 Instalación

### Requisito mínimo
- Python 3.7 o superior → https://www.python.org/downloads/

### Opción A — Instalación automática (recomendada)

Clona el repositorio:
```bash
git clone https://github.com/ElHackerDaniel/forjax.git
cd forjax
```

**En Windows:**
```
install.bat
```

**En Linux / Mac:**
```bash
chmod +x install.sh
./install.sh
```

El instalador detecta tu sistema, verifica qué herramientas tienes y descarga todo automáticamente.

### Opción B — Instalación manual por lenguaje

Si solo quieres usar ForjaX con uno o varios lenguajes específicos, consulta el archivo `requirements.txt` y sigue las instrucciones del lenguaje que necesites. No es necesario instalar todo.

---

## ▶️ Uso

```bash
python forjax.py        # Linux / Mac
python forjax.py        # Windows
```

Al ejecutarlo verás el menú principal:

```
  Selecciona una opcion:

  [1] Empaquetar script a ejecutable
  [2] Ofuscar script
  [3] Ofuscar y empaquetar a ejecutable
  [4] Salir

  Lenguajes: Bash · C · Go · Java · JavaScript · PHP · PowerShell · Python
```

### Empaquetar un script
1. Selecciona `[1]`
2. Elige el lenguaje
3. Ingresa la ruta del archivo
4. Elige la carpeta de salida
5. Asigna un nombre al ejecutable
6. ForjaX genera el ejecutable automáticamente

### Ofuscar un script
1. Selecciona `[2]`
2. Elige el lenguaje
3. Ingresa la ruta del archivo
4. ForjaX genera un archivo `_ofu` con el código protegido

### Ofuscar y empaquetar
1. Selecciona `[3]`
2. ForjaX ofusca el código y luego lo compila a ejecutable en un solo paso

---

## 🧪 Carpeta de pruebas

La carpeta `ReverShell/` incluye un script simple por cada lenguaje soportado. Puedes usarlos para verificar que ForjaX funciona correctamente en tu sistema antes de usar tus propios archivos.

**Ejemplo de uso con la carpeta de ReverShell:**
```bash
# Empaquetar el script de ReverShell de Python
python forjax.py
# → Opcion 1 → Python → ReverShell/Python/Clasic1.py
```

---

## 📦 Archivos generados

| Archivo | Cuándo se genera |
|---------|-----------------|
| `.exe` | Python, C, Go, Bash (con SHC), PowerShell (con ps2exe) |
| `.jar` | Java (cuando Launch4j no está disponible) |
| `.phar` | PHP (cuando PHP está disponible) |
| `.bat` | Fallback automático cuando la herramienta principal no está instalada |

---

## 🔒 Métodos de ofuscación

| Lenguaje | Técnica |
|----------|---------|
| Python | zlib compresión + Base64 + `exec()` |
| Bash | Base64 + `eval` |
| C | Array de bytes del fuente embebido |
| Go | Base64 + ejecución en runtime |
| Java | Base64 + `ScriptEngine` |
| JavaScript | Base64 + `eval` |
| PHP | `base64_decode` + `eval` |
| PowerShell | UTF-16 Base64 + `Invoke-Expression` |

---

## ⚙️ Herramientas externas por lenguaje

| Lenguaje | Herramienta | Instalación |
|----------|-------------|-------------|
| Python | PyInstaller | `pip install pyinstaller` |
| JavaScript | pkg | `npm install -g pkg` |
| PowerShell | ps2exe | `Install-Module ps2exe` |
| Java | JDK + Launch4j | adoptium.net / launch4j.sourceforge.net |
| C | GCC / MinGW | winlibs.com |
| Go | Go compiler | go.dev/dl |
| Bash | SHC / Git Bash | `apt install shc` |
| PHP | PHP + phar | php.net |

---

## 👤 Autor

**XorSvn**

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.

---

<div align="center">
Hecho con 🔥 por <b>XorSvn</b>
</div>
