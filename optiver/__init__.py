import os
from pathlib import Path


class Directories:
    """
    Holds all the important directories in data/ as pathlib path objects.

    Object properties:
    data -- data/
    raw -- data/raw/
    interim -- data/interim/
    processed -- data/processed/
    splits -- data/splits/
    """
    def __init__(self, root: str):
        """
        Initialize the directories object based on the project root.

        Keyword arguments:
        root -- A Linux style path to the root of this project.
        """
        root_dir = Path(root)

        self.data = root_dir / "data"
        self.raw = self.data / "raw"
        self.interim = self.data / "interim"
        self.processed = self.data / "processed"
        self.splits = self.data / "splits"

        def init_dir(directory):
            os.makedirs(directory, exist_ok=True)

        init_dir(self.data)
        init_dir(self.raw)
        init_dir(self.interim)
        init_dir(self.processed)
        init_dir(self.splits)
