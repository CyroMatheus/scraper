import pandas as pd
import os, logging, json

class CSVManager:
    def __init__(self, model):
        files = ["tag", "category"]
        path = f"{os.getcwd()}/data/{model}/"
        self.path = path
        for file in files:
            if not os.path.exists(path) :
                os.makedirs(path, exist_ok=True)
            if self.read(file) is None:
                data = dict()
                match file:
                    case "tag":
                        data.update({element: dict() for element in ["id", "tag"]})
                    case "category":
                        data.update({element: dict() for element in ["id", "category"]})
                self.write(file, data)

    def read(self, file):
        try:
            return pd.read_csv(f"{self.path}{file}.csv")
        except Exception as e:
            return self.write(file, dict())

    def write(self, filename, data):
        df = pd.DataFrame(data)
        path = f"{self.path}{filename}.csv"
        df.to_csv(path, index=False)

    def insert(self, file, data):
        file = f"{self.path}{file}.csv"
        df_new = pd.DataFrame(data)
        try:
            df_now = pd.read_csv(file)
            df_final = pd.concat([df_now, df_new], ignore_index=True)
        except Exception as se:
            df_final = df_new
        df_final.to_csv(file, index=False)
        
    def search(self, file, colunm, value):
        try:
            df = self.read(file)
            if colunm not in df.columns:
                raise ValueError(f"Coluna '{colunm}' não encontrada .")
            result = df[df[colunm] == value]
            if not result.empty:
                return result
        except Exception as e:
            return None

    def getLatestPosition(self, file):
        df = self.read(file)
        return df.tail(1)

class LogManager:
    def __init__(self, model):
        super().__init__()
        self.logger = logging.getLogger(model)
        path = f"{os.getcwd()}/data/{model}/"
        log_file_path = f"{os.getcwd()}/data/{model}/{model}.log"
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        if not os.path.exists(log_file_path):
            with open(log_file_path, 'w+'):
                pass

        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(log_file_path)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
    def msg(self, log_type, msg):
        match log_type:
            case "debug":
                self.logger.debug(msg)
            case "info":
                self.logger.info(msg)
            case "warning":
                self.logger.warning(msg)
            case "error":
                self.logger.error(msg)
            case "critical":
                self.logger.critical(msg)

class JsonManager():
    def __init__(self, model):
        self.path = f"{os.getcwd()}/data/{model}/"

    def read(self, file):
        try:
            with open(f"{self.path}{file}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return self.write(file, [])

    def insert(self, file, data):
        file_path = self.read(file)
        file_path.update(data)
        self.write(file, file_path)

    def write(self, file, data):
        path = f"{self.path}{file}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def search_key(self, file, dict_key):
        slug = dict_key.split('_')
        slug = slug[0]
        file_path = self.read(file)
        keys = list(file_path.keys())
        for key, value in enumerate(keys):
            key_uuid = value.split("_")
            keys[key] = key_uuid[0]
        if slug in keys:
            return True
        return False

    def page(self):
        try:
            page = json.load(open(self.path))
            page = list(page.keys())
            return int(page[0])
        except Exception as e:
            return 1
