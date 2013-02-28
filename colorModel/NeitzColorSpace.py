# -*- coding: utf-8 *-*
from __future__ import division
import numpy as np

from spectsens import spectsens

from NeitzModel import settings
## todo:: Create a logging function.

class colorSpace(object):
    '''
    '''
    def __init__(self, stim='wright', fundamental='neitz', 
                 LMSpeaks=[559.0, 530.0, 421.0]):
        
        if (stim.lower() != 'wright' and stim.lower() != 'stockman' 
            and stim.lower() != 'cie'):
            print 'Sorry, stim light not understood, using wright'
            stim = 'wright' 

        if stim.lower() == 'wright':
            self.lights = {
                            'l': 650.0,
                            'm': 530.0,
                            's': 460.0,
                           }
        if stim.lower() == 'stockman':
            self.lights = {'l': 645.0, 
                           'm': 526.0, 
                           's': 444.0, }

        if stim.lower() == 'cie' or stim.lower() == 'cie 1932':
            self.lights = {'l': 700.0, 
                           'm': 546.1, 
                           's': 435.8, }
                           
        self.params = {'lights': stim.lower, }
        
        self.genStockmanFilter()
        self.genLMS(fundamental, LMSpeaks)
        self.genConvMatrix()
        
        self.LMStoCMFs()
        self.CMFtoEE_CMF()
        self.EE_CMFtoRGB()
        
    def genLMS(self, fundamental, LMSpeaks):
        '''
        '''
        if len(LMSpeaks) != 3:
            print 'LMSpeaks must be length 3! Using defaults: 559, 530, 417nm'
            LMSpeaks = [559.0, 530.0, 421.0]
        
        if fundamental.lower() == 'stockman':
            ind = len(self.spectrum)
            foo = np.genfromtxt(settings.STATIC_ROOT + 
                                    '/stockman/fundamentals2deg.csv', 
                                 delimiter=',')[::10, :]
            self.Lc = 10.0 ** foo[:ind, 1]
            self.Mc = 10.0 ** foo[:ind, 2]
            self.Sc = 10.0 ** foo[:ind, 3]
    
            Lresponse = self.Lc * self.spectrum
            Mresponse = self.Mc * self.spectrum
            Sresponse = self.Sc * self.spectrum
            
        elif fundamental.lower() == 'stockspecsens':
            ind = len(self.spectrum)
            foo = np.genfromtxt(settings.STATIC_ROOT + 
                                    '/stockman/specSens.csv', 
                                delimiter=',')[::10, :]

            LS = np.log10((1.0 - 10.0 ** -((10.0 ** foo[:, 1]) *
                    0.5)) / (1.0 - 10 ** -0.5))
            MS = np.log10((1.0 - 10.0 ** -((10.0 ** foo[:, 2]) *
                    0.5)) / (1.0 - 10 ** -0.5))
            SS = np.log10((1.0 - 10.0 ** -((10.0 ** foo[:, 3]) *
                    0.5)) / (1.0 - 10 ** -0.4))
          
            self.Lc = 10.0 ** LS[:ind]
            self.Mc = 10.0 ** MS[:ind]
            self.Sc = 10.0 ** SS[:ind]
            
            Lresponse = self.Lc / self.filters * self.spectrum
            Mresponse = self.Mc / self.filters * self.spectrum
            Sresponse = self.Sc / self.filters * self.spectrum
            
        elif fundamental.lower() == 'neitz':
            minspec = min(self.spectrum)
            maxspec = max(self.spectrum)
            self.Lc = spectsens(LMSpeaks[0], 0.5, 'anti-log', minspec, 
                                             maxspec, 1)[1]
            self.Mc = spectsens(LMSpeaks[1], 0.5, 'anti-log', minspec, 
                                             maxspec, 1)[1]
            self.Sc = spectsens(LMSpeaks[2], 0.4, 'anti-log', minspec, 
                                             maxspec, 1)[1]
                                                         
            Lresponse = self.Lc / self.filters * self.spectrum
            Mresponse = self.Mc / self.filters * self.spectrum
            Sresponse = self.Sc / self.filters * self.spectrum
        
        #record param
        self.params['fundamentals'] = fundamental
        self.params['LMSpeaks']= LMSpeaks
        
        self.Lnorm = Lresponse / np.max(Lresponse)
        self.Mnorm = Mresponse / np.max(Mresponse)
        self.Snorm = Sresponse / np.max(Sresponse)

    def TrichromaticEquation(self, r, g, b):
        '''
        '''
        rgb = r + g + b
        r_ = r / rgb
        g_ = g / rgb
        b_ = b / rgb
        
        return r_, g_, b_

    def genStockmanFilter(self, maxLambda=770):
        '''
        '''
        lens = np.genfromtxt(settings.STATIC_ROOT + '/stockman/lens.csv', 
                             delimiter=',')[::10, :]
        macula = np.genfromtxt(settings.STATIC_ROOT + 
                                '/stockman/macular.csv', 
                                delimiter=',')[::10, :]

        spectrum = lens[:, 0]
        ind = np.where(spectrum == maxLambda)[0]
        self.spectrum = spectrum[:ind+1]
        
        self.filters = 10.0 ** (lens[:ind+1, 1] +  macula[:ind+1, 1])
        
    def LMStoCMFs(self):
        '''
        '''
        
        LMSsens = np.array([self.Lnorm.T, self.Mnorm.T, self.Snorm.T])
        self.CMFs = np.dot(np.linalg.inv(self.convMatrix), LMSsens)
        
        #save sums for later normalization:
            
        Rnorm = sum(self.CMFs[0, :])
        Gnorm = sum(self.CMFs[1, :])
        Bnorm = sum(self.CMFs[2, :])
        self.EEfactors = {'r': Rnorm, 'g': Gnorm, 'b': Bnorm, }
        
    def genConvMatrix(self, PRINT=False):
        '''
        '''
        self.convMatrix = np.array([
            [np.interp(self.lights['l'], self.spectrum, self.Lnorm),
            np.interp(self.lights['m'], self.spectrum, self.Lnorm),
            np.interp(self.lights['s'], self.spectrum, self.Lnorm)],

            [np.interp(self.lights['l'], self.spectrum, self.Mnorm),
            np.interp(self.lights['m'], self.spectrum, self.Mnorm),
            np.interp(self.lights['s'], self.spectrum, self.Mnorm)],

            [np.interp(self.lights['l'], self.spectrum, self.Snorm),
            np.interp(self.lights['m'], self.spectrum, self.Snorm),
            np.interp(self.lights['s'], self.spectrum, self.Snorm)]])

        if PRINT == True:
            print self.convMatrix
        
    def CMFtoEE_CMF(self):
        '''
        '''
        self.CMFs[0, :], self.CMFs[1, :], self.CMFs[2, :] = self._EEcmf(
                                        self.CMFs[0, :], 
                                        self.CMFs[1, :], 
                                        self.CMFs[2, :])

    def EE_CMFtoRGB(self):
        '''
        '''
        self.rVal, self.gVal, self.bVal = self.TrichromaticEquation(
                            self.CMFs[0, :], self.CMFs[1, :], self.CMFs[2, :])

    def find_copunctuals(self):
        '''
        '''
        protan = self.find_rgb(np.array([1, 0, 0]))
        deutan = self.find_rgb(np.array([0, 1, 0]))
        tritan = self.find_rgb(np.array([0, 0, 1]))
        
        self.copunctuals = {'protan': protan, 
                            'deutan': deutan, 
                            'tritan': tritan, }
    
    def find_testLightMatch(self, testLight=600):
        '''
        '''
        l_ = np.interp(testLight, self.spectrum, self.Lnorm)
        m_ = np.interp(testLight, self.spectrum, self.Mnorm)
        s_ = np.interp(testLight, self.spectrum, self.Snorm)

        rOut, gOut, bOut = self.find_rgb(LMS=np.array([l_, m_, s_]))

        return [rOut, gOut, bOut]        
        
    def find_neitzMatch(self, testLight=500):
        '''
        '''
        r_, g_, b_ = self.find_testLightMatch(testLight)
        print r_, g_, b_

        xOut = r_
        k = self._solve(g_, b_)
        print 'k: ', k       
        yOut = k * g_ + b_

        print xOut, yOut
        
    def find_rgb(self, LMS):
        '''
        '''
        cmf = np.dot(np.linalg.inv(self.convMatrix), LMS)
        cmf[0], cmf[1], cmf[2] = self._EEcmf(cmf[0], cmf[1], cmf[2])
        out = self.TrichromaticEquation(cmf[0], cmf[1], cmf[2])
        return out
        
    def returnConvMat(self):
        '''
        '''
        return self.convMatrix
    
    def returnCMFs(self):
        '''
        '''
        return {'cmfs': self.CMFs, 'wavelengths': self.spectrum, }
    
    def return_rgb(self):
        '''
        '''
        return {'r': self.rVal, 'g': self.gVal, 'b': self.bVal, }

    def _EEcmf(self, r_, g_, b_):   
        '''
        '''
        
        r_ *= 100. / self.EEfactors['r'] 
        g_ *= 100. / self.EEfactors['g']
        b_ *= 100. / self.EEfactors['b']
        
        return [r_, g_, b_]
        
    def _solve(self, g, b):
        k = (g - b) / g
        check = (k * g) + b - g
        if check < 10e-10:
            return k
        else:
            raise IOError('equation was not solved correctly')

        
if __name__ == '__main__':
    color = colorSpace()
    
    #color.plotCompare()
    #color.plotFilters()
    #color.plotSpecSens()
    #color.plotCMFs()
    #color.plotcoeff()
    #color.plotColorSpace()
    color.plotConfusionLines()
    