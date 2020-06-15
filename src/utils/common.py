import os
import sys
import logging
import datetime
import subprocess


def confirm_dialog(message):
    while True:
        op = input(message)
        if op.lower() == 'y':
            return 1
        elif op.lower() == 'n':
            return 0


def get_current_time_str():
    now = datetime.datetime.now()
    return now.isoformat()


def multi_makedirs(dirs, exist_ok=False):
    if not isinstance(dirs, list):
        dirs = list(dirs)
    for d in dirs:
        os.makedirs(d, exist_ok=exist_ok)


def get_logger(name='', log_file=None, debug=False):
    lvl = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=lvl)
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
        "%Y-%m-%d %H:%M:%S")
    stdhandler = logging.StreamHandler(sys.stdout)
    stdhandler.setFormatter(formatter)
    logger.addHandler(stdhandler)
    if log_file is not None:
        fhandler = logging.StreamHandler(open(log_file, "a"))
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
    logger.propagate = False
    logger.setLevel(lvl)
    return logger


def run_command(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    return output
