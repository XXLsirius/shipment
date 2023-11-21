

from redis_om import (Field,
    Migrator,
    JsonModel)

from .Common import CommonModel
import datetime

today = datetime.date.today()


class Waterarea(CommonModel):
    name:str
    note:str
    createdAt: int = Field(sortable=True)
    
    @staticmethod
    def init():
        
        Migrator().run()
        
    


        



