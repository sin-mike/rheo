import pandas as pd
from serial.tools import list_ports

def list_devices() -> pd.DataFrame:
    """
    Lists all connected devices.

    Returns:
        pd.DataFrame: A DataFrame containing details of all connected devices.
    """
    df_ports = pd.DataFrame([c.__dict__ for c in list_ports.comports()])
    return df_ports

if __name__ == "__main__":
    print(list_devices())