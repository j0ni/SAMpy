import os
import sys
import json

fileDir = os.path.dirname(os.path.realpath(__file__))

def load_config(cfg_file=os.path.join(fileDir,'SAMpy.cfg')):
    '''Load configuration information from a json encoded file.
    Core config options are:
    sdk_path: path to the local install of the SAM SDK
    SAM_path: path to the root of the SAM install, from which simulation resources can be recovered
    weather_path: path to a local source of weather data, typically /path/to/SAM/YYYY.MM.DD\solar_resource'''
    if not os.path.isfile(cfg_file):
        raise ValueError("Can't find config at %s" % cfg_file)
    with open(cfg_file, 'r') as cf:
        config = json.load(cf)
    return config

def write_config(config, cfg_file=os.path.join(fileDir,'SAMpy.cfg')):
    '''Write the system configuration to the passed path.'''
    print('writing config to %s' % cfg_file)
    with open(cfg_file,'w') as cf:
        json.dump(config, cf, sort_keys=True, indent=4, separators=(',', ': '))

def get_config_value(key, instructions, prompt, validate, validate_error, cfg_file=os.path.join(fileDir,'SAMpy.cfg')):
    '''Learn where the SAM SDK is on the local system and return that path:
    (1) Look in a simple configuration file.
    (2) If not found, prompt the user, check directory existence, and write to the config file.
    '''
    config = {}
    try:
        config = load_config(cfg_file)
        # provoke KeyError if not found
        junk = config[key]
    except (ValueError, KeyError) as err:
        print(err.message)
        print(instructions)

        # get command line input into a valid path is provided
        while not config.has_key(key):
            valueStr = raw_input(prompt)
            if (validate(valueStr)):
                config[key] = valueStr
            else:
                print(validate_error)
        write_config(config, cfg_file)
    return config[key]

def get_sdk_path(cfg_file=os.path.join(fileDir,'SAMpy.cfg')):
    key = 'sdk_path'
    instructions =  '''This module is a wrapper for the SAM SDK found here: 
        https://sam.nrel.gov/sdk
        Once you have extracted the SDK to disk, you need to provide the path to the base directory.
        For example, /path/to/sam-sdk-YYYY-MM-DD-r1'''
    prompt = 'Enter the path to your SAM SDK directory: '
    validate = os.path.exists
    validate_error = 'That path does not exist. Please enter another.'
    return get_config_value(key, instructions, prompt, validate, validate_error, cfg_file)

def get_sam_path(cfg_file=os.path.join(fileDir,'SAMpy.cfg')):
    key = 'sam_path'
    instructions =  '''This module relies on the resources of the SAM PV and battery simulation tool found here: 
        https://sam.nrel.gov/download
        Once you have installed it, you need to provide the path to the base SAM directory.
        For example, /path/to/SAM/YYYY.MM.DD'''
    prompt = 'Enter the path to your SAM directory: '
    validate = os.path.exists
    validate_error = 'That path does not exist. Please enter another.'
    return get_config_value(key, instructions, prompt, validate, validate_error, cfg_file)

def get_weather_path(cfg_file=os.path.join(fileDir,'SAMpy.cfg')):
    key = 'weather_path'
    instructions =  '''Where a file name without a path is passed to a simulation, his module loads TMY 
        (aka solar resource)or custom weather data from the default 'solar_resource' directory under the SAM tool install directory.
        If you would like to configure a different default location, provide it below. If not, just hit return..'''
    prompt = 'Enter the path to your weather directory or press return for the default: '
    validate = lambda x: x == '' or os.path.exists(x)
    validate_error = 'That path does not exist. Please enter another.'
    return get_config_value(key, instructions, prompt, validate, validate_error, cfg_file)

# Identify the path to the SAM SDK
sdk_path = get_sdk_path()
sam_path = get_sam_path()
weather_path = get_weather_path()

# Add the SDK to the system path so the non-portable PySSC they provide can be imported
sys.path.insert(0, os.path.join(sdk_path, "languages", "python"))
from sscapi import PySSC

from .portable_sscapi import PortablePySSC
from .sam_wrapper import SAMEngine
# Import the oficcial python SDK wrapper, which our portable version will extend

# Copied from the sscapi outside of the class definition
#from ctypes import c_float
#c_number = c_float # must be c_double or c_float depending on how defined in sscapi.h

#__all__ = ['submodule1', 'submodule2']