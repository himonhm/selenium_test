import os
import time

from tests.conftest import DOWNLOAD_FOLDER


def get_latest_file_path(
    folder_path: str = DOWNLOAD_FOLDER, retries: int = 60
) -> str | None:
    for _ in range(retries):
        time.sleep(1)
        files = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ]
        if not files:
            raise ValueError(f"В папке {folder_path} нет файлов")
        file_name = max(files, key=os.path.getmtime)
        if not file_name.endswith(".crdownload"):
            return file_name
    return None


def get_file_size(file_path) -> int:
    return os.path.getsize(file_path) / (1024 * 1024)
