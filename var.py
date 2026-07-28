# Root directory containing project categories
ROOT_PATH = r"your\workspace\root\path"

# Dependency/cache folders that are safe to move to Recycle Bin
FOLDERS_TO_DELETE = {
    "__pycache__",
    ".cache",
    ".npm",
    ".parcel-cache",
    ".pnpm-store",
    ".turbo",
    ".venv",
    ".wrangler",
    ".yarn",
    "dist",
    "node_modules",
    "vendor",
}

# Projects to exclude (relative to the Projects folder)
EXCLUDED_PATHS = [
    r"your\excluded\project\path1",
    r"your\excluded\project\path2",
]
