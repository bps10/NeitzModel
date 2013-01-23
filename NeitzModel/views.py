from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils import simplejson

from eschaton.eschaton import eye, cones
schemEye = eye.eyeModel.SchematicEye().returnOSLOdata()
coneDOG = cones.dogRFields.ConeReceptiveFields(schemEye['freqs']).returnReceptiveField()

DOG = coneDOG['dog']['periph'].tolist()
DOG_xvals = coneDOG['xvals'].tolist()

# diffraction optics:
opticsDiff = schemEye['onAxis']['diffract'].tolist()

# optional optics:
def getMTF(axis,objDist):
    return schemEye[axis][objDist].tolist()

def formatPost(optic):
    return optic.split(" : ")


def index(request):
    t = loader.get_template('index.html')
    
    if request.method == 'GET':
        
        c = RequestContext(request,{'opticDict':schemEye,
                           'MTF_Dif':opticsDiff,
                           'MTF_A':getMTF('onAxis','1m'),
                           'MTF_B':getMTF('onAxis','20ft'),
                           'DOG': DOG,
                           'DOG_xvals':DOG_xvals,})

    if request.method == 'POST':
        try:
            coneInput = request.POST['coneInput']
            optic1 = request.POST['optic1']
            optic1 = formatPost(optic1)
            optic2 = request.POST['optic2']
            optic2 = formatPost(optic2)
                    
            c = RequestContext(request,{'opticDict':schemEye,
                               'MTF_Dif':opticsDiff,
                               'MTF_A':getMTF(optic1[0],optic1[1]),
                               'MTF_B':getMTF(optic2[0],optic2[1]),
                               'DOG': DOG,
                               'DOG_xvals':DOG_xvals,})

        except:
            print 'nope'
        #return HttpResponse('not quite yet')

    return HttpResponse(t.render(c))
