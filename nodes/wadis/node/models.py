from model.fake import *
from model.atmos import *
from model.saga import *
#See django/db/models/base.py in 52 (app_label = model_module.__name__.split('.')[-2]) because the table cache is made by app_label.
import model.h2o.saga2 as saga2
import model.co2.saga2_co2 as saga2_co2
import model.co.saga2_co as saga2_co
import model.n2o.saga2_n2o as saga2_n2o
import model.c2h2.saga2_c2h2 as saga2_c2h2

