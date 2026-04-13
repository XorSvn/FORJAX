import subprocess
import sys
import os
import base64
import zlib
import shutil
import tempfile
from pathlib import Path

# ─── Colores ANSI ────────────────────────────────────────────────────────────
R  = "\033[0m"
O  = "\033[38;5;208m"
O2 = "\033[38;5;214m"
GR = "\033[38;5;83m"
RE = "\033[38;5;203m"
GY = "\033[38;5;245m"
CY = "\033[38;5;117m"
WH = "\033[97m"
BD = "\033[1m"
MG = "\033[38;5;177m"

VERSION  = "2.0.0"
AUTOR    = "XorSvn"

# ─── Lenguajes soportados ────────────────────────────────────────────────────
LENGUAJES = {
    "1": {"nombre": "Bash (.sh)",          "ext": ".sh",   "metodo_exe": "shc",          "metodo_ofu": "bash_b64"},
    "2": {"nombre": "C (.c)",              "ext": ".c",    "metodo_exe": "gcc",          "metodo_ofu": "c_encode"},
    "3": {"nombre": "Go (.go)",            "ext": ".go",   "metodo_exe": "go_build",     "metodo_ofu": "go_b64"},
    "4": {"nombre": "Java (.java)",        "ext": ".java", "metodo_exe": "jar_launch4j", "metodo_ofu": "java_b64"},
    "5": {"nombre": "JavaScript (.js)",    "ext": ".js",   "metodo_exe": "pkg_nexe",     "metodo_ofu": "js_b64"},
    "6": {"nombre": "PHP (.php)",          "ext": ".php",  "metodo_exe": "micro_php",    "metodo_ofu": "php_b64"},
    "7": {"nombre": "PowerShell (.ps1)",   "ext": ".ps1",  "metodo_exe": "ps2exe",       "metodo_ofu": "ps_b64"},
    "8": {"nombre": "Python (.py)",        "ext": ".py",   "metodo_exe": "pyinstaller",  "metodo_ofu": "zlib_b64"},
}

# ─── Banner ───────────────────────────────────────────────────────────────────
BANNER = f"""{O}{BD}
  ███████╗ ██████╗ ██████╗      ██╗ █████╗ ██╗  ██╗
  ██╔════╝██╔═══██╗██╔══██╗     ██║██╔══██╗╚██╗██╔╝
  █████╗  ██║   ██║██████╔╝     ██║███████║ ╚███╔╝
  ██╔══╝  ██║   ██║██╔══██╗██   ██║██╔══██║ ██╔██╗
  ██║     ╚██████╔╝██║  ██║╚█████╔╝██║  ██║██╔╝╚██╗
  ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝{R}
{GY}  ┌───────────────────────────────────────────────┐{R}
{GY}  │{R}   {O2}Empaquetador y ofuscador multi-lenguaje 🔥{R}  {GY}│{R}
{GY}  │{R}              {MG}v{VERSION}{R}  {GY}·{R}  {CY}by {AUTOR}{R}             {GY}│{R}
{GY}  └───────────────────────────────────────────────┘{R}"""

# ─── Helpers ─────────────────────────────────────────────────────────────────
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input(f"\n{GY}  Presiona Enter para continuar...{R}")

def cmd_existe(cmd):
    return shutil.which(cmd) is not None

def pedir_ruta(prompt, debe_existir=True):
    while True:
        ruta = input(f"  {CY}{prompt}{R} ").strip().strip('"').strip("'")
        if not ruta:
            print(f"  {RE}Debes ingresar una ruta.{R}")
            continue
        if debe_existir and not Path(ruta).exists():
            print(f"  {RE}Archivo no encontrado: {ruta}{R}")
            continue
        return ruta

def pedir_directorio(prompt):
    default = str(Path.home() / "ForjaX_output")
    val = input(f"  {CY}{prompt}{R} [{GY}{default}{R}]: ").strip()
    return val if val else default

def pedir_nombre(prompt, default="salida"):
    val = input(f"  {CY}{prompt}{R} [{GY}{default}{R}]: ").strip()
    return val if val else default

