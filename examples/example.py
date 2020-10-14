from pyPLCnext import pyPLCnext
import time

if __name__ == '__main__':
    Plc = pyPLCnext()
    Plc.set_var_names(['LevelMinimum', 'LevelMaximum', 'Robot.Test_Var', 'LevelCurrent'])
    Plc.connect('192.168.1.10', login='user', password='12345', poll_time=100)
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
