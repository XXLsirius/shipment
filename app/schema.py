import graphene
import app.schemas.Charterer as chartererSchema
import app.schemas.WaterArea as watreareaSchema
import app.schemas.Certificate as certificateSchema
import app.schemas.Certtype as certtypeSchema
import app.schemas.Mariner as marinerSchema
import app.schemas.Ship as shipSchema
from app.schemas.Common import QueryParmaType, CertificateType
from app.schemas.Charterer import ChartererInputType

from app.models.Certtype import Certtype
from app.models.Charterer import Charterer
from app.models.Waterarea import Waterarea
from app.models.Certificate import Certificate
from app.models.Ship import Ship
from app.models.Mariner import Mariner

from graphene_file_upload.scalars import Upload
from django.core.files.storage import FileSystemStorage


class Query(
    chartererSchema.schema.Query,
    watreareaSchema.schema.Query,
    certificateSchema.schema.Query,
    certtypeSchema.schema.Query,
    marinerSchema.schema.Query,
    shipSchema.schema.Query,
    graphene.ObjectType,
):
    # Inherits all classes and methods from app-specific queries, so no need
    # to include additional code here.
    pass
    totalCount = graphene.Field(
        graphene.Int,
        modelName=graphene.String(),
        searchParams=graphene.List(QueryParmaType),
    )
    getCertFromMariner = graphene.List(CertificateType, marinerPk=graphene.String())
    getCertFromShip = graphene.List(CertificateType, shipPk=graphene.String())

    @staticmethod
    def resolve_totalCount(root, info, modelName, searchParams):
        # _cnt = Waterarea.getTotalCount(searchParams)
        _cnt = eval(modelName + ".getTotalCount(searchParams)")
        print(_cnt)
        return _cnt

    @staticmethod
    def resolve_getCertFromShip(root, info, shipPk):
        query = [{"key": "marinerPk", "value": shipPk, "op": "equal"}]
        results = Certificate.findAll(1000, 0, query)
        return results


def resolve_upload_file(file):
    # Handle the file upload using django-upload-handler
    print(file)
    file_handler = file.file

    # Save the file to the desired location using FileField.save()
    fs = FileSystemStorage(location="./static/uploads/")
    filename = fs.save(file.name, file_handler)

    # Return the file path
    return "./static/uploads/" + filename


class UploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(root, info, file):
        resolve_upload_file(file)
        return UploadMutation(success=True)


class Mutation(
    chartererSchema.schema.Mutation,
    watreareaSchema.schema.Mutation,
    certificateSchema.schema.Mutation,
    certtypeSchema.schema.Mutation,
    marinerSchema.schema.Mutation,
    shipSchema.schema.Mutation,
    graphene.ObjectType,
):
    # Inherits all classes and methods from app-specific mutations, so no need
    # to include additional code here.
    pass
    uploadFile = UploadMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[ChartererInputType])
