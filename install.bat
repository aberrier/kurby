::This installs choco, as found on https://chocolatey.org/docs/installation
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command " [System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

choco install -y git mpv python3
refreshenv && pip3 install kurby && echo Testing command... && kurby --help && echo You can now run a new terminal and use kurby && pause