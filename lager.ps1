<#
.SYNOPSIS
This script installs and configures various software tools on a Windows virtual machine.

.DESCRIPTION
The script installs tools using Scoop, configures the environment, and launches common applications.

.NOTES
This script requires Scoop to be installed on the system. It is invoked, properly, by the sister-script `lager.bat`.

.EXAMPLE
Run the script during the Windows virtual machine startup process.
#>

# Function to log messages
function Write-Log {
    param (
        [string]$message
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "$timestamp - $message"
    Add-Content -Path "C:\Users\WDAGUtilityAccount\Desktop\logs\scoop_log.txt" -Value "$timestamp - $message"
}

Write-Log "Starting Scoop script execution."

# Function to install and check Scoop
function Install-Scoop {
    if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
        Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')
        Write-Log "Installed Scoop."
    } else {
        Write-Log "Scoop is already installed."
    }
}

# Function to install a package using Scoop
function Install-Package {
    param (
        [string]$packageName
    )
    try {
        if (-not (scoop list $packageName | Select-String $packageName)) {
            scoop install $packageName
            Write-Log "Installed package: $packageName"
        } else {
            Write-Log "Package already installed: $packageName"
        }
    } catch {
        Write-Log "Failed to install package: $packageName. Error: $_"
    }
}

# Add Scoop to PATH for the session
$env:PATH += ";C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Scoop\shims"
Write-Log "Added Scoop to PATH."

# Install Scoop if not already installed
Install-Scoop

# Ensure Git is installed before adding buckets
Install-Package -packageName "git"

# Add necessary buckets
function Add-Bucket {
    param (
        [string]$bucketName
    )
    try {
        scoop bucket add $bucketName
        Write-Log "Added bucket: $bucketName"
    } catch {
        Write-Log "Failed to add bucket: $bucketName. Error: $_"
    }
}

Write-Log "Adding extra buckets."
Add-Bucket -bucketName "nerd-fonts"
Add-Bucket -bucketName "extras"
Add-Bucket -bucketName "versions"

# Install required packages
$packages = @(
    "main/gh",
    "versions/vscode-insiders",
    "versions/windows-terminal-preview",
    "main/lsd",
    "extras/mambaforge"
)

foreach ($package in $packages) {
    Install-Package -packageName $package
}

# Launch common applications
Write-Log "Launching common applications."
Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
Start-Process "notepad.exe"
Start-Process "explorer.exe"

try {
    Start-Process "wt.exe" -Wait
    Write-Log "Launched Windows Terminal."
} catch {
    Write-Log "Failed to launch Windows Terminal. Launching PowerShell instead."
    Start-Process "powershell.exe"
}

# Update Scoop and install additional packages
Write-Log "Updating Scoop."
scoop update

# Install additional packages after updating Scoop
$additionalPackages = @(
    "extras/x64dbg",
    "main/curl",
    "versions/openssl-light",
    "extras/okular",
    "extras/irfanview-lean",
    "extras/mpc-hc-fork",
    "extras/carapace-bin",
    "main/zoxide",
    "nerd-fonts/FiraMono-NF-Mono",
    "nerd-fonts/FiraCode-NF"
)

foreach ($package in $additionalPackages) {
    Install-Package -packageName $package
}

Write-Log "Scoop script execution completed."