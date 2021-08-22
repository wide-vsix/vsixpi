# vsixpi
Make your Raspberry Pi a vSIX access router with cloud-init.

**NOTE:** This cloud-config is for Raspberry Pi - might work on other Ubuntu machines as well but not guaranteed.

## Specs of vSIX Pi
vSIX Pi is a Raspberry Pi-based broadband router officially maintained by vSIX Project. It supports the following features as of August 11, 2021, making it easy for anyone to experience Internet access via vSIX - AS4690.

- **Connect to vSIX directly through NGN** - no need to pay your ISP anymore
- Use with wireless - your Pi becomes a Wi-Fi access point
- Use with wired - support ethernet connection via tagged VLAN on the onboard NIC

### Prerequisites
Apply the Generic Tunneling Access Service from [vSIX Portal](https://portal.vsix.wide.ad.jp/), and get the IPv6 prefixes delegated. The following information is needed to set up; all of them are displayed on the vSIX Portal.

- **Your global IPv6 address** - also needed for the prior submission
- **IPv6 address of each tunnel provider**
- **Delegated IPv6 prefixes**

Prepare the Raspberry Pi. The authors tested using the series 4B+ with 2GB of RAM and 16GB of storage.

- **Ubuntu Server 20.04 and later** installed on **series 4B and later**
- More than **2GB** of RAM
- More than **16GB** of SD card capacity

## Getting started with your Raspberry Pi
First, shallow clone this repository and install dependent libraries with:

```
% git clone --depth 1 https://github.com/wide-vsix/cloud-init-vsixpi
% cd cloud-init-vsixpi
% pipenv update
```

Next, override the template variables adjusting with your environment. Follow the instructions in the comments.

```
% cp vsixpi.yml.example vsixpi.yml
% vim vsixpi.yml
```

Finally, build config templates - the outputs are in the `system-boot` directory.

```
% pipenv run generate
```

## Hints and tips
Below are hints and tips for the advanced use of vSIX Pi.

### Traffic monitoring
TBD

### Install additional USB NIC
First, plug the USB-NIC and check its MAC address. Type the following to fix the interface name with MAC address `11:22:33:AA:BB:CC` to `usb1` by:

```
% sudo cat <<EOF >> /etc/udev/rules.d/30-persistent-net.rules
SUBSYSTEM=="net",ACTION=="add",ATTR{address}=="11:22:33:AA:BB:CC",NAME="usb1"
EOF
```

Restart udev, then unplug and re-plug the USB-NIC. Check the interface name has changed expectedly.

```
% sudo systemctl restart udev.service
```

Edit `/etc/network/interfaces` to enable auto-start the USB-NIC. Note that the two lines you add here have to be written before `br0` statements.

```
...
auto  usb1                   # Add here
iface usb1     inet  manual  # Add here

auto  br0
iface br0      inet  manual
...
```

Edit `/etc/network/if-up.d/vsix` to add the NIC to `br0`

```
...
elif [[ "$IFACE" == br0 ]]; then
  /sbin/ip link set dev eth0.200 master br0
  /sbin/ip link set dev usb1 master br0  # Add here
fi
...
```

Finally, restart networking, and you can now connect vSIX via the USB-NIC.

```
% sudo systemctl restart networking.service
```

## Notes
Check [issues](https://github.com/wide-vsix/cloud-init-vsixpi/issues) and [pull requests](https://github.com/wide-vsix/cloud-init-vsixpi/pulls) as well.

### Planned new features and upcoming releases

- Support wireguard access service
- Health check utilities

### Known issues and workarounds
TBD

## License
This product is licensed under [The 2-Clause BSD License](https://opensource.org/licenses/BSD-2-Clause) - see the [LICENSE](LICENSE) file for details.
