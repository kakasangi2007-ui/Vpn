@echo off
title ÂáæÏ ÎæÏ˜ÇÑ Ñæå Èå íÊåÇÈ

echo ========================================
echo    ÂáæÏ Ñæå Èå íÊåÇÈ
echo    ÓÇÎÊå ÔÏå ÈÑÇí Alireza
echo ========================================
echo.

cd /d "%~dp0"

:: ˜ ˜ÑÏä Git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ÎØÇ] Git äÕÈ äíÓÊ!
    echo áØİÇğ Git Ñæ ÇÒ https://git-scm.com/download/win äÕÈ ˜ä.
    pause
    exit /b
)

:: ÊäÙíã åæíÊ
echo [1/8] ÊäÙíã åæíÊ ˜ÇÑÈÑ...
git config --global user.email "kakasangi2007@gmail.com"
git config --global user.name "kakasangi2007-ui"
echo.

:: ÑÇåÇäÏÇÒí git
echo [2/8] ÑÇåÇäÏÇÒí git...
git init
echo.

:: ÊäÙíã remote
echo [3/8] ÇÊÕÇá Èå íÊåÇÈ...
git remote add origin https://github.com/kakasangi2007-ui/Vpn.git 2>nul
if %errorlevel% neq 0 (
    git remote set-url origin https://github.com/kakasangi2007-ui/Vpn.git
)
echo.

:: ÊÛííÑ Èå ÔÇÎå main
echo [4/8] ÊÛííÑ Èå ÔÇÎå main...
git branch -M main
echo.

:: ÇİÒæÏä İÇíáåÇ
echo [5/8] ÇİÒæÏä İÇíáåÇ...
git add .
echo.

:: ˜ÇãíÊ ÈÇ íÇã ÎæÏ˜ÇÑ (ÈÏæä ÈÇÒ ÔÏä æíÑÇíÔÑ)
echo [6/8] ËÈÊ ÊÛííÑÇÊ...
git commit -m "ÂáæÏ Ñæå VPN" --no-edit
echo.

:: ÏÑíÇİÊ ÊÛííÑÇÊ ÇÒ íÊåÇÈ (ÈÇ Íá ÎæÏ˜ÇÑ)
echo [7/8] åãÇãÓÇÒí ÈÇ íÊåÇÈ...
git pull origin main --allow-unrelated-histories --no-edit
echo.

:: ÇÑÓÇá Èå íÊåÇÈ
echo [8/8] ÇÑÓÇá Èå íÊåÇÈ...
git push -u origin main

echo.
echo ========================================
if %errorlevel% equ 0 (
    echo ? ÂáæÏ ãæİŞ ÈæÏ!
    echo.
    echo ÈÑæ Èå: https://github.com/kakasangi2007-ui/Vpn
    echo ÓÓ ÊÈ Actions -^> Run workflow
) else (
    echo ? ÎØÇ ÑÎ ÏÇÏ. íÇã Ñæ ÈÎæä.
)
echo ========================================
pause