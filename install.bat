@echo off
chcp 65001 >nul
cls

echo.
echo   ███████╗ ██████╗ ██████╗      ██╗ █████╗ ██╗  ██╗
echo   ██╔════╝██╔═══██╗██╔══██╗     ██║██╔══██╗╚██╗██╔╝
echo   █████╗  ██║   ██║██████╔╝     ██║███████║ ╚███╔╝
echo   ██╔══╝  ██║   ██║██╔══██╗██   ██║██╔══██║ ██╔██╗
echo   ██║     ╚██████╔╝██║  ██║╚█████╔╝██║  ██║██╔╝╚██╗
echo   ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
echo.
echo   Instalador de ForjaX v1.0.0 - by XorSvn
echo   -------------------------------------------------------
echo.

:: ── Verificar Python ────────────────────────────────────────────────────────
echo   [1/7] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [X] Python no encontrado.
    echo       Descargalo en: https://www.python.org/downloads/
    echo       Asegurate de marcar "Add Python to PATH" al instalar.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo   [OK] %PYVER% encontrado.

:: ── Instalar PyInstaller ─────────────────────────────────────────────────────
echo.
echo   [2/7] Instalando PyInstaller (Python → .exe)...
pip install pyinstaller --quiet --disable-pip-version-check
if %errorlevel% equ 0 (
    echo   [OK] PyInstaller instalado.
) else (
    echo   [!] No se pudo instalar PyInstaller. Intenta: pip install pyinstaller
)

:: ── Verificar Node.js / npm ──────────────────────────────────────────────────
echo.
echo   [3/7] Verificando Node.js (JavaScript → .exe)...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [!] Node.js no encontrado.
    echo       Para empaquetar JavaScript instala Node.js: https://nodejs.org
) else (
    for /f "tokens=*" %%i in ('node --version 2^>^&1') do set NODEVER=%%i
    echo   [OK] Node.js %NODEVER% encontrado.
    echo        Instalando pkg (JavaScript → .exe)...
    call npm install -g pkg --quiet >nul 2>&1
    if %errorlevel% equ 0 (
        echo   [OK] pkg instalado.
    ) else (
        echo   [!] No se pudo instalar pkg. Intenta: npm install -g pkg
    )
)

:: ── Verificar Go ─────────────────────────────────────────────────────────────
echo.
echo   [4/7] Verificando Go...
go version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [!] Go no encontrado.
    echo       Para compilar .go instala Go: https://go.dev/dl/
) else (
    for /f "tokens=*" %%i in ('go version 2^>^&1') do set GOVER=%%i
    echo   [OK] %GOVER% encontrado.
)

:: ── Verificar Java (JDK) ─────────────────────────────────────────────────────
echo.
echo   [5/7] Verificando Java JDK...
javac -version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [!] JDK no encontrado.
    echo       Para compilar .java instala el JDK: https://adoptium.net
) else (
    for /f "tokens=*" %%i in ('javac -version 2^>^&1') do set JAVAVER=%%i
    echo   [OK] %JAVAVER% encontrado.
)

:: ── Verificar GCC / MinGW ────────────────────────────────────────────────────
echo.
echo   [6/7] Verificando GCC (C → .exe)...
gcc --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [!] GCC/MinGW no encontrado.
    echo       Para compilar .c instala MinGW-w64: https://winlibs.com
) else (
    for /f "tokens=1-3" %%a in ('gcc --version 2^>^&1') do (
        echo   [OK] GCC encontrado.
        goto :gcc_done
    )
    :gcc_done
)

:: ── Verificar PHP ────────────────────────────────────────────────────────────
echo.
echo   [7/7] Verificando PHP...
php --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   [!] PHP no encontrado.
    echo       Para empaquetar .php instala PHP: https://www.php.net/downloads
) else (
    for /f "tokens=1,2" %%a in ('php --version 2^>^&1') do (
        echo   [OK] PHP %%b encontrado.
        goto :php_done
    )
    :php_done
)

:: ── PowerShell ps2exe ────────────────────────────────────────────────────────
echo.
echo   Instalando ps2exe (PowerShell → .exe)...
powershell -NoProfile -Command "Install-Module ps2exe -Scope CurrentUser -Force -ErrorAction SilentlyContinue" >nul 2>&1
if %errorlevel% equ 0 (
    echo   [OK] ps2exe instalado.
) else (
    echo   [!] ps2exe no se pudo instalar automaticamente.
    echo       Ejecuta en PowerShell: Install-Module ps2exe
)

:: ── Resumen final ────────────────────────────────────────────────────────────
echo.
echo   -------------------------------------------------------
echo   [OK] Instalacion completada.
echo        Ejecuta ForjaX con:  python forjax.py
echo   -------------------------------------------------------
echo.
pause
