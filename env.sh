sudo apt update; \

sudo apt install snapd; sudo snap install gstreamer --edge; \
sudo apt install python3.9; sudo apt install python3-pip \

sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio; \

sudo apt install git; \
sudo apt install postgresql postgresql-contrib; sudo systemctl start postgresql.service; \

sudo apt install curl; curl -sL https://deb.nodesource.com/setup_14.x | sudo bash - ; sudo apt -y install nodejs; \

pip install -r requirements.txt


