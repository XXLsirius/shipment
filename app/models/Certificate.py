from redis_om import (Field,
    Migrator,
    JsonModel)

from .Common import CommonModel


class Certificate(CommonModel):
    certtypePk:str = Field(index=True)
    shipPk:str = Field(index=True)
    marinerPk:str = Field(index=True)
    kind:int = Field(index=True)
    issuePutinDate:str
    issueDepartment:str = Field(index=True)
    issueId:str
    issueDate:str
    issueExpireDate:str
    issuePrice:int
    issueRegfee:int
    issueAmount:int
    issueAccount:str
    createdAt: int = Field(sortable=True)

    @staticmethod
    def init():
        
        Migrator().run()

