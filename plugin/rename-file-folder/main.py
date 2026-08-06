import argparse
import ctypes
import re
import sys
from pathlib import Path

FILE_ATTRIBUTE_HIDDEN = 0x2
FILE_ATTRIBUTE_SYSTEM = 0x4


def is_hidden_or_system(path: Path) -> bool:
    """
    Return True if path is hidden or system.
    """

    if path.name.startswith("."):
        return True

    if not hasattr(ctypes, "windll"):
        return False

    attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))

    if attrs == -1:
        return False

    return bool(attrs & FILE_ATTRIBUTE_HIDDEN or attrs & FILE_ATTRIBUTE_SYSTEM)


def split_words(name: str) -> list[str]:
    """
    Split filename into words.

    Example:
        helloWorld -> hello world
        hello_world -> hello world
        hello-world -> hello world
    """

    name = re.sub(r"[_\-]+", " ", name)

    name = re.sub(
        r"([a-z0-9])([A-Z])",
        r"\1 \2",
        name,
    )

    words = re.findall(r"[A-Za-z0-9]+", name)

    return [w.lower() for w in words]


def camel(words):
    """Convert to a string with the separators denoted by having the next letter capitalised"""
    if not words:
        return ""
    return words[0] + "".join(w.capitalize() for w in words[1:])


def pascal(words):
    """Convert to a string denoted in the same fashion as camelCase, but with the first letter also capitalised"""
    return "".join(w.capitalize() for w in words)


def snake(words):
    """Convert to a lower case, underscore separated string."""
    return "_".join(words).lower()


def constant(words):
    """Convert to an upper case, underscore separated string."""
    return "_".join(words).upper()


def kebab(words):
    """Convert to a lower case, dash separated string (alias for param case)."""
    return "-".join(words).lower()


def dot(words):
    """Convert to a lower case, period separated string."""
    return ".".join(words).lower()


def sentence(words):
    """Convert to a lower case, space separated string."""
    return " ".join(words).lower()


def title(words):
    """Convert to a space separated string with the first character of every word upper cased"""
    return " ".join(w.capitalize() for w in words)


def lower(words):
    """Convert to a string in lower case"""
    return " ".join(words)


def upper(words):
    """Convert to a string in upper case"""
    return " ".join(words).upper()


CASE_MAP = {
    "camel": camel,
    "pascal": pascal,
    "snake": snake,
    "constant": constant,
    "kebab": kebab,
    "dot": dot,
    "sentence": sentence,
    "title": title,
    "lower": lower,
    "upper": upper,
}


def rename_path(path: Path, style: str, dry_run=False):
    """
    Rename a single file or folder.
    """

    stem = path.stem if path.is_file() else path.name
    suffix = path.suffix if path.is_file() else ""

    words = split_words(stem)
    new_name = CASE_MAP[style](words) + suffix

    if new_name == path.name:
        return

    new_path = path.with_name(new_name)

    if new_path.exists():
        if new_path.name.lower() == path.name.lower():
            temp_path = path.with_name(f"__rename_temp__{path.name}")

            print(f"{path.name} -> {new_name}")

            if not dry_run:
                path.rename(temp_path)
                temp_path.rename(new_path)

            return

        print(f"[SKIP] {path.name} -> {new_name} (already exists)")
        return

    print(f"{path.name} -> {new_name}")

    if not dry_run:
        path.rename(new_path)


def iter_paths(root: Path, recursive: bool):
    if recursive:
        return sorted(root.rglob("*"), key=lambda p: len(p.parts), reverse=True)

    return sorted(root.iterdir(), reverse=True)


ICON_HEX = (
    "hex(2):25,00,53,00,79,00,73,00,74,00,65,00,6d,00,52,00,6f,00,6f,00,74,\\\r\n"
    "  00,25,00,5c,00,53,00,79,00,73,00,74,00,65,00,6d,00,52,00,65,00,73,00,6f,00,\\\r\n"
    "  75,00,72,00,63,00,65,00,73,00,5c,00,69,00,6d,00,61,00,67,00,65,00,72,00,65,\\\r\n"
    "  00,73,00,2e,00,64,00,6c,00,6c,00,2e,00,6d,00,75,00,6e,00,2c,00,31,00,30,00,\\\r\n"
    "  39,00,00,00"
)


def reg_expand_sz(value: str) -> str:
    """
    Convert a string into REG_EXPAND_SZ hex(2) format.
    """
    data = value.encode("utf-16le") + b"\x00\x00"

    hex_bytes = [f"{b:02x}" for b in data]

    lines = []

    while hex_bytes:
        chunk = hex_bytes[:24]
        hex_bytes = hex_bytes[24:]

        text = ",".join(chunk)

        if hex_bytes:
            lines.append(text + ",\\")
        else:
            lines.append(text)

    return "hex(2):" + "\r\n  ".join(lines)