def menu_lenguaje():
    print(f"\n{O}  Selecciona el lenguaje:{R}\n")
    for k, v in LENGUAJES.items():
        print(f"  {WH}[{k}]{R} {v['nombre']}")
    print(f"  {WH}[0]{R} {GY}Volver{R}")
    while True:
        op = input(f"\n  {O}>{R} ").strip()
        if op == "0":
            return None
        if op in LENGUAJES:
            return LENGUAJES[op]
        print(f"  {RE}Opcion invalida.{R}")

# ════════════════════════════════════════════════════════════════════════════
#  OFUSCADORES
# ════════════════════════════════════════════════════════════════════════════

def ofu_bash(codigo):
    encoded = base64.b64encode(codigo.encode("utf-8")).decode("utf-8")
    return (
        f'#!/usr/bin/env bash\n'
        f'# Ofuscado por ForjaX v{VERSION} - {AUTOR}\n'
        f'eval "$(echo \'{encoded}\' | base64 --decode)"\n'
    )

def ofu_c(codigo):
    nums = ",".join(str(b) for b in codigo.encode("utf-8"))
    return (
        f'/* Ofuscado por ForjaX v{VERSION} - {AUTOR} */\n'
        '#include <stdio.h>\n#include <stdlib.h>\n\n'
        f'static const unsigned char _src[] = {{{nums},0}};\n\n'
        'int main(void) {\n'
        '    const char *t = getenv("TEMP"); if (!t) t = "/tmp";\n'
        '    char tmp[512], cmd[600];\n'
        '    snprintf(tmp, sizeof(tmp), "%s/_fx_src.c", t);\n'
        '    FILE *f = fopen(tmp,"wb");\n'
        '    if (!f) return 1;\n'
        '    fwrite(_src,1,sizeof(_src)-1,f); fclose(f);\n'
        '    snprintf(cmd,sizeof(cmd),"gcc %s -o %s/_fx_out.exe",tmp,t);\n'
        '    return system(cmd);\n'
        '}\n'
    )

def ofu_go(codigo):
    encoded = base64.b64encode(codigo.encode("utf-8")).decode("utf-8")
    lineas  = [encoded[i:i+76] for i in range(0, len(encoded), 76)]
    payload = '"\n\t\t"'.join(lineas)
    return (
        f'// Ofuscado por ForjaX v{VERSION} - {AUTOR}\n'
        'package main\n\nimport (\n\t"encoding/base64"\n\t"fmt"\n\t"os"\n'
        '\t"os/exec"\n\t"path/filepath"\n)\n\n'
        'func main() {\n'
        f'\tenc := "{payload}"\n'
        '\tsrc, err := base64.StdEncoding.DecodeString(enc)\n'
        '\tif err != nil { fmt.Fprintln(os.Stderr, err); os.Exit(1) }\n'
        '\ttmp := filepath.Join(os.TempDir(), "_fx_tmp.go")\n'
        '\tif err := os.WriteFile(tmp, src, 0600); err != nil {\n'
        '\t\tfmt.Fprintln(os.Stderr, err); os.Exit(1)\n\t}\n'
        '\tcmd := exec.Command("go", "run", tmp)\n'
        '\tcmd.Stdout = os.Stdout; cmd.Stderr = os.Stderr; cmd.Stdin = os.Stdin\n'
        '\tif err := cmd.Run(); err != nil { os.Exit(1) }\n'
        '}\n'
    )

def ofu_java(codigo):
    encoded = base64.b64encode(codigo.encode("utf-8")).decode("utf-8")
    lineas  = [encoded[i:i+76] for i in range(0, len(encoded), 76)]
    payload = '"\n            + "'.join(lineas)
    return (
        f'// Ofuscado por ForjaX v{VERSION} - {AUTOR}\n'
        'import java.util.Base64;\nimport javax.script.*;\n\n'
        'public class Ofuscado {\n'
        '    public static void main(String[] args) throws Exception {\n'
        f'        String enc = "{payload}";\n'
        '        String src = new String(Base64.getDecoder().decode(enc));\n'
        '        ScriptEngine e = new ScriptEngineManager().getEngineByName("groovy");\n'
        '        if (e == null) { System.err.println("Requiere Groovy en classpath"); System.exit(1); }\n'
        '        e.eval(src);\n'
        '    }\n}\n'
    )

