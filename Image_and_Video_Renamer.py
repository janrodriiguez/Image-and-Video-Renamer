import os
from datetime import datetime

# Nombre del archivo de registro
log_file = "log.txt"

# Explicación para el usuario
print("\nEscribe la ruta completa C:\\... recuerda que si tiene \
espacios, deberá ir entre comillas.\n\nSi no conoces el directorio, \
dale click derecho a la imagen, *copiar como ruta* y a la hora de pegarlo, \
elimina el nombre del archivo.<extension> y las comillas en caso de que \
la ruta no tenga espacios\n")

# Input de la ruta
folder_path = input("Path: ").lower()

# Verificar si la ruta existe
if not os.path.exists(folder_path):
    print("\n\033[31m[ERROR] La ruta especificada no existe. Verifica la ruta y vuelve a intentarlo.\033[0m\n")
else:
    # Obtener la lista de archivos en la carpeta especificada
    file_list = os.listdir(folder_path)

    # Filtrar la lista para obtener archivos de imagen y video (por extensión)
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.heic']
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.heif', '.hevc']

    # Leer el registro existente o crear uno nuevo
    processed_files = set()
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            processed_files = set(line.strip() for line in f)

    # Inicializar un diccionario para realizar un seguimiento de los nombres de archivo y contar los duplicados
    file_name_count = {}

    print("\n\033[33m[WARNING] Renombrando archivos, por favor, ten paciéncia...\033[0m")

    # Lista para almacenar los nuevos nombres de archivo
    new_file_names = []

    # Obtener la fecha de modificación de los archivos desde los metadatos
    for file in file_list:
        file = file.lower()
        if any(file.endswith(ext) for ext in image_extensions + video_extensions) and file not in processed_files:
            media_path = os.path.join(folder_path, file)
            ti_c = os.path.getmtime(media_path)

            formatted_time = datetime.fromtimestamp(ti_c).strftime('%Y-%m-%d')

            # Obtener el nombre base del archivo (sin extensión) y la extensión
            file_name_base, file_extension = os.path.splitext(file)

            # Verificar si el archivo ya existe con el mismo nombre y extensión
            if file_name_base in file_name_count:
                if file_extension == os.path.splitext(file_name_count[file_name_base])[1]:
                    new_file_name = file_name_count[file_name_base]
                    file_name_count[file_name_base] += 1
                else:
                    new_file_name = formatted_time
            else:
                new_file_name = formatted_time

            # Agregar la extensión al nuevo nombre de archivo
            new_file_name = f"{new_file_name}{file_extension}"

            new_media_path = os.path.join(folder_path, new_file_name)

            # Verificar si el archivo ya existe y añadirle un paréntesis
            while os.path.exists(new_media_path):
                if file_name_base in file_name_count:
                    file_name_count[file_name_base] += 1
                    new_file_name = f"{formatted_time} ({file_name_count[file_name_base]}){file_extension}"
                else:
                    new_file_name = f"{formatted_time} (1){file_extension}"
                    file_name_count[file_name_base] = 1
                new_media_path = os.path.join(folder_path, new_file_name)

            os.rename(media_path, new_media_path)
            processed_files.add(new_file_name)  # Agregar el archivo procesado al conjunto
            new_file_names.append(new_file_name)

    # Función personalizada para obtener la extensión de un archivo
    def get_file_extension(file_name):
        _, file_extension = os.path.splitext(file_name)
        return file_extension

    # Ordenar la lista de nuevos nombres de archivo por extensión
    new_file_names.sort(key=get_file_extension)

    # Imprimir los archivos renombrados ordenados por extensión
    for new_file_name in new_file_names:
        print(f"\n｜Archivo renombrado a: {new_file_name}")

    # Actualizar el archivo de registro con los archivos procesados ordenados por extensión
    with open(log_file, "w") as f:
        processed_files_list = list(processed_files)
        processed_files_list.sort(key=get_file_extension)
        for file in processed_files_list:
            f.write(file + "\n")

    print("\n\033[32m[OK] Proceso de renombrado completado.\033[0m")

    # Agregar la sección para mostrar los archivos previamente modificados según el registro
    print("\n\033[32m[OK] Archivos previamente modificados según el registro:\033[0m")
    for processed_file in processed_files_list:
        print(f"\n｜{processed_file}")
    print("")

# Espera a que el usuario presione Enter para salir
input("Presiona Enter para terminar el script...")
