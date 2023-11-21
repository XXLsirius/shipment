import graphene

class QueryParmaType(graphene.InputObjectType):
    key = graphene.String()
    value = graphene.String()
    op = graphene.String()

# ##Certtype
class CerttypeType(graphene.ObjectType):
    pk = graphene.String()
    name = graphene.String()
    agency = graphene.String()
    note = graphene.String()
    kind = graphene.Int()

class CertificateType(graphene.ObjectType):
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

    certtype = graphene.Field(lambda:CerttypeType)