def ofu_js(codigo):
    encoded = base64.b64encode(codigo.encode("utf-8")).decode("utf-8")
    lineas  = [encoded[i:i+76] for i in range(0, len(encoded), 76)]
    payload = '"\n  +"'.join(lineas)
    return (
        f'// Ofuscado por ForjaX v{VERSION} - {AUTOR}\n'
        f'const _e = "{payload}";\n'
        'const _d = Buffer.from(_e, "base64").toString("utf-8");\n'
        'eval(_d);\n'
    )

def ofu_php(codigo):
    encoded = base64.b64encode(codigo.encode("utf-8")).decode("utf-8")
    lineas  = [encoded[i:i+76] for i in range(0, len(encoded), 76)]
    payload = '"\n."'.join(lineas)
    return (
        f'<?php /* Ofuscado por ForjaX v{VERSION} - {AUTOR} */\n'
        f'eval(base64_decode("{payload}")); ?>\n'
    )

def ofu_powershell(codigo):
    encoded = base64.b64encode(codigo.encode("utf-16-le")).decode("utf-8")
    lineas  = [encoded[i:i+76] for i in range(0, len(encoded), 76)]
    payload = '`\n+"'.join(lineas)
    return (
        f'# Ofuscado por ForjaX v{VERSION} - {AUTOR}\n'
        f'$e="{payload}"\n'
        '$b=[System.Convert]::FromBase64String($e)\n'
        '$t=[System.Text.Encoding]::Unicode.GetString($b)\n'
        'Invoke-Expression $t\n'
    )

def ofu_python(codigo):
    comp    = zlib.compress(codigo.encode("utf-8"), level=9)
    encoded = base64.b64encode(comp).decode("utf-8")
    lineas  = [encoded[i:i+76] for i in range(0, len(encoded), 76)]
    payload = "\n    ".join(f'"{l}"' for l in lineas)
    return (
        f'# Ofuscado por ForjaX v{VERSION} - {AUTOR}\n'
        f'import zlib,base64\n'
        f'exec(zlib.decompress(base64.b64decode(\n    {payload}\n)).decode("utf-8"))\n'
    )

OFUSCADORES = {
    "bash_b64":  ofu_bash,
    "c_encode":  ofu_c,
    "go_b64":    ofu_go,
    "java_b64":  ofu_java,
    "js_b64":    ofu_js,
    "php_b64":   ofu_php,
    "ps_b64":    ofu_powershell,
    "zlib_b64":  ofu_python,
}

# ════════════════════════════════════════════════════════════════════════════
#  COMPILADORES / EMPAQUETADORES
# ════════════════════════════════════════════════════════════════════════════

def compilar_bash(src, outdir, name):
    if cmd_existe("shc"):
        exe = Path(outdir) / f"{name}.exe"
        return subprocess.run(["shc", "-f", src, "-o", str(exe)]).returncode == 0
    bat = Path(outdir) / f"{name}.bat"
    bat.write_text(f'@echo off\nbash "%~dp0{Path(src).name}" %*\n', encoding="utf-8")
    shutil.copy(src, Path(outdir) / Path(src).name)
    print(f"  {O2}SHC no disponible. Wrapper .bat generado (requiere Git Bash / WSL):{R}")
    print(f"     {bat}")
    return True

def compilar_c(src, outdir, name):
    exe = Path(outdir) / f"{name}.exe"
    for comp in ["x86_64-w64-mingw32-gcc", "gcc", "cc"]:
        if cmd_existe(comp):
            print(f"  {GY}Compilador: {comp}{R}")
            return subprocess.run([comp, src, "-o", str(exe), "-O2"]).returncode == 0
    print(f"  {RE}GCC/MinGW no encontrado.{R}")
    print(f"  {GY}Windows: https://winlibs.com  |  Linux: sudo apt install gcc mingw-w64{R}")
    return False

