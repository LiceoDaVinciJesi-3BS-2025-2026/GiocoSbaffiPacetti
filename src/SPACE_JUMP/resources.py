from importlib.resources import files
from pathlib import Path

def get_sound(filename: str) -> Path:
    return files(__package__) / "sounds" / filename

def get_image(filename: str) -> Path:
    return files(__package__) / "images" / filename