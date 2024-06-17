from pathlib import Path

import requests
import zipfile


BASE_DIR = Path(__file__).parent.resolve()
FONT_FILE_PATH = BASE_DIR / "seguiemj.ttf"


def download_segoe_ui_emoji_font():
    font_url = "https://example.com/seguiemj.ttf"  # Replace with a valid URL
    response = requests.get(font_url)
    with open(FONT_FILE_PATH, "wb") as file:
        file.write(response.content)


def download_noto_emoji_font():
    font_url = (
        "https://noto-website-2.storage.googleapis.com/pkgs/NotoEmoji-unhinted.zip"
    )
    font_zip_path = BASE_DIR / "NotoEmoji.zip"

    # Download the zip file
    response = requests.get(font_url)
    with open(font_zip_path, "wb") as file:
        file.write(response.content)

    # Extract the font file from the zip
    with zipfile.ZipFile(font_zip_path, "r") as zip_ref:
        zip_ref.extractall(BASE_DIR)


if __name__ == "__main__":
    if not FONT_FILE_PATH.exists():
        download_segoe_ui_emoji_font()
    print(f"Font downloaded and saved at {FONT_FILE_PATH}")