def compilar_go(src, outdir, name):
    if not cmd_existe("go"):
        print(f"  {RE}Go no encontrado. Descarga: https://go.dev/dl/{R}")
        return False
    exe = Path(outdir) / f"{name}.exe"
    env = os.environ.copy()
    env["GOOS"]   = "windows"
    env["GOARCH"] = "amd64"
    r = subprocess.run(["go", "build", "-o", str(exe), src], env=env)
    return r.returncode == 0

def compilar_java(src, outdir, name):
    if not cmd_existe("javac"):
        print(f"  {RE}javac no encontrado. Instala el JDK: https://adoptium.net{R}")
        return False
    build = Path(outdir) / "_java_build"
    build.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, build / Path(src).name)
    r = subprocess.run(["javac", str(build / Path(src).name)], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  {RE}Error Java:{R}\n{r.stderr}")
        return False
    contenido  = Path(src).read_text(encoding="utf-8", errors="replace")
    clase_main = next(
        (l.strip().split("public class")[1].strip().split()[0]
         for l in contenido.splitlines() if "public class" in l),
        Path(src).stem
    )
    jar = Path(outdir) / f"{name}.jar"
    mf  = build / "MANIFEST.MF"
    mf.write_text(f"Main-Class: {clase_main}\n", encoding="utf-8")
    r2 = subprocess.run(["jar", "cfm", str(jar), str(mf), "-C", str(build), "."],
                        capture_output=True, text=True)
    if r2.returncode != 0:
        print(f"  {RE}Error JAR:{R}\n{r2.stderr}")
        return False
    print(f"  {GR}JAR:{R} {jar}")
    # Intentar Launch4j
    l4j = next((p for p in [
        r"C:\Program Files (x86)\Launch4j\launch4jc.exe",
        r"C:\Program Files\Launch4j\launch4jc.exe",
        "launch4jc"] if (Path(p).exists() if "\\" in p else cmd_existe(p))), None)
    if l4j:
        exe = Path(outdir) / f"{name}.exe"
        xml = build / "l4j.xml"
        xml.write_text(
            f'<launch4jConfig><dontWrapJar>false</dontWrapJar>'
            f'<headerType>console</headerType><jar>{jar}</jar>'
            f'<outfile>{exe}</outfile>'
            f'<jre><minVersion>1.8.0</minVersion></jre></launch4jConfig>',
            encoding="utf-8")
        if subprocess.run([l4j, str(xml)], capture_output=True, text=True).returncode == 0:
            print(f"  {GR}EXE (Launch4j):{R} {exe}")
            return True
    bat = Path(outdir) / f"{name}.bat"
    bat.write_text(f'@echo off\njava -jar "%~dp0{name}.jar" %*\n', encoding="utf-8")
    print(f"  {O2}Launch4j no encontrado. Wrapper .bat:{R} {bat}")
    print(f"  {GY}Para .exe real: https://launch4j.sourceforge.net{R}")
    return True

def compilar_js(src, outdir, name):
    exe = Path(outdir) / f"{name}.exe"
    # Intentar con pkg (Node.js)
    if cmd_existe("pkg"):
        r = subprocess.run(["pkg", src, "--output", str(exe), "--target", "node18-win-x64"],
                           capture_output=True, text=True)
        if r.returncode == 0:
            return True
        print(f"  {O2}pkg falló, intentando con nexe...{R}")
    # Intentar con nexe
    if cmd_existe("nexe"):
        r = subprocess.run(["nexe", src, "-o", str(exe)], capture_output=True, text=True)
        if r.returncode == 0:
            return True
    # Intentar instalar pkg automaticamente
    if cmd_existe("npm"):
        print(f"  {O2}Instalando pkg via npm...{R}")
        inst = subprocess.run(["npm", "install", "-g", "pkg"],
                              capture_output=True, text=True)
        if inst.returncode == 0:
            r = subprocess.run(["pkg", src, "--output", str(exe), "--target", "node18-win-x64"],
                               capture_output=True, text=True)
            if r.returncode == 0:
                return True
    # Fallback: wrapper .bat
    bat = Path(outdir) / f"{name}.bat"
    bat.write_text(f'@echo off\nnode "%~dp0{Path(src).name}" %*\n', encoding="utf-8")
    shutil.copy(src, Path(outdir) / Path(src).name)
    print(f"  {O2}pkg/nexe no disponibles. Wrapper .bat generado (requiere Node.js):{R}")
    print(f"     {bat}")
    print(f"  {GY}Para .exe real: npm install -g pkg{R}")
    return True

def compilar_php(src, outdir, name):
    if not cmd_existe("php"):
        bat = Path(outdir) / f"{name}.bat"
        bat.write_text(f'@echo off\nphp "%~dp0{Path(src).name}" %*\n', encoding="utf-8")
        shutil.copy(src, Path(outdir) / Path(src).name)
        print(f"  {O2}PHP no en PATH. Wrapper .bat generado (requiere PHP):{R} {bat}")
        return True
    phar_path = Path(outdir) / f"{name}.phar"
    src_fwd   = str(Path(src)).replace("\\", "/")
    phar_fwd  = str(phar_path).replace("\\", "/")
    builder   = (
        f"<?php\n$p=new Phar('{phar_fwd}',0,'{name}.phar');\n"
        f"$p->startBuffering();\n$p->addFile('{src_fwd}','index.php');\n"
        f"$p->setStub($p->createDefaultStub('index.php'));\n"
        f"$p->stopBuffering();\necho 'OK';?>"
    )
    tmp = tempfile.NamedTemporaryFile(suffix=".php", delete=False, mode="w", encoding="utf-8")
    tmp.write(builder); tmp.close()
    r = subprocess.run(["php", tmp.name], capture_output=True, text=True)
    os.unlink(tmp.name)
    if r.returncode == 0 and phar_path.exists():
        bat = Path(outdir) / f"{name}.bat"
        bat.write_text(f'@echo off\nphp "%~dp0{name}.phar" %*\n', encoding="utf-8")
        print(f"  {GR}PHAR:{R} {phar_path}")
        print(f"  {GR}Wrapper:{R} {bat}  {GY}(ejecuta el .bat){R}")
        return True
    print(f"  {RE}Error PHAR. Verifica phar.readonly=Off en php.ini{R}")
    return False

def compilar_ps1(src, outdir, name):
    exe    = Path(outdir) / f"{name}.exe"
    ps_cmd = (f"Import-Module ps2exe -ErrorAction Stop; "
              f"Invoke-ps2exe -InputFile '{src}' -OutputFile '{exe}'")
    if cmd_existe("powershell"):
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd],
                           capture_output=True, text=True)
        if r.returncode == 0:
            return True
        print(f"  {O2}ps2exe no instalado. Intentando instalar...{R}")
        inst = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Install-Module ps2exe -Scope CurrentUser -Force"],
            capture_output=True, text=True)
        if inst.returncode == 0:
            r2 = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd],
                                 capture_output=True, text=True)
            if r2.returncode == 0:
                return True
    bat = Path(outdir) / f"{name}.bat"
    bat.write_text(
        f'@echo off\npowershell -ExecutionPolicy Bypass -File "%~dp0{Path(src).name}" %*\n',
        encoding="utf-8")
    shutil.copy(src, Path(outdir) / Path(src).name)
    print(f"  {O2}ps2exe no disponible. Wrapper .bat:{R} {bat}")
    print(f"  {GY}Para .exe real: Install-Module ps2exe en PowerShell{R}")
    return True

