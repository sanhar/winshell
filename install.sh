sudo apt-get install wine
wget https://www.python.org/ftp/python/2.7.9/python-2.7.9.amd64.msi
wine msiexec /i python-2.7.9.amd64.msi /qb
wine ~/.wine/drive_c/Python27/Scripts/pip.exe install pyinstaller
sudo rm -f python-2.7.9.amd64.msi
