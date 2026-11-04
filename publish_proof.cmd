@echo off
REM Publish everything in this folder to GitHub Pages. Run from this folder.
cd /d "%~dp0"
git add -A
git commit -m "proof: %date% %time%"
git push
echo.
echo Live in about a minute at https://proofs.mtdcnc.com/proofs/<filename>
pause
