![](https://i.imgur.com/AluMwI0.png)

# vSIX Pi
[![](http://img.shields.io/github/license/wide-vsix/vsixpi)](LICENSE) [![](https://img.shields.io/github/issues/wide-vsix/vsixpi)](https://github.com/wide-vsix/vsixpi/issues) [![](https://img.shields.io/github/issues-pr/wide-vsix/vsixpi)](https://github.com/wide-vsix/vsixpi/pulls) [![](https://img.shields.io/github/last-commit/wide-vsix/vsixpi)](https://github.com/wide-vsix/vsixpi/commits) [![](https://img.shields.io/github/release/wide-vsix/vsixpi)](https://github.com/wide-vsix/vsixpi/releases)

Make your Raspberry Pi a vSIX access router with cloud-init.

**NOTE:** This cloud-config is for Raspberry Pi - might work on other Ubuntu machines as well but not guaranteed.

## Specs of vSIX Pi
vSIX Pi is a Raspberry Pi-based broadband router officially maintained by vSIX Project. It supports the following features as of August 24, 2021, making it easy for anyone to experience Internet access via vSIX - AS4690.

- **Connect to vSIX directly through NGN** - no need to pay your ISP anymore. Connection via WIDE-BB is also provided
- **Create multi-prefix network** - connect to two or more tunnel providers simultaneously and advertise multiple prefixes with RA
- Use with wireless - your Pi become a fast Wi-Fi access point supporting 11ac
- Use with wired - support ethernet connection via additional USB NICs or tagged VLAN on the onboard NIC

### Prerequisites
Apply the Generic Tunneling Access Service from [vSIX Portal](https://portal.vsix.wide.ad.jp/), and get the IPv6 prefixes delegated. The following information is needed to set up; all of them are displayed on the Portal.

- **Your global IPv6 address** - customer endpoint (CE) address, also needed for the prior submission
- **IPv6 address of each tunnel provider** - provider endpoint (PE) addresses
- **Delegated IPv6 prefixes** - `/60` of address space is allocated for every PE

Prepare a Raspberry Pi. The authors, vSIX Access Service Team, tested using the series 4B+ with 2GB of RAM and 16GB of storage.

- **Ubuntu Server 20.04 and later** installed on **series 4B and later**
- More than **2GB** of RAM
- More than **16GB** of SD card capacity

Thanks to [cloud-init](https://cloudinit.readthedocs.io/en/latest/), installation and setup procedures are fully automated. All you have to do is *1)* edit a simple configuration file in YAML format and *2)* type a single command to generate cloud-config.

## Getting started with your Raspberry Pi
First, shallow clone this repository and install dependent libraries with:

```
% git clone --depth 1 https://github.com/wide-vsix/cloud-init-vsixpi
% cd cloud-init-vsixpi
% pipenv update
```

Next, override the example variables adjusting with your environment. Follow the instructions in the comments.

```
% cp vsixpi.yml.example vsixpi.yml
% vim vsixpi.yml
```

Finally, build config templates - the outputs are in the `cloud-config` directory.

```
% pipenv run generate
```

### For noobs
Download the latest Ubuntu Server from [here](https://ubuntu.com/download/raspberry-pi) - the LTS release is recommended, but it is totally up to you. Then extract .xz archive and burn your SD card.

For macOS users, this is like the following:

```
% diskutil list                         # Check where the SD card is mounted
% sudo diskutil unmountDisk /dev/disk2  # Suppose /dev/disk2 is the SD card
% # Specify target path as /dev/rdisk2 instead of /dev/disk2 - it will fasten the writing
% sudo gdd bs=16M status=progress if=./ubuntu-20.04.2-preinstalled-server-arm64+raspi.img of=/dev/rdisk2
```

When the writing is completed, the SD card will be remounted as `system-boot`. Copy all the files under the `cloud-config` directory to this area.

Connect LAN cable to the onboard NIC, insert the SD card, and turn on the power. `cloud-init` is called during the initial boot sequence, and this is why the first startup takes a long time - it is about 20 minutes in the author's environment, though it depends mainly on your ISP. Note that your Pi will automatically reboot once during the `cloud-init` setup.

You will see a Wi-Fi named VSIX-FREE-WIFI by default. If you connect it with `Adios,IPv4!`, RDNSS will complete the address configuration and ready you to experience the vSIX access service - of course, you can change the SSID and password. Let's test your connectivity at [test-ipv6.com](https://test-ipv6.com/)!

## Hints and tips
Below are hints and tips for the advanced use of vSIX Pi.

### Traffic monitoring
TBD

### Reconfigure running vSIX Pi
The following updates can be applied by editing the `vsixpi.yml`.

- Change CE address
- Add or remove PE addresses - moving tunnels
- Change SSID and password
- Change VLAN ID of the onboard NIC for vSIX access network
- Add or remove USB ethernet adapters
- Add or remove DNS64 servers

```
% cd /var/lib/vsixpi
% vim vsixpi.yml
% sudo pipenv run reconfigure
```

**CAUTION:** This operation is destructive - it overwrites each configuration file, and any manual changes made to them will be lost.

## Notes
Check [issues](https://github.com/wide-vsix/cloud-init-vsixpi/issues) and [pull requests](https://github.com/wide-vsix/cloud-init-vsixpi/pulls) as well.

### Planned new features and upcoming releases

- Health check utility

### Known issues and workarounds

- Currently, auto-reconf function does not work. Follow the above manual reconfigure procedure.

## License
This product is licensed under [The 2-Clause BSD License](https://opensource.org/licenses/BSD-2-Clause) - see the [LICENSE](LICENSE) file for details.
