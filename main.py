import file_util
import engine
import user
from logger import log
import sqlite3 as sql
from multiprocessing.pool import ThreadPool

curdir = file_util.get_curdir()
inputdir = "\\inputs"
outputdir = "\\outputs"
tempdir = "\\tempdir"
tooldir = "\\tools"
concurrent_worker_count = 10
save_to_db = True  # Will be used on "watch folder" mode.
db = sql.connect("history.db")
# id,filename,before_size,before_crc,after_size,after_crc
db.execute(
    "CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT,filename TEXT,before_size INTEGER,before_crc INTEGER,after_size INTEGER,after_crc INTEGER)"
)
# db crc index oluşturma
db.execute(
    'CREATE INDEX IF NOT EXISTS "optimized_crc_index" ON "history" (after_crc ASC)'
)
# db size index oluşturma
db.execute(
    'CREATE INDEX IF NOT EXISTS "optimized_size_index" ON "history" (after_size ASC)'
)


def insert_to_history(file):
    """DB dosyasına file objesinden gelen isim,boyut ve crc değerini girer.

    Args:
        file (inputfile): Temel file objesini alır.
    """
    if not isoptimized(file):  # dbye tekrar tekrar aynı şeyin kaydını engeller.
        db.execute(
            'INSERT INTO history (filename,before_size,before_crc,after_size,after_crc) values("{filename}","{before_size}","{before_crc}","{after_size}","{after_crc}")'.format(
                filename=file.filename,
                before_size=file.inputsize,
                before_crc=file.inputcrc,
                after_size=file.outputsize,
                after_crc=file.outputcrc,
            )
        )
        db.commit()
        log(
            file.filename + " dosyası geçmişe kaydedildi.", "debug", "insert_to_history"
        )


def isoptimized(file):
    """DB'den dosyanın daha önce optimize edilip edilmediğini kontrol eder.

    Args:
        file (inputfile): Temel file objesini alır.

    Returns:
        bool:True ise optimize edilmiş. False ise optimize edilmemiş.
    """
    count = db.execute(
        "SELECT count(*) FROM history WHERE after_size={after_size} AND after_crc={after_crc}".format(
            after_size=file.inputsize, after_crc=file.inputcrc
        )
    )
    result = count.fetchone()[0]
    if result == 0:
        return False
    else:
        return True


class inputfile:
    """İşlenicek dosya objesi"""

    filename = None
    fileloc = None
    filedest = None
    methods = []
    inputsize = None
    outputsize = None
    optimizetype = None
    inputcrc = None
    outputcrc = None
    processed = None

    def __init__(
        self,
        filename,
        fileloc,
        filetmploc,
        filedest,
        methods,
        inputsize,
        optimizetype,
        inputcrc,
        processed,
    ):
        self.filename = filename
        self.fileloc = fileloc
        self.filetmploc = filetmploc
        self.filedest = filedest
        self.methods = methods
        self.inputsize = inputsize
        self.optimizetype = optimizetype
        self.inputcrc = inputcrc
        self.processed = processed


def main():
    losslessness = user.get_loss_settings()
    # Klasör oluşturma ve temizleme
    file_util.clear_folder(curdir + tempdir)
    file_util.create_directory(curdir + inputdir)
    file_util.create_directory(curdir + outputdir)
    file_util.create_directory(curdir + tempdir)
    file_util.copy_dirtree(curdir + inputdir, curdir + outputdir)
    file_util.copy_dirtree(curdir + inputdir, curdir + tempdir)

    tmparray = []
    for file in file_util.get_file_list(curdir + inputdir):
        dest = file.replace(inputdir, outputdir)
        tmpdir = file.replace(inputdir, tempdir)
        tmpfile = inputfile(
            file_util.get_filename(file),
            file,
            tmpdir,
            dest,
            engine.create_dynamic_toolchain(file),
            file_util.get_filesize(file),
            losslessness,
            file_util.crc32(file),
            False,
        )
        tmpfile.processed = isoptimized(tmpfile)

        tmparray.append(tmpfile)
    # bu metodun kötü yanı işlemlerin alıcağı zamanı birbiri ile eşitlemiyor. Bir workerin yapması gereken liste diğerlerinde ayrı olduğundan optimizasyon sonlarına doğru tek işlemci çalışıyor.
    # bunun aksine dosyaları bölmeyi kolaylaştırdığından bitirme projesinde kullanıcağım işlemleri kolaylaştırıyor.
    # başka bir poollama yöntemi ile bu sorun çözülebilir.
    tmparray_chunks = split_list(tmparray, concurrent_worker_count)
    pool = ThreadPool(concurrent_worker_count)
    pool_output = pool.map(
        engine.ignite, tmparray_chunks
    )  # pool_output ileride kullanılıcak. Daha yapılmadı.
    # pool_outputa başarılı başarsız diye array koy eğer başarısız çıkar ise optimizasyon işlemi tamamlandı yerine 1 dosya optimize edilemedi gibi birşey desin
    if save_to_db:
        for file in tmparray:
            insert_to_history(file)
    log("Optimizasyon işlemi tamamlandı.", "info", "main")


def split_list(source_list, wanted_parts=1):
    """Verilen arrayi istenilen sayıdaki parçaya böler.

    Args:
        source_list (array): Bölünücek kaynak liste.
        wanted_parts (int, optional): İstenilen parça sayısı. Defaults to 1.

    Returns:
        array^2:İçinde listeleri bulunduran liste.
    """
    length = len(source_list)
    log("Girdi listesi {}'e bölündü.".format(wanted_parts), "debug", "split_list")
    return [
        source_list[i * length // wanted_parts : (i + 1) * length // wanted_parts]
        for i in range(wanted_parts)
    ]


if __name__ == "__main__":
    main()
