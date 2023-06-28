import logging
import os

# Определение логгера
api_logger = logging.getLogger('api')

# Определение пути к папке с логами
LOGS_FOLDER = os.path.join(os.path.dirname(__file__), 'logs')
LOG_FILE = os.path.join(LOGS_FOLDER, 'api.log')

# Настройка уровня логирования
api_logger.setLevel(logging.INFO)

# Определение форматтера
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Определение обработчика файла
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)

# Добавление обработчика к логгеру
api_logger.addHandler(file_handler)
