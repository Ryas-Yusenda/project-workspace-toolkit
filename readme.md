<p align="center">
  <img width="180" height="180" src="https://raw.githubusercontent.com/github/explore/main/topics/python/python.png" alt="Project Workspace Toolkit Logo">
</p>

<h3 align="center">Project Workspace Toolkit</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

---

<p align="center">
Utilities for creating, organizing, and maintaining large local development workspaces.
<br>
Includes workspace bootstrapping and dependency cleanup tools for developers managing multiple projects.
</p>

## 🧐 About

Project Workspace Toolkit is a lightweight collection of Python utilities designed to help developers manage large local project collections.

The toolkit currently provides two utilities:

- **create_workspace.py** — Generates a standardized workspace structure for organizing projects.
- **clean_dependencies.py** — Removes dependency and cache directories from projects to reclaim disk space.

## ✨ Features

- Create a standardized project workspace
- Organize projects by category
- Clean dependency and cache folders
- Preview disk usage before deletion
- Exclude active projects from cleanup
- Fast scanning without traversing deep nested directories
- No external dependencies required

## 🏁 Getting Started

### Prerequisites

- Python 3.10+

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/project-workspace-toolkit.git
cd project-workspace-toolkit
```

## 🎈 Usage

### Configuration

Change this path to your workspace root directory

```python
ROOT_PATH = r"YOUR-PROJECT_FOLDER"
```

Excluding Projects from Cleanup

```python
EXCLUDED_PATHS = [
]
```

### Create Workspace

```bash
python create_workspace.py
```

### Clean Dependencies

```bash
python clean_dependencies.py
```

## 📄 License

[MIT License](LICENSE) – feel free to fork, modify, and use for your own projects.