def compilar_python(src, outdir, name):
    if not cmd_existe("pyinstaller"):
        print(f"  {RE}PyInstaller no encontrado: pip install pyinstaller{R}")
        return False
    cmd = [sys.executable, "-m", "PyInstaller", src,
           "--name", name, "--distpath", outdir,
           "--workpath", str(Path(outdir)/"_build"),
           "--specpath", str(Path(outdir)/"_spec"),
           "--noconfirm", "--onefile"]
    return subprocess.run(cmd).returncode == 0

COMPILADORES = {
    "shc":          compilar_bash,
    "gcc":          compilar_c,
    "go_build":     compilar_go,
    "jar_launch4j": compilar_java,
    "pkg_nexe":     compilar_js,
    "micro_php":    compilar_php,
    "ps2exe":       compilar_ps1,
    "pyinstaller":  compilar_python,
}

# ════════════════════════════════════════════════════════════════════════════
#  MODOS
# ════════════════════════════════════════════════════════════════════════════

def modo_empaquetar():
    limpiar(); print(BANNER)
    print(f"\n{O}{BD}  ── Empaquetar a ejecutable ──{R}")
    lang = menu_lenguaje()
    if not lang: return
    src    = pedir_ruta(f"Ruta del archivo {lang['ext']}:")
    outdir = pedir_directorio("Carpeta de salida")
    Path(outdir).mkdir(parents=True, exist_ok=True)
    name   = pedir_nombre("Nombre del ejecutable", Path(src).stem)
    print(f"\n  {GY}Empaquetando {Path(src).name} ...{R}\n")
    fn = COMPILADORES.get(lang["metodo_exe"])
    ok = fn(src, outdir, name) if fn else False
    print(f"\n  {GR}✅ Completado.{R}" if ok else f"\n  {RE}❌ Fallo el empaquetado.{R}")
    pausar()

