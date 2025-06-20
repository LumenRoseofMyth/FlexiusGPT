@echo off
echo Checking module compliance...

REM For each module, check that schema.md exists and print module_name and module_id

for /D %%F in (..\modules\*) do (
    if exist "%%F\schema.md" (
        echo.
        echo Found: %%F\schema.md
        for /f "delims=" %%A in ('findstr /B /C:"module_name:" "%%F\schema.md"') do echo   %%A
        for /f "delims=" %%B in ('findstr /B /C:"module_id:" "%%F\schema.md"') do echo   %%B
    ) else (
        echo.
        echo ERROR: Missing schema.md in %%F
    )
)
echo.
echo Compliance check complete.
pause
