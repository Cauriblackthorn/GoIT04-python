
import sys
import shutil
from pathlib import Path

SYMBOLS = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
CYRILIC = ("а", "б", "в", "г", "ґ", "д", "е", "є", "ж", "з", "и", "і", "ї", "й",
           "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч",
           "ш", "щ", "ю", "я", "ь", "ъ", "ё", "э", "ы")
LATINE = ("a", "b", "v", "h", "g", "d", "e", "ye", "zh", "z", "i", "i", "yi", "y",
          "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "kh", "ts", "ch",
          "sh", "shch", "yu", "ya", "", "", "yo", "e", "i")

TRANSLATE_DICT = {}
for c, l in zip(CYRILIC, LATINE):
    TRANSLATE_DICT[ord(c)] = l
    TRANSLATE_DICT[ord(c.upper())] = l.upper()

IMAGE_EXTENS = ['JPEG', 'PNG', 'JPG', 'SVG']
DOCUMENT_EXTENS = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
AUDIO_EXTENS = ['MP3', 'OGG', 'WAV', 'AMR']
VIDEO_EXTENS = ['AVI', 'MP4', 'MOV', 'MKV']
ARCHIVE_EXTENS = ['ZIP', 'GZ', 'TAR']


path = Path(sys.argv[1])

""" Функция транслитерации file_name - название файла, до расширения"""
def normalize(file_name):

    file_name = file_name.translate(TRANSLATE_DICT)
    for sign in SYMBOLS:
        file_name = file_name.replace(sign, "_")
    return file_name

"""Создание папок и иперенос файлов пдходящего типа"""
def create_dir(dir_name):

    dir_name_path = Path(str(path) + f"/{dir_name}")
    if not dir_name_path.exists():
        dir_name_path.mkdir()
    return dir_name_path


images_path = create_dir("images")
documents_path = create_dir("documents")
audio_path = create_dir("audio")
video_path = create_dir("video")
archives_path = create_dir("archives")
another_path = create_dir("another")

DIR_EXT = {images_path: IMAGE_EXTENS,
           documents_path: DOCUMENT_EXTENS,
           audio_path: AUDIO_EXTENS,
           video_path: VIDEO_EXTENS,
           archives_path: ARCHIVE_EXTENS}

""" Разбивает название файла на две части (нозвание и расширение)"""

def get_name_extension(general_name):

    dot_position = general_name.rfind(".")
    name = general_name[:dot_position]
    extension = general_name[dot_position+1:]
    return name, extension

"""Переносит файл в папку, которая была создана ранее под его расширение"""
def transport_file(file):


    file_name, file_extension = get_name_extension(file.name)
    norm_name = normalize(file_name)+"."+file_extension

    for key, val in DIR_EXT.items():
        if file_extension.upper() in val:
            file.rename(str(key) + '/' + norm_name)
            return
    file.rename(str(another_path) + '/' + norm_name)

"""Проверка и игнорирование создания папки, если она была создана ранее """
def ignore(elem):

    for key in DIR_EXT.keys():
        if str(elem) == str(key):
            return True
    return False

"""Рекурсивно достаем файлы из папок и определяем метод сортировки"""
def sort(dir_path):

    for element in dir_path.iterdir():
        if ignore(element):
            continue
        if element.is_dir():
            sort(element)
        else:
            transport_file(element)


sort(path)
for arc in archives_path.iterdir():
    if arc.is_dir():
        continue
    arc_name, arc_ext = get_name_extension(str(arc))
    if arc_ext.upper() not in ARCHIVE_EXTENS:
        continue
    shutil.unpack_archive(arc, arc_name)