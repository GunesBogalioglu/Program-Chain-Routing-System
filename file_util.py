import os
import shutil
import zlib


def zipfolder(file_name, folder):
    shutil.make_archive(file_name, "zip", folder)


def unzipfolder(filename, destination):
    shutil.unpack_archive(filename, destination)


def crc32(target, chunksize=65536):
    """İstenilen dosyanın crc32 değerini hesaplar.

    Args:
        target (string): Hedef dosya
        chunksize (int, optional): Blok boyutu (Default bırakmanız tercih edilir.). Defaults to 65536.

    Returns:
        int: Dosyanın crc32 değeri
    """
    with open(target, "rb") as f:
        checksum = 0
        while chunk := f.read(chunksize):
            checksum = zlib.crc32(chunk, checksum)
        return checksum


def get_file_list(target):
    """İstenilen klasördeki dosyaların listesini getirir.

    Args:
        target (string): Hedef klasör

    Returns:
        List: Dosya listesi
    """
    file_paths = []
    for root, dirs, files in os.walk(target):
        for name in files:
            file_path = os.path.join(root, name)
            file_paths.append(file_path)
    return file_paths


def copy_dirtree(src, dst):
    """Belirtilen klasör sistemini hedef klasörde oluşturur.

    Args:
        src (string): Kaynak klasör
        dst (string): Hedef klasör
    """
    src = os.path.abspath(src)
    src_prefix = len(src) + len(os.path.sep)
    try:
        # os.makedirs(dst)
        for root, dirs, files in os.walk(src):
            for dirname in dirs:
                dirpath = os.path.join(dst, root[src_prefix:], dirname)
                os.mkdir(dirpath)
    except:
        # print("Copy_dirtree failed")
        pass


def get_filesize(file):
    """İstenilen dosyanın boyutunu getirir.

    Args:
        file (string): Dosyanın konumu

    Returns:
        int: Dosyanın boyutu
    """
    try:
        size = os.path.getsize(file)
        if type(size) is type(None):  # Type None check
            return 0
        return size
    except Exception:  # Dosya bulunamaz yada okunamaz ise boyutu 0 al.
        return 0


def join_paths(root, dir):
    """Konum ve klasörü birleştirir.

    Args:
        root (string): Konum
        dir (string): Klasör

    Returns:
        string: Konum + klasör
    """
    return os.path.join(root, dir)


def get_curdir():
    """Programın bulunduğu konumu getirir.

    Returns:
        string: Programın konumu
    """
    return os.curdir


def create_directory(dir):
    """Belirtilen yere klasör oluşturur.

    Args:
        dir (string): Klasör konumu
    """
    try:
        os.mkdir(dir)
    except:
        pass


def remove_file(file):
    """Belirtilen dosyayı siler.

    Args:
        file (string): Dosya konumu
    """
    try:
        os.remove(file)
    except:
        pass


def copy_file(src, dst):
    """Belirtilen dosyayı istenilen yere kopyalar.

    Args:
        src (string): Kaynak konumu
        dst (string): Hedef konumu
    """
    try:
        shutil.copy(src, dst)
    except:
        pass


def get_filename(file):
    """Dosyanın ismini getirir.

    Args:
        file (string): Dosya konumu

    Returns:
        string: Dosyanın ismi
    """
    return os.path.basename(file)


def get_fileext(file):
    """Dosya uzantısını getirir.

    Args:
        file (string): Dosya konumu

    Returns:
        string: Dosyanın uzantısı (küçük harflerle)
    """
    ext = os.path.splitext(os.path.basename(file))
    return ext[1].lower()


def move_file(src, dst):
    """Belirtilen dosyayı taşır.

    Args:
        src (string): Kaynak dosya konumu
        dst (string): Hedef dosya konumu
    """
    try:
        os.replace(src, dst)
    except:
        pass


def clear_folder(folder):
    """Belirtilen klasörün içerini siler

    Args:
        folder (string): Klasör
    """
    try:
        shutil.rmtree(folder)
    except OSError:
        pass


def write_to_file(file, msg=None):
    """Verilen stringi dosyaya yaz.

    Args:
        file (string): Dosyanın konumu
        msg (string, optional): Dosyaya yazılıcak string. Defaults to None.
    """
    try:
        with open(file, "a") as f:
            f.write("{}\n".format(msg))
    except Exception:
        open(file, "w").write(msg)


def check_file_exists(file):
    try:
        if os.path.exists(file):
            return True
        else:
            return False
    except OSError:
        pass