def build_registry_content(script_path: Path) -> str:
    """
    Build a temporary .reg file for the Explorer context menu.
    The command uses the current Python interpreter and the absolute
    location of this script, so it works even if the project is moved.
    """

    python_exe = Path(sys.executable).resolve().with_name("pythonw.exe")
    script_path = script_path.resolve()

    lines = [
        "Windows Registry Editor Version 5.00",
        "",
        r"[HKEY_CLASSES_ROOT\Directory\Background\shell\rename_case]",
        '"SubCommands"=""',
        '"MUIVerb"="Rename Case"',
        f'"Icon"={ICON_HEX}',
        r"[HKEY_CLASSES_ROOT\Directory\Background\shell\rename_case\shell]",
        "",
    ]

    registry_names = {
        "camel": "camelCase",
        "pascal": "PascalCase",
        "snake": "snake_case",
        "constant": "CONSTANT_CASE",
        "kebab": "kebab-case",
        "dot": "dot.case",
        "sentence": "sentence case",
        "title": "Title Case",
        "lower": "lower case",
        "upper": "UPPER CASE",
    }

    for index, (case_name, label) in enumerate(registry_names.items(), start=2):
        key_name = f"Z{index:03d}CMD"
        command = f'"{python_exe}" "{script_path}" --{case_name}'

        lines.extend(
            [
                rf"[HKEY_CLASSES_ROOT\Directory\Background\shell\rename_case\shell\{key_name}]",
                f'"MUIVerb"="{label}"',
                f'"Icon"={ICON_HEX}',
                "",
                rf"[HKEY_CLASSES_ROOT\Directory\Background\shell\rename_case\shell\{key_name}\command]",
                f"@={reg_expand_sz(command)}",
                "",
            ]
        )

    return "\r\n".join(lines).rstrip() + "\r\n"


def install_context_menu(script_path: Path):
    """
    Create a temporary .reg file in the project folder,
    request Administrator privileges, import it into the registry,
    then delete the temporary file.
    """

    if sys.platform != "win32":
        print("This feature is only supported on Windows.")
        return

    reg_path = script_path.parent / "rename_case_context_menu.reg"

    try:
        reg_path.write_text(
            build_registry_content(script_path),
            encoding="utf-8",
        )

        print(f"Temporary registry file: {reg_path}")
        print("Requesting administrator privileges...")

        result = ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            "regedit.exe",
            f'/s "{reg_path}"',
            None,
            1,
        )

        # ShellExecuteW returns a value > 32 on success.
        if result <= 32:
            print(f"Failed to start regedit.exe (ShellExecuteW returned {result}).")
            return

        print("Registry import has been started.")
        print("If the UAC dialog was accepted, the registry was imported successfully.")

    finally:
        if reg_path.exists():
            reg_path.unlink(missing_ok=True)
            print(f"Deleted temporary registry file: {reg_path}")


def main():
    parser = argparse.ArgumentParser(description="Rename files and folders into different naming conventions.")

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursive",
    )

    parser.add_argument(
        "--files",
        action="store_true",
        help="Rename files only",
    )

    parser.add_argument(
        "--dirs",
        action="store_true",
        help="Rename directories only",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview only",
    )

    parser.add_argument(
        "--create-reg",
        action="store_true",
        help="Create a temporary .reg file, import it into Windows Explorer, and delete it automatically.",
    )

    group = parser.add_mutually_exclusive_group(required=False)

    for case in CASE_MAP:
        group.add_argument(
            f"--{case}",
            action="store_true",
        )

    args = parser.parse_args()

    if args.create_reg:
        install_context_menu(Path(__file__).resolve())
        return

    if not any(getattr(args, case) for case in CASE_MAP):
        parser.error(
            "one of the rename modes must be selected: --camel, --pascal, --snake, --constant, --kebab, --dot, --sentence, --title, --lower, --upper"
        )

    root = Path.cwd()

    print(f"Root: {root}")

    if not root.exists():
        print("Path not found.")
        return

    style = next(key for key in CASE_MAP if getattr(args, key))

    for path in iter_paths(root, args.recursive):

        if is_hidden_or_system(path):
            continue

        if args.files and not path.is_file():
            continue

        if args.dirs and not path.is_dir():
            continue

        rename_path(
            path,
            style,
            args.dry_run,
        )


if __name__ == "__main__":
    main()
