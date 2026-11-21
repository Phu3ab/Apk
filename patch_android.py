"""Läuft im Workflow nach 'cap add android': Icon + Farben von Status-/Navigationsleiste."""
import re, shutil, pathlib
root = pathlib.Path(__file__).resolve().parent
res = root / "android" / "app" / "src" / "main" / "res"
# 1) Icons/Farben kopieren (überschreibt die Capacitor-Standard-Icons). Flach hochgeladen: res__<Ordner>__<Datei> -> res/<Ordner>/<Datei>
for f in root.glob("res__*"):
    _, folder, name = f.name.split("__", 2)
    (res / folder).mkdir(parents=True, exist_ok=True)
    shutil.copy(f, res / folder / name)
# Standard-Vordergrund-Vektoren entfernen, damit nichts dazwischenfunkt
for p in list(res.glob("drawable*/ic_launcher_foreground.xml")) + list(res.glob("drawable*/ic_launcher_background.xml")):
    p.unlink()
# 2) Themes: Statusleiste, Navigationsleiste, Start-Hintergrund
st = res / "values" / "styles.xml"
s = st.read_text(encoding="utf-8")
bars = (
    '\n        <item name="android:statusBarColor">@color/foe_bg</item>'
    '\n        <item name="android:navigationBarColor">@color/foe_bg</item>'
    '\n        <item name="android:windowLightStatusBar">false</item>'
    '\n        <item name="android:windowLightNavigationBar">false</item>'
)
s = re.sub(r'(<style name="AppTheme\.NoActionBar"[^>]*>)', lambda m: m.group(1) + bars, s, count=1)
s = re.sub(r'(<style name="AppTheme\.NoActionBarLaunch"[^>]*>)', lambda m: m.group(1) + bars, s, count=1)
s = s.replace("@drawable/splash", "@color/foe_bg")
st.write_text(s, encoding="utf-8")
print(st.read_text(encoding="utf-8"))
