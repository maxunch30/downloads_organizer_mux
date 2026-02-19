import os
from pathlib import Path
import shutil
from datetime import datetime

# Principal Configuration
downloads_path = Path.home() / 'Downloads'
# A folder for files that couldn't move
error_log = downloads_path / "organizer_errors.log"


print("=" * 60)
print("🔍 DIAGNÓSTICO DE RUTAS - WINDOWS 11")
print("=" * 60)
print(f"📁 Ruta detectada: {downloads_path}")
print(f"✅ ¿Existe?: {downloads_path.exists()}")
print(f"🔐 ¿Es accesible?: {os.access(downloads_path, os.R_OK)}")
print(f"📄 Archivos en Downloads: {len(list(downloads_path.iterdir()))}")
print("=" * 60)

# Listar primeros 10 archivos
print("\n📋 PRIMEROS 10 ARCHIVOS:")
for i, file in enumerate(downloads_path.iterdir()):
    if i >= 10:
        break
    print(f"   • {file.name} ({'CARPETA' if file.is_dir() else 'ARCHIVO'})")

print("=" * 60)


def organize_file(file_path):
    try:
        # Get a clean name and extension (ex: '.PDF' -> 'PDF')
        extension = file_path.suffix.upper()

        if not extension:
            return # Ignore files without extension
        
        # This creates a path for the final folder (ex: .../Downloads/PDF)
        folder_extension = downloads_path / extension[1:]
        folder_extension.mkdir(exist_ok=True) # This creates a folder if this don't exists

        # Define final path
        new_path = folder_extension / file_path.name

        # --- Duplicates managements ---
        if new_path.exists():
            # If it exists, we add a timestamp to avoid an overwrite
            timestamp = datetime.now().strftime(f"%Y%m%d_%H%M%S")
            stem = file_path.stem
            new_path = folder_extension / f"{stem}_{timestamp}{extension}"
            print(f'⚠️Duplicate name. Rename: {new_path.name}')
        
        # --- Move file ---
        shutil.move(str(file_path), str(new_path))
        print(f'✅ Moved: {file_path.name} -> {folder_extension.name}/')

    except PermissionError:
        print(f'❌ Permission denied: {file_path.name} (¿Is it open?)')
        with open(error_log, 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} - PermissionError: {file_path}\n')
    except Exception as e:
        print(f"❌ Unexpected error with {file_path.name}: {e}")

# --- Execution ---
if __name__ == '__main__':
    print(f'🔍 Scanning: {downloads_path}')

    for file in downloads_path.iterdir():
        if file.is_file():
            # Ignore the script itself and the error log.
            if file.name in ["organizer.py", "organizer_errors.log"]:
                continue
            organize_file(file)

    print("🎉 Process completed.")