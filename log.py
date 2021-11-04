import logging


class logbook():

    def createINFOLogger(self):
        logger = logging.getLogger('INFO')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        file_handler = logging.FileHandler('INFO.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger


    def createERRORLogger(self):
        logger = logging.getLogger('ERROR')
        logger.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        file_handler = logging.FileHandler('ERROR.log')
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
