class Config:
    SECRET_KEY = "2345678"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    def get_segredo(self):
        return self.SECRET_KEY