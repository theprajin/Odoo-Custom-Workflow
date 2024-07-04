import json
from pathlib import Path

from odoo import modules


def from_json_file():

    # Get the module path
    module_path = modules.get_module_path("accounting_app")
    # Path to your JSON file
    file_path = Path(module_path) / "demo/example.json"

    # Open the file in read mode
    with open(file_path, "r") as f:
        # Read the entire content of the file
        json_data = f.read()

    # Parse the JSON string into a Python object
    data = json.loads(json_data)

    print(data["id"])

    return data
