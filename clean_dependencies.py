import os

from send2trash import send2trash

# Root directory containing project categories
ROOT_PATH = r"YOUR-ROOT-FOLDER"

# Auto add Projects template folder
ROOT_PATH = os.path.join(ROOT_PATH, "Projects")

# Dependency/cache folders that are safe to move to Recycle Bin
FOLDERS_TO_DELETE = {
    "node_modules",
    "vendor",
    ".pnpm-store",
    ".npm",
    ".yarn",
    ".cache",
    ".parcel-cache",
    ".turbo",
    ".wrangler",
}


# Projects to exclude (relative to Projects folder)
EXCLUDED_PATHS = []


# Convert excluded paths to absolute normalized paths
EXCLUDED_PATHS = {os.path.normpath(os.path.join(ROOT_PATH, path)).lower() for path in EXCLUDED_PATHS}


def is_excluded(project_path: str) -> bool:
    """
    Check whether project should be skipped.
    """
    return os.path.normpath(project_path).lower() in EXCLUDED_PATHS


def get_folder_size(folder_path: str) -> int:
    """
    Calculate folder size.
    """
    total_size = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            try:
                total_size += os.path.getsize(os.path.join(root, file))
            except Exception:
                pass

    return total_size


def format_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format.
    """
    size = float(size_bytes)

    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


def find_cleanup_targets():
    """
    Scan:
    Projects
      └── Category
          └── Project
              └── dependency folder

    Only checks direct project children.
    """

    targets = []

    if not os.path.isdir(ROOT_PATH):
        return targets

    for category in os.listdir(ROOT_PATH):

        category_path = os.path.join(ROOT_PATH, category)

        if not os.path.isdir(category_path):
            continue

        for project in os.listdir(category_path):

            project_path = os.path.join(category_path, project)

            if not os.path.isdir(project_path):
                continue

            if is_excluded(project_path):
                print(f"[SKIPPED] {project_path}")
                continue

            for dependency in FOLDERS_TO_DELETE:

                dependency_path = os.path.join(project_path, dependency)

                if os.path.isdir(dependency_path):
                    targets.append(dependency_path)

    return targets


def main():

    print("=" * 80)
    print("PROJECT DEPENDENCY CLEANER")
    print("=" * 80)

    print(f"Root: {ROOT_PATH}")
    print()

    targets = find_cleanup_targets()

    if not targets:
        print("No dependency folders found.")
        return

    total_size = 0

    print("\nFolders to move to Recycle Bin:\n")

    for folder in targets:

        size = get_folder_size(folder)

        total_size += size

        print(folder)
        print(f"  Size: {format_size(size)}")
        print()

    print("-" * 80)
    print(f"Folders Found : {len(targets)}")
    print(f"Space To Free : {format_size(total_size)}")
    print("-" * 80)

    confirm = input("\nMove these folders to Recycle Bin? (y/n): ").strip().lower()

    if confirm != "y":

        print("Operation cancelled.")
        return

    moved_size = 0

    print("\nMoving folders...\n")

    for folder in targets:

        try:

            size = get_folder_size(folder)

            # Safe delete Recycle Bin
            send2trash(folder)

            moved_size += size

            print(f"[MOVED] {folder}")

        except Exception as e:

            print(f"[FAILED] {folder}")
            print(f"         {e}")

    print("\n" + "=" * 80)
    print("CLEANUP COMPLETED")
    print(f"Moved To Recycle Bin: {format_size(moved_size)}")
    print("=" * 80)


if __name__ == "__main__":
    main()
