from ..models import (Waterarea)
import graphene
from .Common import QueryParmaType
class WaterareaType(graphene.ObjectType):
    pk = graphene.String()
    name = graphene.String()
    note = graphene.String()

class WaterareaInputType(graphene.InputObjectType):
    pk = graphene.String()
    name = graphene.String()
    note = graphene.String()
    
class UpdateWaterarea(graphene.Mutation):

    class Arguments:
        data = graphene.Argument(WaterareaInputType, required=True)
    ok = graphene.Boolean()
    pk = graphene.String()
    
    def mutate(root, info, data ):
        fields = data
        ok = True
        _pk = ""
        newData = {}

        print("data", data)
        try:
            if data.pk:
                newData = Waterarea.updateField(fields)
            else:
                newData = Waterarea.create(fields=fields)
            _pk = newData.pk
        except:
            print("error occured!!!!")
            ok = False
        finally:
            return UpdateWaterarea( ok=ok, pk=_pk)
        
class DeleteWaterarea(graphene.Mutation):

    class Arguments:
        pk = graphene.String()
        
    ok = graphene.Boolean()
    
    def mutate(root, info, pk):
        ok = True
        try:
            Waterarea.deleteByID(pk)        
        except Exception as e:
            ok = False
            print("error : ", e)
        return DeleteWaterarea(ok=ok)


class Query(graphene.ObjectType):
    all_waterareas = graphene.List(WaterareaType, pageSize=graphene.Int(), pageIndex=graphene.Int(), searchParams=graphene.List(QueryParmaType))
    waterarea_by_id = graphene.Field(WaterareaType, pk=graphene.String())
    @staticmethod
    def resolve_all_waterareas(root, info, pageSize, pageIndex, searchParams):

        
        query_res = Waterarea.findAll(pageSize, pageIndex, searchParams)
        return (query_res)

    @staticmethod
    def resolve_waterarea_by_id(root, info, pk):
        return Waterarea.findByID(pk)

class Mutation(graphene.ObjectType):
    update_waterarea = UpdateWaterarea.Field()
    delete_waterarea = DeleteWaterarea.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
