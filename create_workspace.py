from pathlib import Path

# Root workspace location
ROOT_PATH = r"YOUR-PROJECT_FOLDER"

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
    (Path(ROOT_PATH) / folder).mkdir(
        parents=True,
        exist_ok=True
    )

print("Folder structure created successfully.")