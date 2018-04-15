'''This file is part of rigol-sourcegui.
   
   Copyright (c) 2017 Márk Vasi

   rigol-sourcegui is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   rigol-sourcegui is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with rigol-sourcegui.  If not, see <http://www.gnu.org/licenses/>.'''

from PyQt4 import QtCore
import vxi11



class CommunicationThread(QtCore.QThread):
    '''Thread for updating memory of instrument'''

    def __init__(self,ip,channel,props,data = None):
        super(self.__class__,self).__init__()

        self.ip = ip
        self.channel = channel
        self.props = props
        self.data = data
        
    def run(self):

        self.scope = vxi11.Instrument(self.ip)

        if self.props['shape'] == 'sin':
            self.sin()
        elif self.props['shape'] == 'square':
            self.sqr()
        elif self.props['shape'] == 'pulse':
            self.pulse()
        elif self.props['shape'] == 'noise':
            self.noise()
        elif self.props['shape'] == 'ramp':
            self.ramp()
        elif self.props['shape'] == 'custom':
            self.custom()
        else:
            self.mem()

    def sin(self):

        amp = self.props['voltage']
        frq = self.props['frequency']
        offset = self.props['offset']
        phase = self.props['phase']

        self.scope.write(':SOUR%d:APPL:SIN %f,%f,%f,%f'%(self.channel,frq,amp,offset,phase))
        self.scope.write(':SOUR%d:PHAS:INIT'%self.channel)

    def sqr(self):

        amp = self.props['voltage']
        frq = self.props['frequency']
        offset = self.props['offset']
        phase = self.props['phase']

        self.scope.write(':SOUR%d:APPL:SQU %f,%f,%f,%f'%(self.channel,frq,amp,offset,phase))
        self.scope.write(':SOUR%d:PHAS:INIT'%self.channel)

    def pulse(self):

        amp = self.props['voltage']
        frq = self.props['frequency']
        offset = self.props['offset']
        phase = self.props['phase']
        duty = self.props['duty']

        self.scope.write(':SOUR{}:FUNC PULS'.format(self.channel))
        self.scope.write(':SOUR{}:VOLT {}'.format(self.channel,amp))
        self.scope.write(':SOUR{}:FREQ {}'.format(self.channel,frq))
        self.scope.write(':SOUR{}:PHAS {}'.format(self.channel,phase))
        self.scope.write(':SOUR{}:VOLT:OFFS {}'.format(self.channel,offset))
        self.scope.write(':SOUR%d:PULS:DCYC %f'%(self.channel,duty))
        self.scope.write(':SOUR%d:PHAS:INIT'%self.channel)

    def noise(self):

        amp = self.props['voltage']
        offset = self.props['offset']

        self.scope.write(':SOUR%d:APPL:NOIS %f,%f'%(self.channel,amp,offset))

    def ramp(self):
        
        amp = self.props['voltage']
        frq = self.props['frequency']
        offset = self.props['offset']
        phase = self.props['phase']
        symmetry = self.props['symmetry']

        self.scope.write(':SOUR%d:APPL:RAMP %f,%f,%f,%f'%(self.channel,frq,amp,offset,phase))
        self.scope.write(':SOUR%d:FUNC:RAMP:SYMM %f'%(self.channel,symmetry))
        self.scope.write(':SOUR%d:PHAS:INIT'%self.channel)

    def mem(self):

        amp = self.props['voltage']
        frq = self.props['frequency']
        offset = self.props['offset']
        phase = self.props['phase']

        self.scope.write(':SOUR%d:APPL:USER %f,%f,%f,%f'%(self.channel,frq,amp,offset,phase))
        self.scope.write(':SOUR%d:FUNC:SHAPE %s'%(self.channel,self.props['shape']))
        self.scope.write(':SOUR%d:PHAS:INIT'%self.channel)

    def custom(self):
        #not implemented
        pass




class InfoThread(QtCore.QThread):
    '''Thread for reading memory of instrument'''

    updateInfo = QtCore.pyqtSignal(dict)


    def __init__(self,ip,channel):
        super(self.__class__,self).__init__()

        self.ip = ip
        self.channel = channel

    def run(self):

        retdict = {}
        self.scope = vxi11.Instrument(self.ip)

        general = self.scope.ask(':SOUR%d:APPL?'%self.channel)

        general = general.split(',')
        retdict['shape'] = general[0].lower()
        retdict['frequency'] = float(general[1])
        retdict['voltage'] = float(general[2])
        retdict['offset'] = float(general[3])
        retdict['phase'] = float(general[4])

        retdict['duty'] = float(self.scope.ask(':SOUR%d:PULS:DCYC?'%self.channel))
        retdict['symmetry'] = float(self.scope.ask(':SOUR%d:FUNC:RAMP:SYMM?'%self.channel))

        if retdict['shape'] == 'squ':
            retdict['shape'] = 'square'
        elif retdict['shape'] in ('puls','nois'):
            retdict['shape']+='e'
        elif retdict['shape'] == 'user':
            retdict['shape'] = self.scope.ask(':SOUR%d:FUNC:SHAP?'%self.channel)
            if retdict['shape'] == 'EXT':
                retdict['shape'] = 'custom'

        self.updateInfo.emit(retdict)
        
        
        
