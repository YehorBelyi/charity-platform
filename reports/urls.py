from django.urls import path
from reports import views

app_name = "reports"

urlpatterns = [
    path("report/<int:report_id>/", views.report, name="report"),
    path("create/<int:announcement_id>/", views.create_report, name="create")
]