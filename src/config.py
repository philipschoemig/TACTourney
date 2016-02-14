'''
Created on 02.10.2014

@author: Philip
'''

import ConfigParser
from enum import Enum


class ConfigOption(object):
    '''
    An option of the application configuration.
    '''

    # Enumeration of the available option types
    Types = Enum('boolean', 'float', 'int', 'string')

    # The section to query from the config parser
    section = None
    # The option to query from the config parser
    option = None
    # The key to store in the application config
    config_key = None
    # The type of the option
    type = None

    def __init__(self, section, option, config_key, option_type=Types.string):
        self.section = section
        self.option = option
        self.config_key = config_key
        self.type = option_type

    def parse(self, config, config_parser):
        '''
        Parses the option from the config parser and stores it in the application configuration.
        '''
        value = None
        if self.type == self.Types.boolean:
            value = config_parser.getboolean(self.section, self.option)
        elif self.type == self.Types.float:
            value = config_parser.getfloat(self.section, self.option)
        elif self.type == self.Types.int:
            value = config_parser.getint(self.section, self.option)
        else:
            value = config_parser.get(self.section, self.option)
        config[self.config_key] = value


class Configurator(object):
    '''
    A configurator for managing the application configuration.
    '''

    config = None
    config_parser = None

    options = [
        ConfigOption('application', 'name', 'APP_NAME'),
        ConfigOption(
            'application', 'testing', 'TESTING', ConfigOption.Types.boolean),
        ConfigOption(
            'application', 'debugging', 'DEBUG', ConfigOption.Types.boolean),
        ConfigOption('database', 'uri', 'SQLALCHEMY_DATABASE_URI'),
        ConfigOption('logging', 'file', 'LOG_FILE'),
        ConfigOption('logging', 'level', 'LOG_LEVEL'),
        ConfigOption('mail', 'server', 'MAIL_SERVER'),
        ConfigOption('mail', 'port', 'MAIL_PORT', ConfigOption.Types.int),
        ConfigOption('mail', 'username', 'MAIL_USERNAME'),
        ConfigOption('mail', 'password', 'MAIL_PASSWORD'),
        ConfigOption('mail', 'sender', 'MAIL_DEFAULT_SENDER'),
        ConfigOption(
            'mail', 'use_ssl', 'MAIL_USE_SSL', ConfigOption.Types.boolean),
        ConfigOption(
            'mail', 'use_tls', 'MAIL_USE_TLS', ConfigOption.Types.boolean),
        ConfigOption('report', 'recipients', 'REPORT_RECIPIENTS'),
        ConfigOption('report', 'level', 'REPORT_LEVEL'),
        ConfigOption('recaptcha', 'public_key', 'RECAPTCHA_PUBLIC_KEY'),
        ConfigOption('recaptcha', 'private_key', 'RECAPTCHA_PRIVATE_KEY'),
        ConfigOption(
            'recaptcha', 'use_ssl', 'RECAPTCHA_USE_SSL', ConfigOption.Types.boolean),
    ]

    def __init__(self, app):
        self.config = app.config
        self.config_parser = ConfigParser.SafeConfigParser({
            'root_path': app.root_path,
            'instance_path': app.instance_path})
        self.parse()

    def parse(self):
        '''
        Parses the configuration file.
        '''
        self.config_parser.readfp(
            open(self.config['DEFAULT_CONFIG_PATH'], 'r'))
        self.config_parser.read([self.config['USER_CONFIG_PATH']])

        for option in self.options:
            option.parse(self.config, self.config_parser)

    def save(self):
        '''
        Saves the configuration file.
        '''
        self.config_parser.write(open(self.config['USER_CONFIG_PATH'], 'w'))
