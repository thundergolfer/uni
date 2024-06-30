"""
Execute the computers-are-fast benchmarks in Modal to gather data
from the Modal runtime. Allows easily gathering data across Python
versions and cloud provider.
"""
import json
import os
import pathlib

import modal

image = modal.Image.debian_slim(python_version="3.11")
app = modal.App("computers-are-fast", image=image)

import main

@app.function(mounts=[modal.Mount.from_local_file(
    local_path="./message.json",
    remote_path="/root/message.json",
)])
def run():
    cloud_provider = os.environ["MODAL_CLOUD_PROVIDER"]
    print(f"{cloud_provider=}")
    main.main()
    print(json.dumps(pathlib.Path("out.json").read_text()))
