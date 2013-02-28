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

    def plotCompare(self, compare=['stockman', 'stockSpecSens', 'neitz']):
        '''
        '''
        try:
            plt.__version__
        except NameError:
            import PlottingFun as pf
            import matplotlib.pylab as plt
            
        self.genStockmanFilter()
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        pf.AxisFormat()
        pf.TufteAxis(ax, ['left', 'bottom'], Nticks=[5, 5])
        style = ['-', '--', '-.']
        for i, condition in enumerate(compare):
            print condition
            self.genLMS(fund=condition)
            
            ax.plot(self.spectrum, self.Lnorm, 'r' + style[i], linewidth=2)
            ax.plot(self.spectrum, self.Mnorm, 'g' + style[i], linewidth=2)
            ax.plot(self.spectrum, self.Snorm, 'b' + style[i], linewidth=2)
        #ax.set_ylim([-0.01, 1.01])
        ax.set_xlim([380, 781])
        ax.set_xlabel('wavelength (nm)')
        ax.set_ylabel('sensitivity')        
        plt.tight_layout()
        plt.show()
            
    def plotFilters(self):
        '''
        '''
        try:
            plt.__version__
        except NameError:
            import PlottingFun as pf
            import matplotlib.pylab as plt
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        pf.AxisFormat()
        pf.TufteAxis(ax, ['left', 'bottom'], Nticks=[5, 5])
        ax.semilogy(self.spectrum, self.filters, 'k', linewidth=2)
        ax.set_ylabel('log density')
        ax.set_xlabel('wavelength (nm)')
        ax.set_xlim([380, 781])
        ax.set_ylim([0.9, max(self.filters)])
        plt.tight_layout()
        plt.show()

    def plotSpecSens(self):
        '''
        '''
        try:
            plt.show()
        except NameError:
            import PlottingFun as pf
            import matplotlib.pylab as plt 
            
        fig = plt.figure()
        ax = fig.add_subplot(111)
        pf.AxisFormat()
        pf.TufteAxis(ax, ['left', 'bottom'], Nticks=[5, 5])
        ax.plot(self.spectrum, self.Lnorm, 'r', linewidth=4)
        ax.plot(self.spectrum, self.Lc, 'r--', linewidth=2)
        ax.plot(self.spectrum, self.Mnorm, 'g', linewidth=4)
        ax.plot(self.spectrum, self.Mc, 'g--', linewidth=2)
        ax.plot(self.spectrum, self.Snorm, 'b', linewidth=4)
        ax.plot(self.spectrum, self.Sc, 'b--', linewidth=2)

        ax.set_ylim([-0.01, 1.01])
        ax.set_xlim([380, 781])
        ax.set_xlabel('wavelength (nm)')
        ax.set_ylabel('sensitivity')
        plt.tight_layout()
        plt.show()

    def plotCMFs(self):
        '''
        '''
        try:
            plt.__version__
        except NameError:
            import PlottingFun as pf
            import matplotlib.pylab as plt
            
        fig = plt.figure()
        ax = fig.add_subplot(111)
        pf.AxisFormat()
        pf.TufteAxis(ax, ['left', 'bottom'], Nticks=[5, 5])
        ax.plot(self.spectrum, self.CMFs[0, :], 'r', linewidth=2)
        ax.plot(self.spectrum, self.CMFs[1, :], 'g', linewidth=2)
        ax.plot(self.spectrum, self.CMFs[2, :], 'b', linewidth=2)
        ax.set_xlabel('wavelength (nm)')
        ax.set_ylabel('sensitivity')
        ax.set_xlim([380, 781])
        ax.set_ylim([-0.25, 2])
        plt.tight_layout()
        plt.show()

    def plotcoeff(self):
        '''
        '''
        try:
            plt.__version__
        except NameError:
            import PlottingFun as pf
            import matplotlib.pylab as plt
            
        fig = plt.figure()
        ax = fig.add_subplot(111)
        pf.AxisFormat()
        pf.TufteAxis(ax, ['left', 'bottom'], Nticks=[5, 5])
        ax.plot(self.spectrum, self.rVal, 'r', linewidth=2)
        ax.plot(self.spectrum, self.gVal, 'g', linewidth=2)
        ax.plot(self.spectrum, self.bVal, 'b', linewidth=2)
        ax.set_xlim([self.spectrum[0], self.spectrum[-1]])
        ax.set_xlabel('wavelength (nm)')
        ax.set_ylabel('coefficients')
        ax.set_xlim([380, 781])
        plt.tight_layout()
        plt.show()

    def plotColorSpace(self):
        '''
        '''
        self._plotColorSpace()
        plt.show()

    def plotConfusionLines(self, deficit='deutan'):
        '''add confusion lines
        '''
        
        self._plotColorSpace()
        self.find_copunctuals()
        print deficit, ': ', self.copunctuals[deficit]
        
        if deficit.lower() == 'deutan' or deficit.lower() == 'protan':
            lambdas = [420, 460, 470, 480, 490, 500, 515,]
        elif deficit.lower() == 'tritan':
            lambdas = [420, 460, 480, 500, 520, 535, 545, 555,
                       570, 585, 600, 625, 700]

        self.cs_ax.plot(self.copunctuals[deficit][0], 
                        self.copunctuals[deficit][1], 'wo', markersize=10)
        for lam in lambdas:
            self.cs_ax.plot([self.find_testLightMatch(lam)[0],
                     self.copunctuals[deficit][0]],
                     [self.find_testLightMatch(lam)[1], 
                      self.copunctuals[deficit][1]],
                     'k-', linewidth=1)   
                     
        self.cs_ax.text(0.7, 1, deficit, fontsize=24)
        plt.show()                 

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

    def _plotColorSpace(self):
        '''
        '''
        
        try:
            plt.__version__
        except NameError:
            import matplotlib.pylab as plt
            
        fig = plt.figure()
        self.cs_ax = fig.add_subplot(111)
        pf.AxisFormat(FONTSIZE=10, TickSize=6)
        pf.centerAxes(self.cs_ax)

        self.cs_ax.plot(self.rVal, self.gVal, 'k', linewidth=3.5)

        # add equi-energy location to plot
        self.cs_ax.plot(1.0/3.0, 1.0/3.0, 'ko', markersize=5)
        self.cs_ax.annotate(s='{}'.format('E'), xy=(1./3.,1./3.), xytext=(2,8),
                    ha='right', textcoords='offset points', fontsize=16)

        # annotate plot
        dat = zip(self.spectrum[::10], self.rVal[::10], self.gVal[::10])
        for text, X, Y in dat:
            if text > 460 and text < 630:

                if text <= 500: 
                    self.cs_ax.scatter(X - 0.02, Y, marker='_', s=150, c='k')
                    self.cs_ax.annotate(s='{}'.format(int(text)),
                                xy=(X, Y), 
                                xytext=(-15, -5), 
                                ha='right', 
                                textcoords='offset points', fontsize=16)
                elif text > 500 and text <= 510:
                    self.cs_ax.scatter(X, Y + 0.02, marker='|', s=150, c='k')
                    self.cs_ax.annotate(s='{}'.format(int(text)),
                                xy=(X, Y), 
                                xytext=(5, 20), 
                                ha='right', 
                                textcoords='offset points', fontsize=16) 
                else:
                    self.cs_ax.scatter(X + 0.02, Y, marker='_', s=150, c='k')
                    self.cs_ax.annotate(s='{}'.format(int(text)),
                                xy=(X, Y), 
                                xytext=(45, -5), 
                                ha='right', 
                                textcoords='offset points', fontsize=16)
        
        self.cs_ax.set_xlim([-0.4, 1.2])
        self.cs_ax.set_ylim([-0.2, 1.2])
        
        plt.tight_layout()
        
if __name__ == '__main__':
    import PlottingFun as pf
    import matplotlib.pylab as plt
    color = colorSpace()
    
    #color.plotCompare()
    #color.plotFilters()
    #color.plotSpecSens()
    #color.plotCMFs()
    #color.plotcoeff()
    #color.plotColorSpace()
    color.plotConfusionLines()
    