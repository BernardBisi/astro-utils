# phot_utils/fits_utils.py
from astropy.io import fits
import numpy as np

def load_fits(fpath: str, extension: int = 0) -> tuple:
    """
    Load a FITS file and return the header and data from a specified extension.
    
    Parameters
    ----------
    fpath : str
        Path to the FITS file to load. Must end in .fit, .fits, .FIT, or .FITS.
    extension : int, optional
        The extension number to load (default is 0, the primary HDU).
        
    Returns
    -------
    tuple
        A tuple containing:
            - header: dict-like object containing the header data from the FITS file.
            - data: numpy.ndarray containing the data from the FITS extension.
    """
    with fits.open(fpath) as hdu:
        header = hdu[extension].header
        data = hdu[extension].data
    return header, np.array(data, dtype=float)

