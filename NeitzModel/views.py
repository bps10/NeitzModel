from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils import simplejson

from eschaton.eschaton import eye
schemEye = eye.eyeModel.SchematicEye().returnOSLOdata()

array = schemEye['farPeriph']['40deg'].tolist()

def index(request):
    t = loader.get_template('index.html')
    c = RequestContext(request,{'opticDict':schemEye,'MTF':array})
    return HttpResponse(t.render(c))
