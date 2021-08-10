# cloud-init-vsixpi


**NOTE:** This cloud-config is for Raspberry Pi - on other Ubuntu machines, it might work, but it is not guaranteed.

## Brief introduction of vSIX Pi

### Prerequisites


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
