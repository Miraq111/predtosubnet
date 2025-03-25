from typing import Literal, Any
import datetime
import csv
from datetime import datetime, timedelta, timezone
import random
import subprocess
import os
import codecs
import re

def iso_timestamp_now() -> str:
    """Returns the current timestamp in ISO format with UTC timezone."""
    now = datetime.now(tz=timezone.utc)
    iso_now = now.isoformat()
    return iso_now

def log(
    msg: str,
    *values: object,
    sep: str | None = " ",
    end: str | None = "\n",
    file: Any | None = None,
    flush: Literal[False] = False,
):
    """Custom logging function with timestamp."""
    print(
        f"[{iso_timestamp_now()}] " + msg,
        *values,
        sep=sep,
        end=end,
        file=file,
        flush=flush,
    )

def export_to_csv(data, filename):
    """
    Exports data to a CSV file.

    Args:
        data: List of data (dict) to export.
        filename: The filename to save the data as CSV.
    """
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['time', 'category', 'amount', 'open', 'high', 'low', 'close'])

            for item in data:
                time = item.get('timestamp', 'N/A')
                category = item.get('category', 'UNKNOWN')
                amount = item.get('amount', 'N/A')
                open_price = item.get('open', 'N/A')
                high_price = item.get('high', 'N/A')
                low_price = item.get('low', 'N/A')
                close_price = item.get('close', 'N/A')

                writer.writerow([time, category, amount, open_price, high_price, low_price, close_price])
    except Exception as e:
        log(f"Error exporting to CSV: {e}")

def dateToTimestamp(date_string: str) -> float:
    """
    Converts a formatted date string (YYYY-MM-DD.HH:MM:SS) into a Unix timestamp.

    Args:
        date_string (str): The formatted date string.
    
    Returns:
        float: The Unix timestamp.
    """
    formatted_date_string = date_string.replace('h', ':').replace('m', ':').replace('s', '').replace('.', '-')
    date_format = "%Y-%m-%d.%H:%M:%S"
    date_object = datetime.strptime(formatted_date_string, date_format)
    return date_object.timestamp()

def get_random_future_timestamp(hours_ahead=8) -> int:
    """
    Returns a random future timestamp within a given range of hours ahead.

    Args:
        hours_ahead (int): The range in hours for the random future timestamp.

    Returns:
        int: The generated future timestamp.
    """
    now = datetime.now()
    random_seconds = random.randint(60, hours_ahead * 3600)
    random_future_timestamp = now + timedelta(seconds=random_seconds)
    timestamp = int(round(random_future_timestamp.timestamp()))
    return timestamp

def update_repository():
    """Updates the repository and re-installs the package if the version has changed."""
    print("Checking repository updates...")
    try:
        subprocess.run(["git", "pull"], check=True)
    except subprocess.CalledProcessError as e:
        log(f"Git pull failed: {e}")
        return False

    here = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(here)
    init_file_path = os.path.join(parent_dir, 'prediction/__init__.py')
    
    try:
        with codecs.open(init_file_path, encoding='utf-8') as init_file:
            version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", init_file.read(), re.M)
            if version_match:
                new_version = version_match.group(1)
                log(f"Current version: {prediction.__version__}, New version: {new_version}")
                if prediction.__version__ != new_version:
                    subprocess.run(["python3", "-m", "pip", "install", "-e", "."], check=True)
                    os._exit(1)
            else:
                log("No version changes detected.")
    except FileNotFoundError as e:
        log(f"Error reading version file: {e}")
        return False
