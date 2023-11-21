from app.models import (Ship,Certificate,Certtype)

import graphene
from .Common import QueryParmaType
from .Common import CertificateType

class ShipType(graphene.ObjectType):
    pk = graphene.String()
    name = graphene.String()
    registerdDate = graphene.String()
    isRemoved = graphene.Boolean()
    removedDate = graphene.String()
    shipType = graphene.String()
    buildYear = graphene.Int()
    flag = graphene.String()
    homeport = graphene.String()
    grossTonnage = graphene.Int()
    deadWeight = graphene.Int()
    length = graphene.Int()
    beam = graphene.Int()
    depth = graphene.Int()
    draught = graphene.Int()
    note = graphene.String()
    photoUris = graphene.String()
    regNumber = graphene.String()
    callsign = graphene.String()
    imoNumber = graphene.String()

class ShipQueryType(graphene.ObjectType):
    ship = graphene.Field(lambda:ShipType)
    certificates = graphene.List(lambda:CertificateType)


class ShipInputType(graphene.InputObjectType):
    pk = graphene.String()
    name = graphene.String()
    registerdDate = graphene.String()
    isRemoved = graphene.Boolean()
    removedDate = graphene.String()
    shipType = graphene.String()
    buildYear = graphene.Int()
    flag = graphene.String()
    homeport = graphene.String()
    grossTonnage = graphene.Int()
    deadWeight = graphene.Int()
    length = graphene.Int()
    beam = graphene.Int()
    depth = graphene.Int()
    draught = graphene.Int()
    note = graphene.String()
    photoUris = graphene.String()
    regNumber = graphene.String()
    callsign = graphene.String()
    imoNumber = graphene.String()


class UpdateShip(graphene.Mutation):

    class Arguments:
        data = graphene.Argument(ShipInputType, required=True)
        
    ok = graphene.Boolean()
    pk = graphene.String()

    def mutate(root, info, data):
        fields = data
        ok = True
        pk = ""
        newData = {}
        try:
            if data.pk:
                newData = Ship.updateField(fields)
            else:
                newData = Ship.create(fields=fields)
            pk = newData.pk
        except:
            print("error occured!!!!")
            ok = False
        finally:
            return UpdateShip(ok=ok, pk=pk)

        
class DeleteShip(graphene.Mutation):

    class Arguments:
        pk = graphene.String()
        
    ok = graphene.Boolean()
    
    def mutate(root, info, pk):
        ok = True
        try:
            Ship.deleteByID(pk)        
        except Exception as e:
            ok = False
            print("error : ", e)
        return DeleteShip(ok=ok)


class Query(graphene.ObjectType):
    
    all_ships = graphene.List(ShipQueryType, pageSize=graphene.Int(), pageIndex=graphene.Int(), searchParams=graphene.List(QueryParmaType))
    ship_by_id = graphene.Field(ShipQueryType, pk=graphene.String())
    
    @staticmethod
    def resolve_all_ships(root, info, pageSize, pageIndex, searchParams):
        print(pageSize, pageIndex, searchParams)
        query_res = Ship.findAll(pageSize, pageIndex, searchParams)
        result = []
        for obj in query_res:
            ship = obj
            query = [{"key":"shipPk","value":obj.pk,"op":"equal"}]
            certificates = Certificate.findAll(1000,0,query)
            for certificate in certificates:
                print("============", certificate.certtypePk)
                certificate.certtype = Certtype.findByID(certificate.certtypePk)
            newInstance = ShipQueryType(ship=ship, certificates=certificates)
            result.append(newInstance)
        return (result)

    @staticmethod
    def resolve_ship_by_id(root, info, pk):
        ship = Ship.findByID(pk)
        query = [{"key":"shipPk","value":ship.pk,"op":"equal"}]
        certificates = Certificate.findAll(1000,0,query)
        newInstance = ShipQueryType(ship=ship, certificates=certificates)
        return (newInstance)

class Mutation(graphene.ObjectType):
    update_ship = UpdateShip.Field()
    delete_ship = DeleteShip.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
