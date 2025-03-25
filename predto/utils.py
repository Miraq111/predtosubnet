from typing import Literal, Any
import datetime
import csv
from datetime import datetime, timedelta, timezone
import random
import subprocess
import os
import codecs
import re
import prediction

def iso_timestamp_now() -> str:
    """Returns the current timestamp in ISO format (UTC)."""
    now = datetime.now(tz=timezone.utc)
    return now.isoformat()

def log(
    msg: str,
    *values: object,
    sep: str = " ",
    end: str = "\n",
    file: Any = None,
    flush: bool = False,
):
    """Logs a message with a timestamp."""
    print(
        f"[{iso_timestamp_now()}] {msg}",
        *values,
        sep=sep,
        end=end,
        file=file,
        flush=flush,
    )

def export_to_csv(data, filename):
    """Exports structured data to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'category', 'value'])

        for entry in data:
            timestamp = entry.get('timestamp', iso_timestamp_now())
            category = entry.get('category', 'unknown')
            value = entry.get('value', 'N/A')

            writer.writerow([timestamp, category, value])

def date_to_timestamp(date_string):
    """Converts a formatted date string to a timestamp."""
    formatted_date_string = date_string.replace('h', ':').replace('m', ':').replace('s', '')
    formatted_date_string = formatted_date_string.replace('.', '-')

    date_format = "%Y-%m-%d.%H:%M:%S"
    date_object = datetime.strptime(formatted_date_string, date_format)

    return date_object.timestamp()

def get_random_future_timestamp(hours_ahead=8):
    """Generates a random future timestamp within the next 'hours_ahead' hours."""
    now = datetime.now()
    random_seconds = random.randint(60, hours_ahead * 3600)
    future_timestamp = now + timedelta(seconds=random_seconds)
    
    return int(round(future_timestamp.timestamp()))

def update_repository():
    """Checks for repository updates and installs them if necessary."""
    print("Checking for repository updates...")
    try:
        subprocess.run(["git", "pull"], check=True)
    except subprocess.CalledProcessError:
        print("Git pull failed.")
        return False

    here = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(here) 
    init_file_path = os.path.join(parent_dir, 'prediction/__init__.py')

    with codecs.open(init_file_path, encoding='utf-8') as init_file:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", init_file.read(), re.M)
        if version_match:
            new_version = version_match.group(1)
            print(f"Current version: {prediction.__version__}, New version: {new_version}")
            if prediction.__version__ != new_version:
                try:
                    subprocess.run(["python3", "-m", "pip", "install", "-e", "."], check=True)
                    os._exit(1)
                except subprocess.CalledProcessError:
                    print("Pip install failed.")
        else:
            print("No changes detected!")
