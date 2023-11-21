from app.models import (Certificate, Mariner, Certtype, Ship)
import graphene
from .Common import QueryParmaType
from .Mariner import MarinerType
from .Ship import ShipType
from .Certtype import CerttypeType
from .Common import CertificateType

class CertificateQueryType(graphene.ObjectType):
    certificate = graphene.Field(lambda:CertificateType)
    ship = graphene.String()
    mariner = graphene.String()
    certtype = graphene.Field(lambda:CerttypeType)


class CertificateInputType(graphene.InputObjectType):
    pk = graphene.String()
    certtypePk = graphene.String()
    shipPk = graphene.String()
    marinerPk = graphene.String()
    kind = graphene.Int()
    issuePutinDate = graphene.String()
    issueDepartment = graphene.String()
    issueId = graphene.String()
    issueDate = graphene.String()
    issueExpireDate = graphene.String()
    issueAccount = graphene.String()
    issuePrice = graphene.Int()
    issueRegfee = graphene.Int()
    issueAmount = graphene.Int()

    
class UpdateCertificate(graphene.Mutation):

    class Arguments:
        data = graphene.Argument(CertificateInputType, required=True)
        
    ok = graphene.Boolean()
    pk = graphene.String()
    
    def mutate(root, info, data):
        fields = data
        ok = True
        pk = ""
        newData = {}
        try:
            if data.pk:
                newData = Certificate.updateField(fields)
            else:
                newData = Certificate.create(fields=fields)
            pk = newData.pk
        except:
            print("error occured!!!!")
            ok = False
        finally:
            return UpdateCertificate(ok=ok, pk=pk)

        
class DeleteCertificate(graphene.Mutation):

    class Arguments:
        pk = graphene.String()
        
    ok = graphene.Boolean()
    
    def mutate(root, info, pk):
        ok = True
        try:
            Certificate.deleteByID(pk)        
        except Exception as e:
            ok = False
            print("error : ", e)
        return DeleteCertificate(ok=ok)


class Query(graphene.ObjectType):
    
    all_certificate = graphene.List(CertificateQueryType, pageSize=graphene.Int(), pageIndex=graphene.Int(), searchParams=graphene.List(QueryParmaType))
    certificate_by_id = graphene.Field(CertificateQueryType, pk=graphene.String())
 
    @staticmethod
    def resolve_all_certificate(root, info, pageSize, pageIndex, searchParams):
        query_res = Certificate.findAll(pageSize, pageIndex, searchParams)
        result = []
        for obj in query_res:
            certificate = obj
            try:

                ship = Ship.findByID(certificate.shipPk).name
            except Exception as e:
                ship = ""
            try:
                mariner = Mariner.findByID(certificate.marinerPk).name
            except Exception as e:
                mariner = ""
            
            certtype = Certtype.findByID(certificate.certtypePk)
            newInstance = CertificateQueryType(certificate=certificate, mariner=mariner, ship=ship, certtype=certtype)
            result.append(newInstance)
        return (result)

    @staticmethod
    def resolve_certificate_by_id(root, info, pk):
        certificate = Certificate.findByID(pk)
        if (certificate is not None):

            try:
                ship = Ship.findByID(certificate.shipPk).name
            except Exception as e:
                ship = ""
            try:
                mariner = Mariner.findByID(certificate.marinerPk).name
            except Exception as e:
                mariner = ""
            certtype = Certtype.findByID(certificate.certtypePk)
            newInstance = CertificateQueryType(certificate=certificate, mariner=mariner, ship=ship, certtype=certtype)
            return newInstance


class Mutation(graphene.ObjectType):
    update_certificate = UpdateCertificate.Field()
    delete_certificate = DeleteCertificate.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
