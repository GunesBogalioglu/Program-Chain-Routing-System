import time
import file_util

file_util.create_directory(".\\logs")
logfileloc = ".\\logs\\log.log"
log_levels = ["info", "error", "debug"]
log_level = "debug"


def log(msg, level, function_name):
    """Mesaj loglaması yapar.

    Args:
        msg (string): Mesaj
        level (string): Mesajın seviyesi ["info", "error", "debug"]
        function_name (string): Mesajın gönderildiği fonksiyonun ismi
    """
    if log_levels.index(log_level) > 0:
        tmp_msg = "[{level}][{time}][{function_name}] {msg}".format(
            level=level, function_name=function_name, msg=msg, time=time.ctime()
        )
        print(tmp_msg)
        file_util.write_to_file(logfileloc, tmp_msg)
    elif level == "info":
        print(msg)


# log("Logger test", "debug", "test")
