@echo off
title SchemeSathi Master Launcher
echo ===================================================
echo       Launching SchemeSathi Full-Stack Project
echo ===================================================

:: Check if port 8080 is busy and kill it if needed
echo [1/3] Checking backend port 8080...
powershell -NoProfile -Command "try { $proc = (Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue).OwningProcess; if ($proc) { Stop-Process -Id $proc -Force; Write-Host 'Released stale port 8080 process.' } } catch {}"

:: Launch Backend in separate window
echo [2/3] Starting Java Backend REST API Server (:8080)...
start "SchemeSathi Backend API (:8080)" cmd /k "java -jar target\schemesathi-1.0.0-jar-with-dependencies.jar --server --port 8080"

:: Launch Frontend in separate window
echo [3/3] Starting React Vite Frontend (:5173)...
start "SchemeSathi React Frontend (:5173)" cmd /k "cd frontend && npm run dev"

:: Wait 3 seconds and launch browser
timeout /t 3 /nobreak >nul
echo Opening SchemeSathi in your default browser...
start http://localhost:5173

echo ===================================================
echo [SUCCESS] Both Backend and Frontend are now running!
echo User App:      http://localhost:5173
echo Admin Console: http://localhost:5173/#/admin
echo ===================================================
