from django.template import RequestContext, loader
from django.http import HttpResponse

from eschaton.eschaton import eye
schemEye = eye.eyeModel.SchematicEye().returnOSLOdata()


def index(request):
    t = loader.get_template('index.html')
    c = RequestContext(request,{'opticDict':schemEye,})
    return HttpResponse(t.render(c))
