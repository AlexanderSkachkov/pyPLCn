# PyPLCn

| Date       | Version | Author       |
|------------|---------|--------------|
| 14.10.2020 | 1.0.1   | Alexander Skachkov |

## Description

A simple REST library to use variables in PLCnext(c) AXC F 2152 PLC from Python.

## Contributing

Contributions to this project are welcome.

## Installing

Run `pip install PyPLCn`

## Usage

Make to any global variable hmi Tag

Put variable to list - `Plc.set_var_names(['LevelMinimum', 'LevelMaximum', 'Robot.Test_Var', 'LevelCurrent'])`

Set variable value - `Plc.set_var('LevelMinimum', '500')` Don't forget! Variable value must be a string.

Get variable value - `Plc.get_var('LevelMinimum')`

You also can access variables with "HMI" flag in programs - `Plc.get_var('Robot.Test_Var')` Where `Robot` is program name.

If you use HMI authentication you must set login name and password in method `Plc.connect('192.168.1.10', login='user', password='12345', poll_time=100)`. Else leave these fields blank or dont use them.

## Example details

|Description | Value |
|------------ |-----------|
|Controller| AXC F 2152 |
|FW | 2020.0 LTS or later |
|PLCnext(c) Engineer(c)| 2020.0 LTS or later |
|Python| Version 3 or later |

## Exaple usage

Upload project to PLC from "examples" folder

Run code below

On HMI page you can see how values `LevelMinimum` and `LevelMaximum` change states, and in Python console you can see value `LevelCurrent`

```
from pyPLCn import pyPLCn
import time

if __name__ == '__main__':
    Plc = pyPLCn()
    Plc.set_var_names(['LevelMinimum', 'LevelMaximum', 'Robot.Test_Var', 'LevelCurrent'])
    Plc.connect('192.168.1.10', poll_time=100)
    while True:
        Plc.set_var('LevelMinimum', '500')
        Plc.set_var('LevelMaximum', '800')
        print('#####################################')
        print('LevelMinimum - {}'.format(Plc.get_var('LevelMinimum')))
        print('LevelMaximum - {}'.format(Plc.get_var('LevelMaximum')))
        print('Robot.Test_Var - {}'.format(Plc.get_var('Robot.Test_Var')))
        print('LevelCurrent - {}'.format(Plc.get_var('LevelCurrent')))
        print('#####################################')
        time.sleep(0.5)
        Plc.set_var('LevelMinimum', '300')
        Plc.set_var('LevelMaximum', '500')
        print('#####################################')
        print('LevelMinimum - {}'.format(Plc.get_var('LevelMinimum')))
        print('LevelMaximum - {}'.format(Plc.get_var('LevelMaximum')))
        print('Robot.Test_Var - {}'.format(Plc.get_var('Robot.Test_Var')))
        print('LevelCurrent - {}'.format(Plc.get_var('LevelCurrent')))
        print('#####################################')
        time.sleep(0.5)
```

## Warning note!

Not for industrial usage! Use it on you own risk.