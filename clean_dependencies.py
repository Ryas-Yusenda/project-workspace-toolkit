import os
import shutil

# Root directory containing project categories
ROOT_PATH = r"YOUR-PROJECT_FOLDER"

# Dependency/cache folders that are safe to remove
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

# Projects to exclude (relative to ROOT_PATH)
EXCLUDED_PATHS = [
]

# Convert excluded paths to absolute normalized paths
EXCLUDED_PATHS = {
    os.path.normpath(os.path.join(ROOT_PATH, path)).lower()
    for path in EXCLUDED_PATHS
}


def is_excluded(project_path: str) -> bool:
    """
    Check whether a project should be skipped.
    """
    return os.path.normpath(project_path).lower() in EXCLUDED_PATHS


def get_folder_size(folder_path: str) -> int:
    """
    Calculate folder size in bytes.
    """
    total_size = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            try:
                total_size += os.path.getsize(
                    os.path.join(root, file)
                )
            except Exception:
                pass

    return total_size


def format_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format.
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024

    return f"{size_bytes:.2f} PB"


def find_cleanup_targets():
    """
    Scan only:
    Category -> Project

    Example:
    APIs/cloudflare-api-proxy/node_modules

    It will NOT scan deeper nested projects.
    """
    targets = []

    if not os.path.isdir(ROOT_PATH):
        return targets

    # First level: categories
    for category in os.listdir(ROOT_PATH):

        category_path = os.path.join(ROOT_PATH, category)

        if not os.path.isdir(category_path):
            continue

        # Second level: projects
        for project in os.listdir(category_path):

            project_path = os.path.join(category_path, project)

            if not os.path.isdir(project_path):
                continue

            if is_excluded(project_path):
                print(f"[SKIPPED] {project_path}")
                continue

            # Check only direct children of project root
            for dependency in FOLDERS_TO_DELETE:

                dependency_path = os.path.join(
                    project_path,
                    dependency
                )

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

    print("\nFolders to delete:\n")

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

    confirm = input(
        "\nProceed with deletion? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Operation cancelled.")
        return

    deleted_size = 0

    print("\nDeleting folders...\n")

    for folder in targets:

        try:
            size = get_folder_size(folder)

            shutil.rmtree(folder)

            deleted_size += size

            print(f"[OK] {folder}")

        except Exception as e:
            print(f"[FAILED] {folder}")
            print(f"         {e}")

    print("\n" + "=" * 80)
    print("CLEANUP COMPLETED")
    print(f"Recovered Space: {format_size(deleted_size)}")
    print("=" * 80)


if __name__ == "__main__":
    main()