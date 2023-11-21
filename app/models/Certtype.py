from redis_om import (Field,
    Migrator,
    JsonModel)

from .Common import CommonModel

class Certtype(CommonModel):
    name:str
    agency:str
    note:str
    kind:int = Field(index=True)
    createdAt: int = Field(sortable=True)

    @staticmethod
    def init():
        
        Migrator().run()

