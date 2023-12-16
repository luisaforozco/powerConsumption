## 👋 Welcome!

I have created this repo for the scripts that I use to monitor the power consumption at my home 🏡.

It is a personal project, but please reach out if there is anything to improve, or something that you find interesting.

## Installation

```bash
 conda create --name tuya python=3.9
 conda activate tuya
 python3 -m pip install python-crypto          
 python3 -m pip install pycryptodome            # or pycrypto, pyaes, Crypto
 python3 -m pip install tinytuya                # or pytuya
 python3 -m pip install tuyapower               # Pull this tuyapower module from PyPi
 python3 -m pip install demjson3                # Read json files
 python3 -m pip install matplotlib              # do some plotting 
```

## Setup of TuyaPower

Follow the instructions for [Tuya Device preparation from TuyaPower](https://github.com/jasonacox/tuyapower#tuya-device-preparation) and read the **Notes**. They are pertinent for using these scripts after the first time.

As a result, you should now have in the root folder the following files:

- `devices.json` : most important one - contains the keys.
- `tinytuya.json` : configuration data with the credentials that you used to scan.
- `tuya-raw.json` : General information about the devices, contains the mappings.
- `snapshot.json` : Only created if you answered `Y` to Poll local devices? (Y/n). It has the current reading values of the device.

## Scripts

This contains examples scripts for using `tuyapower`.

Check the main [Example.py](https://github.com/jasonacox/tuyapower/blob/master/examples/README.md) from TuyaPower.

### washing_machine.py

I created this script to monitor the power consumption during a wash.
This script:

- Gathers the device info and establishes the communication with it.
- Has a loop in time to retrieve the information from the smart plug.
- Saves the reading to a txt file with name the time stamp.
- (Optionally) plots the power consumption.
