#!/bin/sh


echo "Installing dependencies..."
pip install -r requirements.txt >/dev/null 2>&1
echo "Installed dependencies\n"

if [ ! "$(id -u)" -eq 0 ]; then
    echo "Please run this script as root or sudo!"
    exit
fi

echo "Making file executable"
chmod +x ./main.py
echo "Moving file to \`/bin\`"
cp ./main.py /bin/obyaf

echo "\nAll done! you may now run obyafetch using \`obyaf\`"
