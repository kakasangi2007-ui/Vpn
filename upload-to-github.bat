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

echo [1/7] Git äÕÈ ÇÓÊ. ÇÏÇãå ãíÏåíã...
echo.

:: ÊäÙíã åæíÊ ˜ÇÑÈÑ (ãåã!)
echo [2/7] ÊäÙíã åæíÊ ˜ÇÑÈÑ ÈÑÇí git...
git config --global user.email "kakasangi2007@gmail.com"
git config --global user.name "kakasangi2007-ui"
echo.

:: ÑÇåÇäÏÇÒí git
echo [3/7] ÏÑ ÍÇá ÑÇåÇäÏÇÒí git...
git init
echo.

:: ÊäÙíã remote
echo [4/7] ÇÊÕÇá Èå ãÎÒä íÊåÇÈ...
git remote add origin https://github.com/kakasangi2007-ui/Vpn.git 2>nul
if %errorlevel% neq 0 (
    echo ŞÈáÇğ remote ÊäÙíã ÔÏå¡ ÈåÑæÒÑÓÇäí ãíÔæÏ...
    git remote set-url origin https://github.com/kakasangi2007-ui/Vpn.git
)
echo.

:: ÇİÒæÏä åãå İÇíáåÇ
echo [5/7] ÇİÒæÏä åãå İÇíáåÇ Èå git...
git add .
echo.

:: ˜ÇãíÊ ˜ÑÏä (ÈÇ íÇã)
echo [6/7] ËÈÊ ÊÛííÑÇÊ...
git commit -m "ÂáæÏ Ñæå VPN"
echo.

:: æÔ Èå íÊåÇÈ
echo [7/7] ÇÑÓÇá Èå íÊåÇÈ...
echo.

git push -u origin main

echo.
echo ========================================
if %errorlevel% equ 0 (
    echo ? ÂáæÏ ÈÇ ãæİŞíÊ ÇäÌÇã ÔÏ!
    echo.
    echo ÍÇáÇ ÈÑæ Èå:
    echo https://github.com/kakasangi2007-ui/Vpn
    echo.
    echo ÓÓ ÊÈ Actions Ñæ ÈÒä æ Run workflow Ñæ ˜áí˜ ˜ä.
) else (
    echo ? ÎØÇíí ÑÎ ÏÇÏ.
    echo.
    echo ÇÑ ÎØÇ İÊ "failed to push some refs"¡
    echo Çæá Çíä ÏÓÊæÑ Ñæ Êæ ÊÑãíäÇá ÈÒä:
    echo git pull --rebase origin main
    echo.
    echo ÓÓ ÏæÈÇÑå İÇíá bat Ñæ ÇÌÑÇ ˜ä.
)
echo ========================================
pause