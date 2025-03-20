from pathlib import Path

def get_filenames(directory, marker):
    """
    Function to get a list of all files whose names contain the specified marker in the specified folder.
    
    Inputs:
        directory (str or Path): Directory to search through.
        marker (str): Identifier for the sought files (e.g., "*.fits" for wildcard search or "fits" for substring match).
    
    Outputs:
        file_names (list of str): A sorted list of all files in the directory that match the search marker.
    """
    directory = Path(directory)  # Convert to Path object
    if "*" in marker:  # If marker is a wildcard pattern
        file_names = sorted(directory.glob(marker))
    else:  # If marker is a substring in the filename
        file_names = sorted(f for f in directory.iterdir() if marker in f.name)

    return [str(f) for f in file_names]  # Convert to string paths for compatibility

