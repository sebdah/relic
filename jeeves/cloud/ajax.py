import models
import time
from dajax.core import Dajax
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def start_instance(request, instance_id):
    instance = models.Instance.objects.get(id = instance_id)
    instance.start_instance()
    return simplejson.dumps({'message': 'Started instance'})

@dajaxice_register
def start_instance_mockup(request, instance_id):
    dajax = Dajax()
    dajax.assign('#apa', 'innerHTML', 'Loading..')
    time.sleep(2)
    return simplejson.dumps({'message': 'Started instance'})

@dajaxice_register
def terminate_instance(request, instance_id):
    instance = models.Instance.objects.get(id = instance_id)
    instance.terminate_instance()
    return simplejson.dumps({'message': 'Terminated instance'})
