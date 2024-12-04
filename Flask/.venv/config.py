class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    PATH_ONTOLOGIE_URI = "C:\Users\USER\Documents\WebSemantica\web-semantics\oncology.rdf"

config={
    "development":DevelopmentConfig
}