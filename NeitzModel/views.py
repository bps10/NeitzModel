from django.template import RequestContext, loader
from django.http import HttpResponse
#from django.utils import simplejson

# eschaton imports
from eschaton.eschaton import eye
from eschaton.eschaton.cones import dogRFields as df
from eschaton.eschaton.scene import powerlaw

schemEye = eye.eyeModel.SchematicEye().returnOSLOdata()
powerlaw = powerlaw.normPowerlaw


def getRField(freqs=schemEye['freqs'], cone_spacing=2.0):
    coneDOG = df.genReceptiveFields(freqs, cone_spacing)
    # DoG receptive field:
    DOG = coneDOG['dog'].tolist()
    DOG_xvals = coneDOG['xvals'].tolist()
    DOG_fft = coneDOG['fft'][:].tolist()
    return DOG, DOG_xvals, DOG_fft


# optics:
def getMTF(axis, objDist):

    return schemEye[axis][objDist][:].tolist()


def formatPost(optic):

    return optic.split(" : ")


opticsDiff = getMTF('onAxis', 'diffract')


# image, powerlaw:
def getPowerlaw(xlen=60, exponent=2):

    return powerlaw(xlen, exponent)


# processing:
def arrayMultiply(inputA, inputB):

    output = []
    for i in range(len(inputA)):
        output.append(inputA[i] * inputB[i])
    return output


# view
def index(request):
    t = loader.get_template('index.html')

    if request.method == 'GET':
        # power law and MTFs
        power = 2
        coneInput = 2
        MTF_A = getMTF('onAxis', '1m')
        MTF_B = getMTF('onAxis', '20ft')
        powLaw = getPowerlaw(power)

        # compute stats at retina:
        retPowDiffract = arrayMultiply(opticsDiff[1:], getPowerlaw())
        retPowOpt1 = arrayMultiply(MTF_A[1:], getPowerlaw())
        retPowOpt2 = arrayMultiply(MTF_B[1:], getPowerlaw())
        # compute cone activity:
        DOG, DOG_xvals, DOG_fft = getRField(cone_spacing=2.0)
        conePowDiffract = arrayMultiply(retPowDiffract[1:], DOG_fft)
        conePowOpt1 = arrayMultiply(retPowOpt1[1:], DOG_fft)
        conePowOpt2 = arrayMultiply(retPowOpt2[1:], DOG_fft)

        # integrate activity:
        coneActivity = [round(sum(conePowDiffract), 4),
                        round(sum(conePowOpt1), 4),
                        round(sum(conePowOpt2), 4)]

        c = RequestContext(request,
                           {'opticDict': schemEye,
                           'optic1': 'onAxis : 1m',
                           'optic2': 'onAxis : 20ft',
                           'powerOpt': power,
                           'coneOpt': coneInput,
                           'MTF_Dif': opticsDiff,
                           'MTF_A': MTF_A,
                           'MTF_B': MTF_B,
                           'DOG': DOG,
                           'DOG_xvals': DOG_xvals,
                           'DOG_fft': DOG_fft,
                           'powerLaw': powLaw,
                           'retPowDiffract': retPowDiffract,
                           'retPowOpt1': retPowOpt1,
                           'retPowOpt2': retPowOpt2,
                           'conePowDiffract': conePowDiffract,
                           'conePowOpt1': conePowOpt1,
                           'conePowOpt2': conePowOpt2,
                           'coneActivity': coneActivity, })

    if request.method == 'POST':
        try:
            # get and format form input:
            power = float(request.POST['powerInput'])
            coneInput = float(request.POST['coneInput'])
            print coneInput
            optic1 = request.POST['optic1']
            optic1 = formatPost(optic1)
            optic2 = request.POST['optic2']
            optic2 = formatPost(optic2)

            # power law and MTFs
            MTF_A = getMTF(optic1[0], optic1[1])
            MTF_B = getMTF(optic2[0], optic2[1])
            powLaw = getPowerlaw(exponent=power)

            # compute stats at retina:
            retPowDiffract = arrayMultiply(opticsDiff[1:],
                 getPowerlaw(60, power))
            retPowOpt1 = arrayMultiply(MTF_A[1:], getPowerlaw(60, power))
            retPowOpt2 = arrayMultiply(MTF_B[1:], getPowerlaw(60, power))
            # compute cone activity:
            DOG, DOG_xvals, DOG_fft = getRField(cone_spacing=coneInput)
            conePowDiffract = arrayMultiply(retPowDiffract[1:], DOG_fft)
            conePowOpt1 = arrayMultiply(retPowOpt1[1:], DOG_fft)
            conePowOpt2 = arrayMultiply(retPowOpt2[1:], DOG_fft)

            # integrate activity:
            coneActivity = [round(sum(conePowDiffract), 4),
                            round(sum(conePowOpt1), 4),
                            round(sum(conePowOpt2), 4)]

            c = RequestContext(request,
                               {'opticDict': schemEye,
                               'optic1': request.POST['optic1'],
                               'optic2': request.POST['optic2'],
                               'powerOpt': power,
                               'coneOpt': coneInput,
                               'MTF_Dif': opticsDiff,
                               'MTF_A': MTF_A,
                               'MTF_B': MTF_B,
                               'DOG': DOG,
                               'DOG_xvals': DOG_xvals,
                               'DOG_fft': DOG_fft,
                               'powerLaw': powLaw,
                               'retPowDiffract': retPowDiffract,
                               'retPowOpt1': retPowOpt1,
                               'retPowOpt2': retPowOpt2,
                               'conePowDiffract': conePowDiffract,
                               'conePowOpt1': conePowOpt1,
                               'conePowOpt2': conePowOpt2,
                               'coneActivity': coneActivity, })

        except:
            print 'nope'

    return HttpResponse(t.render(c))
