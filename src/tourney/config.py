'''
Created on 02.10.2014

@author: Philip
'''

import ConfigParser


class Configurator(object):
    '''
    Configurator for parsing the application configuration.
    '''

    config = None
    config_parser = None

    def __init__(self, app):
        self.config = app.config
        self.config_parser = ConfigParser.SafeConfigParser({
            'root_path': app.root_path,
            'instance_path': app.instance_path})
        self.config_parser.readfp(open(self.config['DEFAULT_CONFIG_PATH']))
        self.config_parser.read([self.config['USER_CONFIG_PATH']])
        self.parse()
    
    def parse(self):
        self.parse_application_section()
        self.parse_database_section()
        self.parse_logging_section()
        self.parse_mail_section()
        self.parse_report_section()
        self.parse_recaptcha_section()
    
    def parse_application_section(self):
        section = 'application'
        
        name = self.config_parser.get(section, 'name')
        self.config['APP_NAME'] = name
        
        testing = self.config_parser.getboolean(section, 'testing')
        self.config['TESTING'] = testing
        
        debugging = self.config_parser.getboolean(section, 'debugging')
        self.config['DEBUG'] = debugging
    
    def parse_database_section(self):
        section = 'database'
        
        uri = self.config_parser.get(section, 'uri')
        self.config['SQLALCHEMY_DATABASE_URI'] = uri
    
    def parse_logging_section(self):
        section = 'logging'
        
        logfile = self.config_parser.get(section, 'file')
        self.config['LOG_FILE'] = logfile
        
        level = self.config_parser.get(section, 'level')
        self.config['LOG_LEVEL'] = level
    
    def parse_mail_section(self):
        section = 'mail'
        
        server = self.config_parser.get(section, 'server')
        self.config['MAIL_SERVER'] = server
        
        port = self.config_parser.getint(section, 'port')
        self.config['MAIL_PORT'] = port
        
        username = self.config_parser.get(section, 'username')
        self.config['MAIL_USERNAME'] = username
        
        password = self.config_parser.get(section, 'password')
        self.config['MAIL_PASSWORD'] = password
        
        sender = self.config_parser.get(section, 'sender')
        self.config['MAIL_DEFAULT_SENDER'] = sender
        
        use_ssl = self.config_parser.getboolean(section, 'use_ssl')
        self.config['MAIL_USE_SSL'] = use_ssl
        
        use_tls = self.config_parser.getboolean(section, 'use_tls')
        self.config['MAIL_USE_TLS'] = use_tls
    
    def parse_report_section(self):
        section = 'report'
        
        recipients = self.config_parser.get(section, 'recipients')
        self.config['REPORT_RECIPIENTS'] = recipients
        
        level = self.config_parser.get(section, 'level')
        self.config['REPORT_LEVEL'] = level
    
    def parse_recaptcha_section(self):
        section = 'recaptcha'
        
        public_key = self.config_parser.get(section, 'public_key')
        self.config['RECAPTCHA_PUBLIC_KEY'] = public_key
        
        private_key = self.config_parser.get(section, 'private_key')
        self.config['RECAPTCHA_PRIVATE_KEY'] = private_key
        
        use_ssl = self.config_parser.getboolean(section, 'use_ssl')
        self.config['RECAPTCHA_USE_SSL'] = use_ssl
