import numpy as np
import matplotlib.pyplot as plt
from astropy.wcs import WCS

def implot(image, figsize=(15, 13), cmap='gray_r', scale=0.5, colorbar=False, header=None, wcs=None, **kwargs):
    """
    Plot an astronomical image with default options and support for WCS projection.
    
    Parameters
    ----------
    image : array_like
        2D array containing an astronomical image.
    figsize : tuple, optional
        Figure size (default: (15, 13)).
    cmap : str, optional
        Colormap to use for the image (default: 'gray_r').
    scale : float, optional
        Scale for image contrast, defining the range as mean ± scale * std (default: 0.5).
    colorbar : bool, optional
        Whether to add a colorbar (default: False).
    header : dict, optional
        FITS header; used to construct a WCS projection if `wcs` is not provided (default: None).
    wcs : WCS, optional
        WCS object for celestial coordinate plotting (default: None).
    **kwargs
        Additional arguments passed to `imshow` (e.g., vmin, vmax).
    
    Returns
    -------
    fig, ax : matplotlib.figure.Figure, matplotlib.axes.Axes
        The figure and axis objects containing the plotted data.
    """
    # Handle WCS projection
    if wcs is None and header is not None:
        header = {k: v for k, v in header.items() if not k.startswith(('A_', 'B_'))}  # Remove SIP distortion keywords
        wcs = WCS(header)
    
    # Create figure and axis
    projection_kw = {'projection': wcs} if wcs else {}
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=projection_kw)
    
    # Configure celestial axis if WCS is provided
    if wcs:
        ax.set_xlabel('Right Ascension [hms]', fontsize=15)
        ax.set_ylabel('Declination [degrees]', fontsize=15)
        ax.coords.grid(color='gray', alpha=0.5, linestyle='solid')
    
    # Compute intensity limits
    mu, sigma = np.mean(image), np.std(image)
    vmin, vmax = kwargs.get('vmin', mu - scale * sigma), kwargs.get('vmax', mu + scale * sigma)
    
    # Plot image
    im = ax.imshow(image, origin='lower', cmap=cmap, vmin=vmin, vmax=vmax)
    
    # Add colorbar if requested
    if colorbar:
        plt.colorbar(im, ax=ax)
    
    ax.tick_params(direction='in', length=9, width=1.5, labelsize=15)
    
    return fig, ax

