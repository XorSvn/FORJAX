#!/usr/bin/env bash
# ══════════════════════════════════════════════════
#  ForjaX v1.0.0 - Instalador para Linux / Mac
#  by XorSvn
# ══════════════════════════════════════════════════
#  Uso:
#    chmod +x install.sh
#    ./install.sh
# ══════════════════════════════════════════════════

# ─── Colores ─────────────────────────────────────
R="\033[0m"
O="\033[38;5;208m"
GR="\033[38;5;83m"
RE="\033[38;5;203m"
GY="\033[38;5;245m"
WH="\033[97m"
BD="\033[1m"

OK="${GR}[OK]${R}"
WARN="${O}[!] ${R}"
ERR="${RE}[X] ${R}"

clear
echo -e "${O}${BD}"
echo "  ███████╗ ██████╗ ██████╗      ██╗ █████╗ ██╗  ██╗"
echo "  ██╔════╝██╔═══██╗██╔══██╗     ██║██╔══██╗╚██╗██╔╝"
echo "  █████╗  ██║   ██║██████╔╝     ██║███████║ ╚███╔╝ "
echo "  ██╔══╝  ██║   ██║██╔══██╗██   ██║██╔══██║ ██╔██╗ "
echo "  ██║     ╚██████╔╝██║  ██║╚█████╔╝██║  ██║██╔╝╚██╗"
echo "  ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝"
echo -e "${R}"
echo -e "  Instalador de ForjaX v1.0.0 - by XorSvn"
echo -e "${GY}  -------------------------------------------------------${R}"
echo ""

# ─── Detectar gestor de paquetes ─────────────────
if command -v apt &>/dev/null; then
    PKG_MANAGER="apt"
    PKG_INSTALL="sudo apt install -y"
elif command -v dnf &>/dev/null; then
    PKG_MANAGER="dnf"
    PKG_INSTALL="sudo dnf install -y"
elif command -v pacman &>/dev/null; then
    PKG_MANAGER="pacman"
    PKG_INSTALL="sudo pacman -S --noconfirm"
elif command -v brew &>/dev/null; then
    PKG_MANAGER="brew"
    PKG_INSTALL="brew install"
else
    PKG_MANAGER="unknown"
    PKG_INSTALL=""
fi

echo -e "  ${GY}Sistema detectado: $(uname -s) | Gestor: ${PKG_MANAGER}${R}"
echo ""

# ─── 1. Python ───────────────────────────────────
echo -e "  ${WH}[1/8]${R} Verificando Python..."
if command -v python3 &>/dev/null; then
    PYVER=$(python3 --version 2>&1)
    echo -e "  $OK $PYVER encontrado."
else
    echo -e "  $ERR Python3 no encontrado."
    if [ -n "$PKG_INSTALL" ]; then
        echo -e "  ${GY}  Instalando Python3...${R}"
        $PKG_INSTALL python3 python3-pip
    else
        echo -e "  ${GY}  Instala Python3 desde: https://www.python.org/downloads/${R}"
    fi
fi

# ─── 2. pip ──────────────────────────────────────
echo ""
echo -e "  ${WH}[2/8]${R} Verificando pip..."
if command -v pip3 &>/dev/null || command -v pip &>/dev/null; then
    echo -e "  $OK pip encontrado."
else
    echo -e "  $WARN pip no encontrado. Instalando..."
    if [ -n "$PKG_INSTALL" ]; then
        $PKG_INSTALL python3-pip
    fi
fi

# ─── 3. PyInstaller ──────────────────────────────
echo ""
echo -e "  ${WH}[3/8]${R} Instalando PyInstaller (Python → ejecutable)..."
if command -v pip3 &>/dev/null; then
    pip3 install pyinstaller --quiet --disable-pip-version-check
elif command -v pip &>/dev/null; then
    pip install pyinstaller --quiet --disable-pip-version-check
fi
if command -v pyinstaller &>/dev/null; then
    echo -e "  $OK PyInstaller instalado."
else
    echo -e "  $WARN PyInstaller no se pudo instalar. Intenta: pip3 install pyinstaller"
fi

# ─── 4. Node.js / pkg ────────────────────────────
echo ""
echo -e "  ${WH}[4/8]${R} Verificando Node.js (JavaScript → ejecutable)..."
if command -v node &>/dev/null; then
    NODEVER=$(node --version 2>&1)
    echo -e "  $OK Node.js $NODEVER encontrado."
    echo -e "       Instalando pkg..."
    npm install -g pkg &>/dev/null
    if command -v pkg &>/dev/null; then
        echo -e "  $OK pkg instalado."
    else
        echo -e "  $WARN pkg no se pudo instalar. Intenta: npm install -g pkg"
    fi
