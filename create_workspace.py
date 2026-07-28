from pathlib import Path

from var import ROOT_PATH

# Folder structure to create
FOLDERS = [
    "Projects/Web",
    "Projects/Mobile",
    "Projects/Desktop",
    "Projects/APIs",
    "Projects/Automation",
    "Projects/AI",
    "Projects/Libraries",
    "Projects/ReverseEngineering",
    "Archives",
    "Templates",
]

for folder in FOLDERS:
    (Path(ROOT_PATH) / folder).mkdir(parents=True, exist_ok=True)

print("Folder structure created successfully.")
