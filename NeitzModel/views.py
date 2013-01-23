from django.template import RequestContext, loader
from django.http import HttpResponse
from django.utils import simplejson

# eschaton imports
from eschaton.eschaton import eye, cones
from eschaton.eschaton.scene import powerlaw

schemEye = eye.eyeModel.SchematicEye().returnOSLOdata()
coneDOG = cones.dogRFields.ConeReceptiveFields(schemEye['freqs']).returnReceptiveField()
powerlaw = powerlaw.normPowerlaw

# DoG receptive field:
DOG = coneDOG['dog']['periph'].tolist()
DOG_xvals = coneDOG['xvals'].tolist()
DOG_fft = coneDOG['RField']['fft']['periph'][1:].tolist()


# optics:
def getMTF(axis,objDist):
    return schemEye[axis][objDist].tolist()

def formatPost(optic):
    return optic.split(" : ")
opticsDiff = getMTF('onAxis','diffract')


# image, powerlaw:
def getPowerlaw(exponent=2):
    xlen = len(getMTF('onAxis','1m'))
    return powerlaw(xlen, exponent)


# view
def index(request):
    t = loader.get_template('index.html')
    
    if request.method == 'GET':
        
        c = RequestContext(request,
                           {'opticDict':schemEye,
                           'optic1': 'farPeriph : 40deg',
                           'optic2': 'farPeriph : 20deg',
                           'MTF_Dif':opticsDiff,
                           'MTF_A':getMTF('onAxis','1m'),
                           'MTF_B':getMTF('onAxis','20ft'),
                           'DOG': DOG,
                           'DOG_xvals':DOG_xvals,
                           'DOG_fft': DOG_fft,
                           'powerLaw': getPowerlaw()})

    if request.method == 'POST':
        try:
            coneInput = request.POST['coneInput']
            optic1 = request.POST['optic1']
            optic1 = formatPost(optic1)
            optic2 = request.POST['optic2']
            optic2 = formatPost(optic2)
                    
            c = RequestContext(request,
                               {'opticDict':schemEye,
                               'optic1': request.POST['optic1'],
                               'optic2': request.POST['optic2'],
                               'MTF_Dif':opticsDiff,
                               'MTF_A':getMTF(optic1[0],optic1[1]),
                               'MTF_B':getMTF(optic2[0],optic2[1]),
                               'DOG': DOG,
                               'DOG_xvals': DOG_xvals,
                               'DOG_fft': DOG_fft,
                               'powerLaw': getPowerlaw()})

        except:
            print 'nope'
        #return HttpResponse('not quite yet')

    return HttpResponse(t.render(c))
