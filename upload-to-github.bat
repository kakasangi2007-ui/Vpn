@echo off
title ÂáæÏ ÎæÏ˜ÇÑ Ñæå Èå íÊåÇÈ

echo ========================================
echo    ÂáæÏ Ñæå Èå íÊåÇÈ
echo    ÓÇÎÊå ÔÏå ÈÑÇí Alireza
echo ========================================
echo.

cd /d "%~dp0"

where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ÎØÇ] Git äÕÈ äíÓÊ!
    echo áØİÇğ ÇÈÊÏÇ Git Ñæ ÇÒ https://git-scm.com/download/win äÕÈ ˜ä.
    pause
    exit /b
)

echo [1/8] Git äÕÈ ÇÓÊ. ÇÏÇãå ãíÏåíã...
echo.

:: ÊäÙíã åæíÊ ˜ÇÑÈÑ
echo [2/8] ÊäÙíã åæíÊ ˜ÇÑÈÑ ÈÑÇí git...
git config --global user.email "kakasangi2007@gmail.com"
git config --global user.name "kakasangi2007-ui"
echo.

:: ÑÇåÇäÏÇÒí git
echo [3/8] ÏÑ ÍÇá ÑÇåÇäÏÇÒí git...
git init
echo.

:: ÊäÙíã remote
echo [4/8] ÇÊÕÇá Èå ãÎÒä íÊåÇÈ...
git remote add origin https://github.com/kakasangi2007-ui/Vpn.git 2>nul
if %errorlevel% neq 0 (
    echo ŞÈáÇğ remote ÊäÙíã ÔÏå¡ ÈåÑæÒÑÓÇäí ãíÔæÏ...
    git remote set-url origin https://github.com/kakasangi2007-ui/Vpn.git
)
echo.

:: ÊÛííÑ äÇã ÔÇÎå Èå main
echo [5/8] ÊÛííÑ ÔÇÎå Èå main...
git branch -M main
echo.

:: ÇİÒæÏä åãå İÇíáåÇ
echo [6/8] ÇİÒæÏä åãå İÇíáåÇ Èå git...
git add .
echo.

:: ˜ÇãíÊ ˜ÑÏä
echo [7/8] ËÈÊ ÊÛííÑÇÊ...
git commit -m "ÂáæÏ Ñæå VPN"
echo.

:: æÔ Èå íÊåÇÈ (ÔÇÎå main)
echo [8/8] ÇÑÓÇá Èå íÊåÇÈ (ÔÇÎå main)...
echo.

git pull origin main --allow-unrelated-histories
git push -u origin main

echo.
echo ========================================
if %errorlevel% equ 0 (
    echo ? ÂáæÏ ÈÇ ãæİŞíÊ ÇäÌÇã ÔÏ!
    echo.
    echo ÈÑæ Èå: https://github.com/kakasangi2007-ui/Vpn
    echo ÓÓ ÊÈ Actions Ñæ ÈÒä æ Run workflow Ñæ ˜áí˜ ˜ä.
) else (
    echo ? ÎØÇíí ÑÎ ÏÇÏ.
    echo.
    echo ÇÑ ÎØÇ İÊ "failed to push some refs":
    echo git pull --rebase origin main
    echo.
    echo ÓÓ ÏæÈÇÑå bat Ñæ ÇÌÑÇ ˜ä.
)
echo ========================================
pause