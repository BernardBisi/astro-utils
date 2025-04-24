import numpy as np
import glob
import os
from astropy.io import fits


# Utility function from get_filenames.py
def get_filenames(directory, pattern):
    """
    Get a list of filenames in a directory matching a pattern.
    """
    return glob.glob(os.path.join(directory, pattern))


# Utility function from fits_reader.py
def load_fits(file_path):
    """
    Load a FITS file and return its header and data.
    """
    with fits.open(file_path) as hdul:
        header = hdul[0].header
        data = hdul[0].data
    return header, data


def create_master_frame(file_dir, method=np.median, output_dir=None, bulk=50):
    """
    Create a master frame by processing FITS files in batches.

    Parameters:
    - file_dir: Directory containing the FITS files.
    - method: Method to combine the frames (e.g., np.median).
    - output_dir: Directory to save the master frame. Defaults to file_dir.
    - bulk: Number of files to process in each batch.
    """
    if output_dir is None:
        output_dir = file_dir

    fits_files = get_filenames(file_dir, "*.fits")
    num_files = len(fits_files)
    batch_master_frames = []

    for i in range(0, num_files, bulk):
        # Get the current batch of files
        batch_files = fits_files[i:i + bulk]
        data_list = []

        # Load data from each file in the batch
        for fits_file in batch_files:
            _, data = load_fits(fits_file)
            data_list.append(data)

        # Combine the data using the specified method
        master_frame = method(data_list, axis=0)

        # Save the master frame for the current batch
        batch_index = i // bulk
        output_path = os.path.join(output_dir, f"master_frame_batch_{batch_index}.fits")
        fits.writeto(output_path, master_frame, overwrite=True)

        # Keep track of batch master frames
        batch_master_frames.append(master_frame)

        print(f"Processed batch {batch_index + 1}/{(num_files + bulk - 1) // bulk}: {output_path}")

    # Combine all batch master frames to create the final master frame
    final_master_frame = method(batch_master_frames, axis=0)
    final_output_path = os.path.join(output_dir, "final_master_frame.fits")
    fits.writeto(final_output_path, final_master_frame, overwrite=True)

    print(f"Final master frame saved to: {final_output_path}")

