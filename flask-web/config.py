class Config:
    DEBUG = False

class DevelopmentConfig(Config):
    #CONFIGS DO FLASK
    
    DEBUG = True
    SECRET_KEY = '123456790'

    #CONFIGS FLASK_SECURITY
    SECURITY_PASSWORD_SALT = '123'
    SECURITY_REGISTERABLE = True
    
    #CONFIGS DO SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = 'sqlite:///keys.db'
    SQLALCHEMY_ECHO = True
    
    #CONFIGS JWT
    JWT_SECRET_KEY = '123'
        

class ProductionConfig(Config):
    # Configurações de produção...
    pass

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}