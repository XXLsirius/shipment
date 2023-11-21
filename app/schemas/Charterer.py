from ..models import (Charterer)
import graphene
from .Common import QueryParmaType
class ChartererType(graphene.ObjectType):
    pk = graphene.String()
    company = graphene.String()
    nation = graphene.String()
    phone = graphene.String()
    email = graphene.String()
    note = graphene.String()

class ChartererInputType(graphene.InputObjectType):
    pk = graphene.String()
    company = graphene.String()
    nation = graphene.String()
    phone = graphene.String()
    email = graphene.String()
    note = graphene.String()
    
class UpdateCharterer(graphene.Mutation):

    class Arguments:
        data = graphene.Argument(ChartererInputType, required=True)
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
                newData = Charterer.updateField(fields)
            else:
                newData = Charterer.create(fields=fields)
            _pk = newData.pk
        except:
            print("error occured!!!!")
            ok = False
        finally:
            return UpdateCharterer( ok=ok, pk=_pk)
        
class DeleteCharterer(graphene.Mutation):

    class Arguments:
        pk = graphene.String()
        
    ok = graphene.Boolean()
    
    def mutate(root, info, pk):
        ok = True
        try:
            Charterer.deleteByID(pk)        
        except Exception as e:
            ok = False
            print("error : ", e)
        return DeleteCharterer(ok=ok)


class Query(graphene.ObjectType):
    all_charterers = graphene.List(ChartererType, pageSize=graphene.Int(), pageIndex=graphene.Int(), searchParams=graphene.List(QueryParmaType))
    charterer_by_id = graphene.Field(ChartererType, pk=graphene.String())
    @staticmethod
    def resolve_all_charterers(root, info, pageSize, pageIndex, searchParams):

        
        query_res = Charterer.findAll(pageSize, pageIndex, searchParams)
        return (query_res)

    @staticmethod
    def resolve_charterer_by_id(root, info, pk):
        return Charterer.findByID(pk)

class Mutation(graphene.ObjectType):
    update_charterer = UpdateCharterer.Field()
    delete_charterer = DeleteCharterer.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