def modo_ofuscar(empaquetar_despues=False):
    limpiar(); print(BANNER)
    accion = "Ofuscar y empaquetar" if empaquetar_despues else "Ofuscar"
    print(f"\n{O}{BD}  ── {accion} ──{R}")
    lang = menu_lenguaje()
    if not lang: return
    src    = pedir_ruta(f"Ruta del archivo {lang['ext']}:")
    outdir = pedir_directorio("Carpeta de salida")
    Path(outdir).mkdir(parents=True, exist_ok=True)
    codigo  = Path(src).read_text(encoding="utf-8", errors="replace")
    ofuscar = OFUSCADORES.get(lang["metodo_ofu"])
    if not ofuscar:
        print(f"  {RE}Ofuscacion no disponible para este lenguaje.{R}")
        pausar(); return
    print(f"\n  {GY}Ofuscando con metodo: {lang['metodo_ofu']}...{R}")
    resultado = ofuscar(codigo)
    stem      = Path(src).stem
    ruta_ofu  = Path(outdir) / f"{stem}_ofu{lang['ext']}"
    ruta_ofu.write_text(resultado, encoding="utf-8")
    print(f"  {GR}✅ Ofuscado:{R} {ruta_ofu}")
    print(f"  {GY}Original : {len(codigo.encode())/1024:.1f} KB"
          f"  →  Ofuscado : {len(resultado.encode())/1024:.1f} KB{R}")
    if empaquetar_despues:
        name = pedir_nombre("Nombre del ejecutable", stem)
        print(f"\n  {GY}Empaquetando...{R}\n")
        fn = COMPILADORES.get(lang["metodo_exe"])
        ok = fn(str(ruta_ofu), outdir, name) if fn else False
        print(f"\n  {GR}✅ Completado.{R}" if ok else f"\n  {RE}❌ Fallo el empaquetado.{R}")
    pausar()

# ════════════════════════════════════════════════════════════════════════════
#  MENU PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

def mostrar_menu():
    limpiar(); print(BANNER)
    print(f"""
  {WH}Selecciona una opcion:{R}

  {WH}[1]{R} Empaquetar script a ejecutable
  {WH}[2]{R} Ofuscar script
  {WH}[3]{R} Ofuscar y empaquetar a ejecutable
  {WH}[4]{R} Salir

  {GY}Lenguajes: Bash · C · Go · Java · JavaScript · PHP · PowerShell · Python{R}
{GY}─────────────────────────────────────────────────────────────────────────{R}""")
    while True:
        op = input(f"  {O}>{R} ").strip()
        if op in ("1","2","3","4"):
            return op
        print(f"  {RE}Opcion invalida.{R}")

# ════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    while True:
        op = mostrar_menu()
        if   op == "1": modo_empaquetar()
        elif op == "2": modo_ofuscar(False)
        elif op == "3": modo_ofuscar(True)
        elif op == "4":
            limpiar()
            print(f"\n{O}                         ForjaX v{VERSION} - {AUTOR}{R}")
            print(f"{O}                           \U0001f525 !Hasta luego! \U0001f525{R}\n")
            break