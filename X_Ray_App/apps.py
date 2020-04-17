import os
import importlib.util

from django.apps import AppConfig
from django.conf import settings
from keras.models import load_model

class XRayAppConfig(AppConfig):
    name = 'X_Ray_App'
    MODEL = 'cnn_model.h5'
    METRICS_MODULE = 'metrics.py'
    LABEL_MAP = {0: 'No pneumonia', 1: 'Pneumonia'}

    # import custom metric
    metrics_path = os.path.join(settings.ML_MODELS, METRICS_MODULE)
    mod_spec = importlib.util.spec_from_file_location(METRICS_MODULE, metrics_path) #import_module('.ml_models.metrics', package=__package__)
    metrics_module = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(metrics_module)
    F1 = getattr(metrics_module, 'F1')

    # import model
    model_path = os.path.join(settings.ML_MODELS, MODEL)
    cnn_model = load_model(model_path, custom_objects={'F1': F1})
