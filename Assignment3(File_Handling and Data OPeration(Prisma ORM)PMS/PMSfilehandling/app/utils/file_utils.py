import pandas as pd
from io import StringIO

def read_csv_to_dicts(file):
    """Reads uploaded CSV file and returns list of dict records."""
    content = file.file.read().decode('utf-8')
    df = pd.read_csv(StringIO(content))
    return df.to_dict(orient='records')

def export_to_csv(data):
    """Converts list of dicts into a CSV stream (for download)."""
    df = pd.DataFrame(data)
    output = StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output
