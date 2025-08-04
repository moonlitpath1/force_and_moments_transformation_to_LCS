import os
import pandas as pd
from math import sqrt

# Assuming 'env' is a custom module providing file paths
import env 

# Constants for pandas display options (applied globally)
PD_DISPLAY_OPTIONS = {
    'display.max_columns': None,
    'display.max_rows': None,
    'display.max_colwidth': None,
    'display.width': 0
}

def get_lcs_def_data():
    """
    Load and parse Local Coordinate System (LCS) definition data from a file.
    
    This function reads a file with specific formatting (e.g., lines starting with 'CORD2R' or '+'),
    extracts numerical blocks, handles exponential notation (e.g., '1.23-4' -> 1.23e-4), and returns
    the origin, z-point, and x-point as lists of floats.
    
    Returns:
        tuple: (origin, z_point, x_point) each as lists of 3 floats.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If insufficient data is extracted.
    """
    if not os.path.exists(env.lcs_def_path):
        raise FileNotFoundError(f"File not found at {env.lcs_def_path}")
    
    extracted_data = []
    with open(env.lcs_def_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Determine start index based on line prefix
            start_index = 3 if line.startswith('CORD2R') else 1 if line.startswith('+') else -1
            if start_index == -1:
                continue
            # Split line into 8-character blocks
            blocks = [line[i:i+8].strip() for i in range(0, len(line), 8)]
            for block in blocks[start_index:]:
                if not block:
                    continue
                try:
                    # Handle exponential notation by replacing the last '-' with 'e-'
                    if '-' in block[1:]:  # Ignore leading minus
                        parts = block.rsplit('-', 1)
                        if len(parts) == 2:
                            block = f"{parts[0]}e-{parts[1]}"
                    extracted_data.append(float(block))
                except ValueError:
                    continue  # Skip non-numeric blocks
    
    if len(extracted_data) < 9:
        raise ValueError("Insufficient data extracted from LCS file (expected at least 9 values)")
    
    return extracted_data[0:3], extracted_data[3:6], extracted_data[6:9]

def get_vector_data():
    """
    Load and clean vector data from a CSV file.
    
    This function reads the CSV, forward-fills key columns, filters out 'Centroid' rows,
    renames columns, assigns unique file_ids (e.g., 'f001'), and returns a cleaned DataFrame
    with forces (Fx, Fy, Fz) and moments (Mx, My, Mz).
    
    Returns:
        pd.DataFrame: Cleaned data with columns ['file_id', 'file', 'nodeid', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'].
    """
    # Read CSV, assuming header starts at row 3 (0-indexed)
    df = pd.read_csv(env.csv_file_path, header=2)
    
    # Forward-fill to propagate values
    df['Result File'] = df['Result File'].ffill()
    df['Summation Point'] = df['Summation Point'].ffill()
    
    # Exclude 'Centroid' rows
    df_data = df[df['Summation Point'] != 'Centroid'].copy()
    
    # Rename columns for clarity
    df_data.rename(columns={
        'Result File': 'file',
        'Summation Point': 'nodeid'
    }, inplace=True)
    
    # Assign unique file_ids like 'f001', 'f002', etc.
    unique_files = df_data['file'].unique()
    file_map = {fname: f"f{str(i+1).zfill(3)}" for i, fname in enumerate(unique_files)}
    df_data['file_id'] = df_data['file'].map(file_map)
    
    # Select relevant columns and reset index
    return df_data[['file_id', 'file', 'nodeid', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']].reset_index(drop=True)

def get_unit_vectors(origin, point):
    """
    Compute unit vector from origin to a given point.
    
    Translates the vector, computes its magnitude, and returns direction cosines rounded to 8 decimals.
    
    Args:
        origin (list): 3D origin point [ox, oy, oz].
        point (list): 3D target point [px, py, pz].
    
    Returns:
        list: Unit vector components [ux, uy, uz].
    """
    translated = [point[i] - origin[i] for i in range(3)]
    magnitude = sqrt(sum(v ** 2 for v in translated))
    if magnitude == 0:
        raise ValueError("Cannot compute unit vector: magnitude is zero")
    return [round(v / magnitude, 8) for v in translated]

def cross_product(a, b):
    """
    Compute the cross product of two 3D vectors.
    
    Returns components rounded to 8 decimals.
    
    Args:
        a (list): Vector [ax, ay, az].
        b (list): Vector [bx, by, bz].
    
    Returns:
        list: Cross product [ix, jy, kz].
    """
    return [
        round(a[1] * b[2] - a[2] * b[1], 8),
        round(a[2] * b[0] - a[0] * b[2], 8),
        round(a[0] * b[1] - a[1] * b[0], 8)
    ]

def normalize(vector):
    """
    Normalize a 3D vector to unit length.
    
    Computes magnitude and divides components, rounding to 8 decimals.
    
    Args:
        vector (list): [vx, vy, vz].
    
    Returns:
        list: Normalized vector.
    """
    magnitude = sqrt(sum(i ** 2 for i in vector))
    if magnitude == 0:
        raise ValueError("Cannot normalize zero vector")
    return [round(i / magnitude, 8) for i in vector]

def lcs_transform(vector_gcs, origin, z_point, x_point):
    """
    Transform a 3D vector from Global Coordinate System (GCS) to Local Coordinate System (LCS).
    
    Computes direction cosines for x, y (via cross product), z axes, then projects the input vector.
    
    Args:
        vector_gcs (list): GCS vector [vx, vy, vz].
        origin (list): LCS origin.
        z_point (list): Point defining z-axis.
        x_point (list): Point defining x-axis.
    
    Returns:
        list: Transformed vector in LCS [lx, ly, lz].
    """
    z_cosines = get_unit_vectors(origin, z_point)
    x_cosines = get_unit_vectors(origin, x_point)
    
    # Compute y cosines as cross product of z and x, then normalize
    y_cosines_raw = cross_product(z_cosines, x_cosines)
    y_cosines = normalize(y_cosines_raw)
    
    # Project vector onto LCS axes
    return [
        round(sum(vector_gcs[i] * x_cosines[i] for i in range(3)), 8),
        round(sum(vector_gcs[i] * y_cosines[i] for i in range(3)), 8),
        round(sum(vector_gcs[i] * z_cosines[i] for i in range(3)), 8)
    ]

def transform_to_lcs(gcs_data, origin, z_point, x_point):
    """
    Apply LCS transformation to all rows in the GCS DataFrame for forces and moments.
    
    Uses pandas apply for row-wise transformation.
    
    Args:
        gcs_data (pd.DataFrame): Data with GCS forces/moments.
        origin, z_point, x_point: LCS definition points.
    
    Returns:
        pd.DataFrame: Transformed data with LCS forces/moments.
    """
    def transform_row(row):
        f_gcs = [row['Fx'], row['Fy'], row['Fz']]
        m_gcs = [row['Mx'], row['My'], row['Mz']]
        f_lcs = lcs_transform(f_gcs, origin, z_point, x_point)
        m_lcs = lcs_transform(m_gcs, origin, z_point, x_point)
        return pd.Series(f_lcs + m_lcs, index=['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
    
    lcs_df = gcs_data.apply(transform_row, axis=1)
    return pd.concat([gcs_data[['file_id', 'file', 'nodeid']], lcs_df], axis=1)

def get_max_df(lcs_data):
    """
    Compute maximum values per component (Fx, Fy, etc.) for each unique nodeid.
    
    Uses groupby and idxmax for efficiency, including the file_id of the max value.
    
    Args:
        lcs_data (pd.DataFrame): LCS-transformed data.
    
    Returns:
        pd.DataFrame: Max values with columns like 'nodeid', 'max_Fx_file', 'max_Fx_value', etc.
    """
    components = ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']
    unique_nodes = lcs_data['nodeid'].unique()
    max_data = {'nodeid': unique_nodes}
    
    for comp in components:
        # Find index of max per node, then extract file_id and value
        idx = lcs_data.groupby('nodeid')[comp].idxmax()
        max_rows = lcs_data.loc[idx]
        max_data[f'max_{comp}_file'] = max_rows['file_id'].values
        max_data[f'max_{comp}_value'] = max_rows[comp].values
    
    return pd.DataFrame(max_data).sort_values('nodeid').reset_index(drop=True)

def export_df(ref_df, lcs_data, max_df):
    # Define output directory (customize this path if needed)
    output_dir = env.output_dir  # e.g., "results/" or an absolute path

    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Export DataFrames to CSV
    ref_df.to_csv(os.path.join(output_dir, 'ref_file_map.csv'), index=False)
    lcs_data.to_csv(os.path.join(output_dir, 'lcs_transformed_data.csv'), index=False)
    max_df.to_csv(os.path.join(output_dir, 'max_values_per_node.csv'), index=False)



if __name__ == '__main__':
    # Apply pandas display options for full output visibility
    for opt, val in PD_DISPLAY_OPTIONS.items():
        pd.set_option(opt, val)
    
    # Optional: Clear terminal (remove if not needed in all environments)
    os.system('clear')
    
    # Load data
    gcs_data = get_vector_data()
    origin, z_point, x_point = get_lcs_def_data()
    
    # Transform to LCS
    lcs_data = transform_to_lcs(gcs_data, origin, z_point, x_point)
    
    # Compute max values per node
    max_df = get_max_df(lcs_data)

    # reference dataframe that maps file_id to file location 
    ref_df = gcs_data[['file_id', 'file']].drop_duplicates(subset='file_id').reset_index(drop=True)



    
    # Print results (usage: replace with saving to file or further processing if needed)
    print("File IDs")
    print(ref_df)
    print("LCS Transformed Data:")
    print(lcs_data)
    print("\nMax Values per Node:")
    print(max_df)


    export_df(ref_df, lcs_data, max_df)