else
    echo -e "  $WARN Node.js no encontrado."
    if [ "$PKG_MANAGER" = "apt" ]; then
        echo -e "  ${GY}  Instala con: sudo apt install nodejs npm${R}"
    elif [ "$PKG_MANAGER" = "brew" ]; then
        echo -e "  ${GY}  Instala con: brew install node${R}"
    else
        echo -e "  ${GY}  Descarga desde: https://nodejs.org${R}"
    fi
fi

# ─── 5. Go ───────────────────────────────────────
echo ""
echo -e "  ${WH}[5/8]${R} Verificando Go..."
if command -v go &>/dev/null; then
    GOVER=$(go version 2>&1)
    echo -e "  $OK $GOVER encontrado."
else
    echo -e "  $WARN Go no encontrado."
    if [ "$PKG_MANAGER" = "apt" ]; then
        echo -e "  ${GY}  Instala con: sudo apt install golang-go${R}"
    elif [ "$PKG_MANAGER" = "brew" ]; then
        echo -e "  ${GY}  Instala con: brew install go${R}"
    else
        echo -e "  ${GY}  Descarga desde: https://go.dev/dl/${R}"
    fi
fi

# ─── 6. Java JDK ─────────────────────────────────
echo ""
echo -e "  ${WH}[6/8]${R} Verificando Java JDK..."
if command -v javac &>/dev/null; then
    JAVAVER=$(javac -version 2>&1)
    echo -e "  $OK $JAVAVER encontrado."
else
    echo -e "  $WARN Java JDK no encontrado."
    if [ "$PKG_MANAGER" = "apt" ]; then
        echo -e "  ${GY}  Instala con: sudo apt install default-jdk${R}"
    elif [ "$PKG_MANAGER" = "brew" ]; then
        echo -e "  ${GY}  Instala con: brew install openjdk${R}"
    else
        echo -e "  ${GY}  Descarga desde: https://adoptium.net${R}"
    fi
fi

# ─── 7. GCC ──────────────────────────────────────
echo ""
echo -e "  ${WH}[7/8]${R} Verificando GCC (C → ejecutable)..."
if command -v gcc &>/dev/null; then
    GCCVER=$(gcc --version 2>&1 | head -1)
    echo -e "  $OK $GCCVER encontrado."
else
    echo -e "  $WARN GCC no encontrado."
    if [ "$PKG_MANAGER" = "apt" ]; then
        echo -e "  ${GY}  Instalando GCC...${R}"
        sudo apt install -y gcc build-essential
    elif [ "$PKG_MANAGER" = "brew" ]; then
        echo -e "  ${GY}  Instala con: brew install gcc${R}"
    else
        echo -e "  ${GY}  Instala el compilador GCC para tu distro.${R}"
    fi
fi

# ─── 8. PHP ──────────────────────────────────────
echo ""
echo -e "  ${WH}[8/8]${R} Verificando PHP..."
if command -v php &>/dev/null; then
    PHPVER=$(php --version 2>&1 | head -1)
    echo -e "  $OK $PHPVER encontrado."
else
    echo -e "  $WARN PHP no encontrado."
    if [ "$PKG_MANAGER" = "apt" ]; then
        echo -e "  ${GY}  Instala con: sudo apt install php-cli${R}"
    elif [ "$PKG_MANAGER" = "brew" ]; then
        echo -e "  ${GY}  Instala con: brew install php${R}"
    else
        echo -e "  ${GY}  Descarga desde: https://www.php.net/downloads${R}"
    fi
fi

# ─── SHC (Bash compiler) ─────────────────────────
echo ""
echo -e "  ${WH}[+] ${R} Verificando SHC (Bash → ejecutable)..."
if command -v shc &>/dev/null; then
    echo -e "  $OK shc encontrado."
else
    echo -e "  $WARN shc no encontrado."
    if [ "$PKG_MANAGER" = "apt" ]; then
        echo -e "  ${GY}  Instala con: sudo apt install shc${R}"
    elif [ "$PKG_MANAGER" = "brew" ]; then
        echo -e "  ${GY}  Instala con: brew install shc${R}"
    fi
fi

# ─── Resumen ─────────────────────────────────────
echo ""
echo -e "${GY}  -------------------------------------------------------${R}"
echo -e "  $OK Instalacion completada."
echo -e "       Ejecuta ForjaX con: ${O}python3 forjax.py${R}"
echo -e "${GY}  -------------------------------------------------------${R}"
echo ""
