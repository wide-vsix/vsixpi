# cloud-init-vsixpi


**NOTE:** This cloud-config is for Raspberry Pi - might work on other Ubuntu machines as well but not guaranteed.

## Specs of vSIX Pi
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

Next, override the template variables adjusting with your environment. 
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

### Monitoring traffic
TBD

### Install additional USB NIC
TBD

## License
This product is licensed under [The 2-Clause BSD License](https://opensource.org/licenses/BSD-2-Clause) - see the [LICENSE](LICENSE) file for details.
