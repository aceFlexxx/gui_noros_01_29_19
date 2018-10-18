### Install udev rules

sudo ln -s $(pwd)/99-hue.rules /etc/udev/rules.d/99-hue.rules
sudo udevadm control --reload
sudo udevadm trigger
