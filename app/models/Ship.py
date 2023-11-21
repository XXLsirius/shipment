from redis_om import (Field,
    Migrator,
    JsonModel)

from .Common import CommonModel


class Ship(CommonModel):
    name:str
    registerdDate:str
    isRemoved:bool
    removedDate:str
    shipType:str
    buildYear:int
    flag:str
    homeport:str
    grossTonnage:int
    deadWeight:int
    length:int
    beam:int
    depth:int
    draught:int
    note:str
    photoUris:str
    regNumber:str
    callsign:str
    imoNumber:str
    createdAt: int = Field(sortable=True)
    
    @staticmethod
    def init():
        Migrator().run()

