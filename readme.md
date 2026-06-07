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
Includes workspace bootstrapping and safe dependency cleanup tools for developers managing multiple projects.
</p>

## 🧐 About

Project Workspace Toolkit is a lightweight collection of Python utilities designed to help developers manage large local project collections.

The toolkit currently provides two utilities:

- **create_workspace.py** — Generates a standardized workspace structure for organizing projects.
- **clean_dependencies.py** — Scans projects and moves dependency/cache directories to Recycle Bin to safely reclaim disk space.

## ✨ Features

- Create a standardized project workspace
- Organize projects by category
- Clean dependency and cache folders safely
- Move deleted folders to Windows Recycle Bin
- Prevent permanent deletion
- Preview disk usage before cleanup
- Exclude active projects from cleanup
- Fast scanning without traversing deep nested directories

## 🏁 Getting Started

### Prerequisites

- Python 3.10+
- Windows (for Recycle Bin support)

### Install Dependency

Install required package:

```bash
pip install send2trash
```
