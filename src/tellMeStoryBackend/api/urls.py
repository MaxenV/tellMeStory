from django.urls import path

from .views import (
    ModelAllView,
    ModelRunningView,
    ModelRunView,
    ModelStopView,
    PresentView,
    ResponseView,
)

urlpatterns = [
    path("present", PresentView.as_view(), name="present"),
    path("model/all", ModelAllView.as_view(), name="model_all"),
    path("model/running", ModelRunningView.as_view(), name="model_running"),
    path("model/run", ModelRunView.as_view(), name="model_run"),
    path("model/stop", ModelStopView.as_view(), name="model_stop"),
    path("response", ResponseView.as_view(), name="response"),
]
