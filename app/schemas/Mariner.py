from app.models import (Mariner, Ship,Certificate,Certtype)

import graphene
from .Common import QueryParmaType, CertificateType
from .Ship import ShipType


# ##Mariner
class MarinerType(graphene.ObjectType):
    pk = graphene.String()
    name = graphene.String()
    shipPk = graphene.String()
    birthday = graphene.String()
    duty = graphene.String()
    registerDate = graphene.String()
    isRetired = graphene.Boolean()
    retiredDate = graphene.String()
    job = graphene.String()
    dailyFee = graphene.Int()
    platoon = graphene.String()
    prevAffilication = graphene.String()
    code = graphene.String()
    mobilePhone = graphene.String()
    homePhone = graphene.String()
    graduate = graphene.String()
    graduateDate = graphene.String()
    qualGrade = graphene.String()
    boardedYears = graphene.Int()
    note = graphene.String()
    placeBorn = graphene.String()
    placeResidence = graphene.String()
    photoUris = graphene.String()


class MarinerQueryType(graphene.ObjectType):
    mariner = graphene.Field(lambda:MarinerType)
    ship = graphene.Field(lambda:ShipType)
    certificates = graphene.List(lambda:CertificateType)


class MarinerInputType(graphene.InputObjectType):
    pk = graphene.String()
    name = graphene.String()
    shipPk = graphene.String()
    birthday = graphene.String()
    duty = graphene.String()
    registerDate = graphene.String()
    isRetired = graphene.Boolean()
    retiredDate = graphene.String()
    job = graphene.String()
    dailyFee = graphene.Int()
    platoon = graphene.String()
    prevAffilication = graphene.String()
    code = graphene.String()
    mobilePhone = graphene.String()
    homePhone = graphene.String()
    graduate = graphene.String()
    graduateDate = graphene.String()
    qualGrade = graphene.String()
    boardedYears = graphene.Int()
    note = graphene.String()
    placeBorn = graphene.String()
    placeResidence = graphene.String()
    photoUris = graphene.String()

    
class UpdateMariner(graphene.Mutation):

    class Arguments:
        data = graphene.Argument(MarinerInputType, required=True)
        
    ok = graphene.Boolean()
    pk = graphene.String()

    @staticmethod
    def mutate(root, info, data):
        fields = data
        ok = True
        pk = ""
        newData = {}
        try:
            if data.pk:
                newData = Mariner.updateField(fields)
            else:
                newData = Mariner.create(fields=fields)
            pk = newData.pk
        except:
            print("error occured!!!!")
            ok = False
        finally:
            return UpdateMariner(ok=ok, pk=pk)

        
class DeleteMariner(graphene.Mutation):

    class Arguments:
        pk = graphene.String()
        
    ok = graphene.Boolean()
    
    def mutate(root, info, pk):
        ok = True
        try:
            Mariner.deleteByID(pk)        
        except Exception as e:
            ok = False
            print("error : ", e)
        return DeleteMariner(ok=ok)


class Query(graphene.ObjectType):
    
    all_mariners = graphene.List(MarinerQueryType, pageSize=graphene.Int(), pageIndex=graphene.Int(), searchParams=graphene.List(QueryParmaType))
    mariner_by_id = graphene.Field(MarinerQueryType, pk=graphene.String())

    @staticmethod
    def resolve_all_mariners(root, info, pageSize, pageIndex, searchParams):
        query_res = Mariner.findAll(pageSize, pageIndex, searchParams)
        print('>?>>>>>>>>>>>>', searchParams)
        result = []
        for obj in query_res:
            mariner = obj
            ship = Ship.findByID(obj.shipPk)
            query = [{"key":"marinerPk","value":obj.pk,"op":"equal"}]
            certificates = Certificate.findAll(1000,0,query)

            print(certificates)
            for certificate in certificates:
                certificate.certtype = Certtype.findByID(certificate.certtypePk)

            
            newmarinerQueryType = MarinerQueryType(mariner=mariner, ship=ship,certificates=certificates)
            result.append(newmarinerQueryType)
        return (result)

    @staticmethod
    def resolve_mariner_by_id(root, info, pk):
        print("dfafasdfasdf")

        mariner = Mariner.findByID(pk)
        ship = Ship.findByID(mariner.shipPk)
        newmarinerQueryType = MarinerQueryType(mariner=mariner, ship=ship)
        return newmarinerQueryType

class Mutation(graphene.ObjectType):
    update_mariner = UpdateMariner.Field()
    delete_mariner = DeleteMariner.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
