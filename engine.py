import file_util
import subprocess
import json
from logger import log

curdir = file_util.get_curdir()
inputdir = "\\inputs"
outputdir = "\\outputs"
tempdir = "\\tempdir"
tooldir = "\\tools"


def get_tool_list():
    """Tool list

    Returns:
        array: Tool list
    """
    tmparr = []
    for tool in file_util.get_file_list(curdir + tooldir):
        if tool.endswith(".json"):
            tmparr.append(file_util.get_filename(tool).split(".")[0])
    return tmparr


def get_config(tool):
    """Method json dosyasını okur.

    Args:
        tool (string): Method.

    Returns:
        json: Method'un json objesi
    """
    jsn = json.load(open("{}\\{}.json".format(curdir + tooldir, tool)))
    return jsn


def get_config_priority(i):
    """Verilen methodun prioritysini verir.

    Args:
        i (string): Method ismi.

    Returns:
        int: priority of method
    """
    return get_config(i)["priority"]


# dinamik toolchain oluşturma metodu
def create_dynamic_toolchain(file):
    """Dinamik olarak method zinciri oluşturur.

    Args:
        file (inputfile): Temel file objesini alır.

    Returns:
        array:method listesi.
    """
    tmparr = []
    tool_list = get_tool_list()
    for tool in tool_list:
        tmpjsn = get_config(tool)["support"]
        ext = file_util.get_fileext(file)
        if ext in tmpjsn:
            tmparr.append(tool)
            # print("{} eklendi.".format(tool))
    tmparr.sort(key=get_config_priority)
    return tmparr


def engine(file):
    """Dosyaları file.method'un içindeki methodlara göre işlemden geçirir.

    Args:
        file (inputfile): Temel file objesini alır.

    Returns:
        int: file.outputsize'ı geri verir.
    """
    if file.outputsize == 0:  # bug check will remove
        return 0
    if file.processed:
        file_util.move_file(file.filetmploc, file.filedest)
        log(
            "{input} dosyası daha önce optimize edildiği için {output}'e taşındı.".format(
                input=file.fileloc, output=file.filedest
            ),
            "debug",
            "engine",
        )
        # queue.task_done()
        return file.outputsize
    if len(file.methods) == 0:
        file_util.move_file(file.filetmploc, file.filedest)
        log(
            "{input} dosyası {output}'e taşındı.".format(
                input=file.fileloc, output=file.filedest
            ),
            "debug",
            "engine",
        )
        return file.outputsize

    else:
        method = file.methods[0]
        if file.optimizetype:
            losslessness = "lossless"
        else:
            losslessness = "lossy"
        tmp_str = file_util.get_fileext(file.filename).split(".")[1] + "_"
        tmp_str += losslessness

        # lossless mi değilmi kontrol et ona göre dosya uzantısı için ayarlanan argümentleri al
        # veya argümentleri burda oluştur. Örn:Fileoptimizerda yapıldığı gibi
        methodjson = get_config(method)

        try:
            args = (
                methodjson[tmp_str]
                .replace("fileloc", file.filetmploc)
                .replace("filedest", file.filetmploc)
            )
        except Exception:
            args = (
                methodjson["default_args"]
                .replace("fileloc", file.filetmploc)
                .replace("filedest", file.filetmploc)
            )

        subprocess.run(
            "{}\\{} {}".format(curdir + tooldir, methodjson["filename"], args),
            shell=False,
            capture_output=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        log(
            '{input} dosyası "{method}" ile optimize edildi.'.format(
                input=file.fileloc, method=method
            ),
            "debug",
            "engine",
        )

        file.methods.remove(method)
        file.outputsize = file_util.get_filesize(file.filetmploc)
        return engine(file)


def ignite(files):
    """Verilen listeyi böler ve engine'e gönderir.

    Args:
        files (list): file objelerinden oluşan liste.

    Returns:
        dict: total_input,total_output,total_progression,crc32 gibi değerleri sözlük olarak verir.
    """
    file_crcs = []
    total_input_file_size = 0
    total_output_file_size = 0
    total_progression = 0
    # current_progression = 0
    total_progression = len(files)
    for file in files:
        file.inputsize = file_util.get_filesize(file.fileloc)
        # current_progression += 1
        total_input_file_size += file.inputsize
        # Test amaçlı copy_file olarak değiştirlebilir.
        # def. move_file
        file_util.copy_file(file.fileloc, file.filetmploc)
        file.outputsize = engine(file)
        if type(file.outputsize) != type(None):
            total_output_file_size += file.outputsize

        file.outputcrc = file_util.crc32(file.filedest)
        file_crcs.append(file.outputcrc)
    # İstatistik toplarken lazım olucak.
    tmpdict = dict()
    tmpdict["total_input"] = total_input_file_size
    tmpdict["total_output"] = total_output_file_size
    tmpdict["total_progression"] = total_progression
    tmpdict["crc32"] = file_crcs
    return tmpdict
