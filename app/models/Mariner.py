from redis_om import (Field,
    Migrator,
    JsonModel)

from .Common import CommonModel


class Mariner(CommonModel):
    name:str = Field(index=True, full_text_search=True, regex=r'.*')
    shipPk:str = Field(index=True, full_text_search=True, regex=r'.*')
    birthday:str
    duty:str
    registerDate:str
    isRetired:bool
    retiredDate:str
    job:str
    dailyFee:int
    platoon:str
    prevAffilication:str
    code:str
    mobilePhone:str
    homePhone:str
    graduate:str
    graduateDate:str
    qualGrade:str
    boardedYears:int
    note:str
    placeBorn:str
    placeResidence:str
    photoUris:str
    createdAt: int = Field(sortable=True)

    @staticmethod
    def init():
        
        Migrator().run()

