from redis_om import (Field,
    Migrator,
    JsonModel)

from .Common import CommonModel

class Charterer(CommonModel):
    company:str = Field(index=True, full_text_search=True, regex=r'.*')
    nation:str = Field(index=True, full_text_search=True, regex=r'.*')
    phone:str
    email:str
    note:str
    createdAt: int = Field(sortable=True)

    @staticmethod
    def init():
        
        Migrator().run()

