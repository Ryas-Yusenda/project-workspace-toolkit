# rename-file-folder

This script is used to rename files and folders into a specific naming convention, such as camelCase, snake_case, or PascalCase.

## Usage

Run the script from the directory containing the files and folders you want to rename.

### Available Options

1. `-r`, `--recursive`
   Rename files and folders recursively, including all subdirectories.

2. `--files`
   Rename files only.

3. `--dirs`
   Rename directories only.

4. `--dry-run`
   Preview the changes without actually renaming any files or folders.

5. `--create-reg`
   Create a temporary `.reg` file, import it into the Windows Explorer registry, and automatically remove it afterward.

### Naming Formats

Choose **one** of the following naming conventions:

- `--camel`
- `--pascal`
- `--snake`
- `--constant`
- `--kebab`
- `--dot`
- `--sentence`
- `--title`
- `--lower`
- `--upper`

### Examples

```cmd
python main.py --snake --recursive
```

```cmd
python main.py --camel --files --dry-run
```

### Notes

- Select only one naming format at a time.
- Use `--dry-run` to preview the changes before applying them.
- This script is primarily intended for Windows environments, especially when using the `--create-reg` option.
