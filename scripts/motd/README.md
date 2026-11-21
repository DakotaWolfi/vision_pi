# VisionPi SSH welcome banner

The original MOTD was captured from the working VisionPi Raspberry Pi 5.

Install on the VisionPi host:

```sh
sudo install -m 755 scripts/motd/10-visionpi /etc/update-motd.d/10-visionpi
sudo /etc/update-motd.d/10-visionpi
```

This is an SSH/login banner, **not** a graphical Plymouth boot splash. The banner reads host, kernel, IPv4 address and SoC temperature dynamically. A separate `10-uname` or USB gadget MOTD may also be enabled on the original installation.
