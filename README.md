![](https://i.imgur.com/AluMwI0.png)

# vSIX Pi
[![](http://img.shields.io/github/license/wide-vsix/vsixpi)](LICENSE) [![](https://img.shields.io/github/issues/wide-vsix/vsixpi)](https://github.com/wide-vsix/vsixpi/issues) [![](https://img.shields.io/github/issues-pr/wide-vsix/vsixpi)](https://github.com/wide-vsix/vsixpi/pulls) [![](https://img.shields.io/github/last-commit/wide-vsix/vsixpi)](https://github.com/wide-vsix/vsixpi/commits) [![](https://img.shields.io/github/release/wide-vsix/vsixpi)](https://github.com/wide-vsix/vsixpi/releases)

Make your Raspberry Pi a vSIX access router with cloud-init.

**NOTE:** This cloud-config is for Raspberry Pi - might work on other Ubuntu machines as well but not guaranteed.

## Specs of vSIX Pi
vSIX Pi is a Raspberry Pi-based broadband router officially maintained by vSIX Project. It supports the following features as of September 1, 2021, making it easy for anyone to experience Internet access via vSIX - AS4690.

- **Connect to vSIX directly through NGN** - no need to pay your ISP anymore. Connection through the WIDE-BB is also supported 
- **Living in a multi-prefix network** - connect to two or more tunnel providers simultaneously and advertise multiple prefixes with RA
- Use with wireless - your Pi become a fast Wi-Fi access point supporting 11n/ac
- Use with wired - support Ethernet connection via additional USB NICs or tagged VLAN on the onboard NIC

### Prerequisites
Apply the Generic Tunneling Access Service from [vSIX Portal](https://portal.vsix.wide.ad.jp/), and get the IPv6 prefixes delegated. The following information is needed to set up vSIX Pi; all of them are displayed on the Portal.

- **Your global IPv6 address** - customer endpoint (CE) address, also needed for the prior submission. Typically, this address is allocated from your ISP (VNE)
- **IPv6 addresses of each tunnel provider** - provider endpoint (PE) addresses
- **Delegated IPv6 prefixes of each site** - `/60` of address space is allocated for every PE

Prepare a Raspberry Pi. The authors, the vSIX Access Service Team, tested using the series 4B+ with 2GB of RAM and 16GB of storage. It might also work with the series 3B, although Wi-Fi and Ethernet performance would be degraded - check  [hardware specifications](https://en.wikipedia.org/wiki/Raspberry_Pi#Specifications) of your Pi. In summary, the minimum system requirements are as follows:

- **Ubuntu Server 20.04 and later** installed on **series 3B and later**
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

Next, override the example variables adjusting with your environment. Follow the instructions in the comments carefully.

```
% cp vsixpi.yml.example vsixpi.yml
% vim vsixpi.yml
```

Finally, build the cloud-config templates - the outputs are in the `cloud-config` directory.

```
% pipenv run generate
% bat cloud-config/user-data -l yaml
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

When the writing is completed, the SD card will be remounted as `system-boot`. Copy all the files under the `cloud-config` directory to this area and overwrite the default cloud-config.

Connect LAN cable to the onboard NIC, insert the SD card, and turn on the power. cloud-init is called during the initial boot sequence, and this is why the first startup takes a relatively long time - it is about 30 minutes in the author's environment, though it depends mainly on your network bandwidth. Note that your Pi will automatically reboot once during the cloud-init setup. Wait until the console is entirely silent.

You will see a Wi-Fi named VSIX-FREE-WIFI by default. If you connect it with `Adios,IPv4!`, RDNSS will complete the address configuration and ready you to experience the vSIX access service - of course, you can change the SSID and password. Welcome to vSIX; let's test your connectivity at [test-ipv6.com](https://test-ipv6.com/)!

**FYI:** [iNonius Project](https://inonius.net/) provides the speed test service for both IPv4 and IPv6.

## Hints and tips from vSIX developers
Below are hints and tips for the advanced use of vSIX Pi.

### Traffic monitoring
Open your favorite browser and go to [http://vsixpi.local:19999](http://vsixpi.local:19999) to see [Netdata](https://www.netdata.cloud/) monitoring dashboard.

[![](https://i.imgur.com/nHMLnWY.png)](https://i.imgur.com/nHMLnWY.png)
[![](https://i.imgur.com/uYjA47F.png)](https://i.imgur.com/uYjA47F.png)

**ATTENTION:** If you would like to help us improve our service quality, please run the following command on your Pi. Netbox will send your Pi's metrics to our account, enabling us to detect the deterioration quickly.

```
% sudo docker exec -it netdata netdata-claim.sh \
    -token=HMWaSQ0c3eTe_NE3qXW2RNi8uK5aWKRvY__pO8Z8rcIKsd90duT4zzeHqHGV8phaKzp-7QGK1-o9RIEPNL_nH1j_eD6xL_lubBBKoYYcXOqJThubqomLNwm4gE-1x56yFSNvJpk \
    -rooms=0e12b8e6-bf96-4d10-aabd-a3f0976f43de,7a52dc34-6231-4dee-8fb2-fd7259b77e3f \
    -url=https://app.netdata.cloud
```

### Reconfigure your vSIX Pi after cloud-init
The following updates can be applied by editing the `vsixpi.yml`:

- Change CE address and PE addresses - discarding or moving tunnels
- Change SSID, passphrase, and radio channel
- Change VLAN ID of the onboard NIC, install or uninstall USB Ethernet adapters
- Change RA related parameters as well as MTU and MSS-clamp

Remember to reboot after the reconfiguration; otherwise, system will be unstable or some configuration will not applied appropriately.

```
% cd /var/lib/vsixpi
% sudo vim vsixpi.yml
% sudo pipenv run reconfigure
% sudo reboot
```

**CAUTION:** This operation is destructive - it overwrites each configuration file, and any manual changes made to them will be lost.

## Announcements
Check [issues](https://github.com/wide-vsix/cloud-init-vsixpi/issues) and [pull requests](https://github.com/wide-vsix/cloud-init-vsixpi/pulls) as well.

### Planned new features and upcoming releases

- Perform periodical health checks from vSIX Pis to automatically detect failures of the access service or backbone network - currently being undertaken and developed with the [@SINDAN](https://github.com/SINDAN) project
- Selective RA based on an automatic tunnel quality measurement for IPv6 multi-prefix environment

### Known issues and workarounds

- Currently, the auto-reconfiguration feature doesn't work. We're trying to fix the bugs, and kindly follow the above [manual reconfigure procedure](https://github.com/wide-vsix/vsixpi#reconfigure-running-vsix-pi) for the time being

## Maintainers
This repository is maintained by the vSIX Access Service Team and supported by many volunteers. Followings are responsible for reviewing pull requests:

- **miya** - *Author of the initial release* [@mi2428](https://github.com/mi2428)
- **hide** - *Co-author of the initial release* [@hdfln](https://github.com/hdfln)

See also the list of [contributors](https://github.com/wide-vsix/vsixpi/graphs/contributors) who participated in this project.

## License
This product is licensed under [The 2-Clause BSD License](https://opensource.org/licenses/BSD-2-Clause) - see the [LICENSE](LICENSE) file for details.
