from django.urls import path
from django.views.decorators.csrf import csrf_exempt
# from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("shipping", views.shipping, name="shipping"),
    path("waterArea", views.waterArea, name="waterArea"),
    path("charterer", views.charterer, name="charterer"),
    path("certificate", views.certificate, name="certificate"),
    path("certificate/edit", views.certificateEdit, name="certificateEdit"),
    path("ship", views.ship, name="ship"),
    path("ship/edit", views.shipEdit, name="shipEdit"),
    path("ship/detail", views.shipDetail, name="shipDetail"),
    path("mariner", views.mariner, name="mariner"),
    path("mariner/edit", views.marinerEdit, name="marinerEdit"),
    path("mariner/detail", views.marinerDetail, name="marinerDetail"),
    path("certType", views.certType, name="certType"),
    path("graphql", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
]
