@echo off
title ÂáæÏ Èå íÊåÇÈ

echo ========================================
echo    ÂáæÏ Ñæå Èå íÊåÇÈ
echo ========================================
echo.

cd /d "%~dp0"

where git >nul 2>nul
if %errorlevel% neq 0 (
    echo Git äÕÈ äíÓÊ!
    pause
    exit /b
)

git config --global user.email "kakasangi2007@gmail.com"
git config --global user.name "kakasangi2007-ui"

git remote add origin https://github.com/kakasangi2007-ui/Vpn.git 2>nul
git branch -M main
git add .
git commit -m "ÂáæÏ Ñæå" --no-edit
git pull origin main --allow-unrelated-histories --no-edit
git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ? ÂáæÏ ãæİŞ! ÈÑæ Èå Actions
) else (
    echo ? ÎØÇ
)
pause