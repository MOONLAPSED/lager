@echo off

:: Add Scoop to PATH for this session
set PATH=%PATH%;C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Scoop\bin

:: Introduce a delay of 3 seconds
ping 127.0.0.1 -n 4 > nul

:: Check if Scoop is in the PATH
echo %PATH% | findstr /i /c:"C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Scoop\bin" > nul

IF %ERRORLEVEL% EQU 0 (
    echo Scoop is in the PATH.
) ELSE (
    echo Scoop is not in the PATH. Please check the installation.
    goto :retry
)

:: Invoke the PowerShell script without user input
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "C:\Users\WDAGUtilityAccount\Desktop\lager.ps1"

IF %ERRORLEVEL% NEQ 0 (
    echo There was an error executing the PowerShell script.
    goto :retry
)

echo Initialization completed successfully.
goto :EOF

:retry
:: Retry logic
echo Retrying...
ping 127.0.0.1 -n 4 > nul
goto :EOF

pause
