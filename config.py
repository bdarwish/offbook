import configparser
import os

def load_config(config_path: str):
    config = configparser.ConfigParser()

    if not os.path.exists(config_path):
        config['general'] = {
            'feedback_mode': 'line'
        }

        config['voice'] = {
            'voice': 'en-US-AndrewNeural',
            'speed': '100'
        }

        config['silence'] = {
            'toggle_silence_stop': 'True',
            'seconds_of_silence': '3'
        }

        config['duration'] = {
            'toggle_max_duration': 'False',
            'max_duration': '30'
        }
        
        config['other'] = {
            'api_key': 'None',
        }

        with open(config_path, 'w') as path:
            config.write(path)
    else:
        try:
            config.read(config_path)

            _ = config.get('general', 'feedback_mode')
            _ = config.get('voice', 'voice')
            _ = config.getint('voice', 'speed')
            _ = config.getboolean('silence', 'toggle_silence_stop')
            _ = config.getint('silence', 'seconds_of_silence')
            _ = config.getboolean('duration', 'toggle_max_duration')
            _ = config.getint('duration', 'max_duration')
            _ = config.get('other', 'api_key')
        except (configparser.NoSectionError, configparser.NoOptionError, KeyError, ValueError) as e:
            print(f'Error loading config: {e}')
            print('Regenerating file...')
            os.remove(config_path)
            load_config(config_path)

    return config