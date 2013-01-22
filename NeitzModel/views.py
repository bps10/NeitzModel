from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils import simplejson

from eschaton.eschaton import eye
schemEye = eye.eyeModel.SchematicEye().returnOSLOdata()

optics = schemEye['onAxis']['diffract'].tolist()
opticsA = schemEye['onAxis']['1m'].tolist()
opticsB = schemEye['onAxis']['20ft'].tolist()

def index(request):
    t = loader.get_template('index.html')
    c = RequestContext(request,{'opticDict':schemEye,
                                'MTF_Dif':optics,
                                'MTF_A':opticsA,
                                'MTF_B':opticsB,})
    return HttpResponse(t.render(c))
