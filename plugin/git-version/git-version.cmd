@echo off
setlocal EnableDelayedExpansion

REM Check if Git is initialized
if not exist ".git" (
    echo Git repository not found.
    echo Initializing Git...

    git init

    if errorlevel 1 (
        echo Failed to initialize Git.
        pause
        exit /b 1
    )

    set "VERSION=1"
) else (
    REM Find latest version from commit messages
    set "VERSION=0"

    for /f "tokens=*" %%A in ('git log --pretty^=format:"%%s" 2^>nul') do (
        set "MSG=%%A"

        if "!MSG:~0,1!"=="v" (
            set "NUM=!MSG:~1!"
            for /f "delims=0123456789" %%B in ("!NUM!") do set "NUM="

            if defined NUM (
                if !NUM! GTR !VERSION! set "VERSION=!NUM!"
            )
        )
    )

    set /a VERSION+=1
)

echo.
echo ==========================
echo Commit version: v%VERSION%
echo ==========================
echo.

git add .

git commit -m "v%VERSION%"

if errorlevel 1 (
    echo.
    echo Commit failed.
    pause
    exit /b 1
)

echo.
echo Successfully committed v%VERSION%.
pause