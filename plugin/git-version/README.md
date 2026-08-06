# git-version.cmd

This script is used to automatically create Git commits with incrementing version numbers.

## Usage

1. Run the script from the Git repository directory.
2. If the repository has not been initialized, the script will automatically execute `git init`.
3. The script searches for the latest commit using the `vN` format (for example, `v1`, `v2`) and determines the next available version number.
4. It then:
   - stages all changes,
   - creates a new commit with the message `vN`,
   - displays a success message when the commit is completed.

### Example

Run the script from Command Prompt:

```cmd
git-version.cmd
```

### Notes

- Make sure Git is installed and available in your system's PATH.
- This script is intended for use in Windows environments.
