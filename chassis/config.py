import sys
import configparser


def get_config_value(section, key):
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        value = config[section][key]
    except KeyError:
        sys.stderr.write("Section or Key does not exist in config.ini")
        sys.exit(1)

    return value


def set_config_value(section, key, value):
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        config[section][key] = value
    except KeyError:
        sys.stderr.write("Section or Key does not exist in config.ini")
        sys.exit(1)

    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def create_default_configfile():
    config = configparser.ConfigParser()

    config['CAN'] = {}
    config['CAN']['can1-interface'] = 'vcan0'
    config['CAN']['can2-interface'] = 'vcan1'
    config['CAN']['can3-interface'] = 'vcan2'
    config['CAN']['inverter-id'] = '0x0C00'
    config['CAN']['amu-id'] = '0x0A00'
    config['CAN']['pdm-id'] = '0x0900'
    config['CAN']['shutdown-id'] = '0x0880'
    config['CAN']['wheel-id'] = '0x0840'

    config['HEARTBEAT'] = {}
    config['HEARTBEAT']['heartbeat-frequency'] = '1000'
    config['HEARTBEAT']['inverter-frequency'] = '100'
    config['HEARTBEAT']['amu-frequency'] = '20'
    config['HEARTBEAT']['pdm-frequency'] = '20'
    config['HEARTBEAT']['shutdown-frequency'] = '10'
    config['HEARTBEAT']['wheel-frequency'] = '20'

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

