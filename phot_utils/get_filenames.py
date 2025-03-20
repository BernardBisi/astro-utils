# phot_utils/file_utils.py
from glob import glob
from pathlib import Path

def get_filenames(directory: str, marker: str) -> list:
    """
    Get a list of all files in a directory that match the specified marker.

    Args:
        directory (str): Directory to search in.
        marker (str): Identifier for the sought files, e.g., "*.fits".

    Returns:
        list: Sorted list of file paths matching the search marker.
    """
    file_list = sorted(glob(str(Path(directory) / marker)))
    return file_list

