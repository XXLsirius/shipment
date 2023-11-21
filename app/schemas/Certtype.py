from app.models import (Certtype)
import graphene
from .Common import QueryParmaType
from .Common import CerttypeType
import datetime

class CerttypeInputType(graphene.InputObjectType):
    pk = graphene.String()
    name = graphene.String()
    agency = graphene.String()
    note = graphene.String()
    kind = graphene.Int()


class UpdateCerttype(graphene.Mutation):

    class Arguments:
        data = graphene.Argument(CerttypeInputType, required=True)
        
    ok = graphene.Boolean()
    pk = graphene.String()
    
    def mutate(root, info, data):
        fields = data
        ok = True
        pk = ""
        newData = {}
        try:
            print("fields:", fields)
            if data.pk:
                newData = Certtype.updateField(fields)
            else:
                newData = Certtype.create(fields=fields)
            pk = newData.pk
        except:
            print("error occured!!!!")
            ok = False
        finally:
            return UpdateCerttype(ok=ok, pk=pk)

        
class DeleteCerttype(graphene.Mutation):

    class Arguments:
        pk = graphene.String()
        
    ok = graphene.Boolean()
    
    def mutate(root, info, pk):
        ok = True
        try:
            Certtype.deleteByID(pk)        
        except Exception as e:
            ok = False
            print("error : ", e)
        return DeleteCerttype(ok=ok)


class Query(graphene.ObjectType):
    all_certtypes = graphene.List(CerttypeType, pageSize=graphene.Int(), pageIndex=graphene.Int(), searchParams=graphene.List(QueryParmaType))
    certById = graphene.Field(CerttypeType, pk=graphene.String())
 
    @staticmethod
    def resolve_all_certtypes(root, info, pageSize, pageIndex, searchParams):
        query_res = Certtype.findAll(pageSize, pageIndex, searchParams)
        return (query_res)

    @staticmethod
    def resolve_certById(root, info, pk):

        print('>>>>>>>>>>>>>>sss>', pk)
        return Certtype.findByID(pk)


class Mutation(graphene.ObjectType):
    update_certtype = UpdateCerttype.Field()
    delete_certtype = DeleteCerttype.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
