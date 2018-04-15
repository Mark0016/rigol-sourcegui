#!/usr/bin/env python3

##'''This file is part of rigol-sourcegui.
##
##   Copyright (c) 2017 Márk Vasi 
##
##   rigol-sourcegui is free software: you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation, either version 3 of the License, or
##   (at your option) any later version.
##
##   rigol-sourcegui is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.
##
##   You should have received a copy of the GNU General Public License
##   along with rigol-sourcegui.  If not, see <http://www.gnu.org/licenses/>.'''



import sys
from PyQt4 import QtGui,QtCore
from design import source_design, mwf_popup_design, custom_popup_design, ip_popup_design

import vxi11
from ipaddress import IPv4Address
from core import path
from core import Properties
from network import CommunicationThread


INPUT_VALIDATOR = QtGui.QRegExpValidator(QtCore.QRegExp('[-]?[0-9]*\.?[0-9]+[TGMkmunp]?'))



class DutyValidator(QtGui.QIntValidator):
    def __init__(self,*arg,**kwa):
        super(self.__class__,self).__init__(*arg,**kwa)

        self.setRange(10,90)

    def fixup(self,inpt):
        if int(inpt) < 10:
            inpt = '10'

        elif int(inpt) > 90:
            inpt = '90'

        return inpt
    
        

def toFloat(string):

    prefixes = { 'T':10**12,
                 'G':10**9,
                 'M':10**6,
                 'k':10**3,
                 'm':10**-3,
                 'u':10**-6,
                 'n':10**-9,
                 'p':10**-12 }

    for prefix in prefixes.keys():
        if prefix in string:
            return float(string.replace(prefix,''))*prefixes[prefix]

    return float(string)


def wfFromFile(path):
    f = open(path,'rb')
    rd = f.read()
    hs = '#'
    dl = str(len(rd))
    hs += str(len(dl)) + dl
    hs = bytes(hs,'utf-8')
    f.close()
    return hs + rd


class IpWindow(QtGui.QMainWindow,ip_popup_design.Ui_MainWindow):

    addressChanged = QtCore.pyqtSignal(str)
    
    
    def __init__(self,currentAddress = None):
        super(self.__class__,self).__init__()

        self.setupUi(self)
        if currentAddress != None:
            self.lineEdit.setText(str(currentAddress))

        self._connections()

    def changeAddress(self):

        try:
            IPv4Address(self.lineEdit.text())
        except ValueError:
            return
        
        ip = self.lineEdit.text()
        self.addressChanged.emit(ip)
        self.close()

    def _connections(self):

        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.changeAddress)
        self.lineEdit.returnPressed.connect(self.changeAddress)


class MoreWaveforms(QtGui.QMainWindow,mwf_popup_design.Ui_MainWindow):

    itemChanged = QtCore.pyqtSignal(int,str)
    customSelected = QtCore.pyqtSignal(int)

    def __init__(self,channel):
        super(self.__class__,self).__init__()

        self.setupUi(self)
        self.channel = channel
        self._connections()

    def retShape(self):
        try:
            t = self.listWidget.selectedItems()[0].text()
        except IndexError:
            return
        if t == 'Custom...':
            self.customSelected.emit(self.channel)
        elif t == 'Sinusoid':
            t = 'sin'
        elif t == 'Exp. Rise':
            t = 'exprise'
        elif t == 'Exp. Fall':
            t = 'expfall'
        else:
            t = t.lower()
        self.itemChanged.emit(self.channel,t)
        self.close()

    def _connections(self):

        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.retShape)

    

class CustomWaveform(QtGui.QMainWindow,custom_popup_design.Ui_MainWindow):

    fromFile = QtCore.pyqtSignal(str)

    def __init__(self,channel):
        super(self.__class__,self).__init__()

        self.channel = channel
        
        self.setupUi(self)

        self._connections()
        

    def openFile(self):
        self.fd = QtGui.QFileDialog()
        self.fd.setFilter('Waveforms (*.arb);;Any File (*)')
        self.fd.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        if self.fd.exec_():
            self.wfLoad.emit(self.fd.selectedFiles()[0])

    def _connections(self):

        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.openFile)
    


class MainWindow(QtGui.QMainWindow,source_design.Ui_MainWindow):

    properties = Properties()

    def __init__(self,app=QtGui.QApplication):
        super(self.__class__,self).__init__()

        self.app = app

        self.setupUi(self)

        self._setLeText()

        for channel in (1,2):
            self.setEnabledObjects(channel,self.properties['source%d'%channel]['shape'])

        self._connections()

        self._setLeValidator()
        
        if self.properties['main']['ip']==None:
            self.ipPopup()

        

    def sourceEnable(self,channel,enable = True):

        scope = vxi11.Instrument(self.properties['main']['ip'])
        scope.write('SOUR%d:OUTP:STAT %d'%(channel,enable))
        if enable:
            th = CommunicationThread(self.properties['main']['ip'],channel,self.properties['source%d'%channel])
            th.run()

        
    def updateProps1(self):
        
        d = self.properties['source1']
        d['voltage'] = toFloat(self.s1_v.text()) 
        d['frequency'] = toFloat(self.s1_frq.text())
        d['offset'] = toFloat(self.s1_offset.text())
        d['phase'] = int(self.s1_phase.text())
        d['duty'] = int(self.s1_duty.text())
        d['symmetry'] = int(self.s1_simm.text())

        if self.s1_enable.checkState() == 2:
            th = CommunicationThread(self.properties['main']['ip'],1,self.properties['source1'])
            th.run()

    def updateProps2(self):
        
        d = self.properties['source2']
        d['voltage'] = toFloat(self.s2_v.text() )
        d['frequency'] = toFloat(self.s2_frq.text())
        d['offset'] = toFloat(self.s2_offset.text())
        d['phase'] = int(self.s2_phase.text())
        d['duty'] = int(self.s2_duty.text())
        d['symmetry'] = int(self.s2_simm.text())

        if self.s2_enable.checkState() == 2:
            th = CommunicationThread(self.properties['main']['ip'],2,self.properties['source2'])
            th.run()

    def updateShape(self, channel, shape=None):
        if channel == 1:
            cb = self.s1_shape
            e = self.s1_enable
        elif channel == 2:
            cb = self.s2_shape
            e = self.s2_enable
        if shape == None:
            i = cb.currentIndex()
            shapes = ('sin','square','ramp','pulse','noise')
            if i == 5:
                self.moreShapes(channel)
            else:
                self.properties['source%d'%channel]['shape'] = shapes[i]
        else:
            self.properties['source%d'%channel]['shape'] = shape

        self.setEnabledObjects(channel,self.properties['source%d'%channel]['shape'])

        if e.checkState() == 2:
            th = CommunicationThread(self.properties['main']['ip'],channel,self.properties['source%d'%channel])
            th.run()



    def moreShapes(self, channel):

        self.mwfw = MoreWaveforms(channel)
        self.mwfw.itemChanged.connect(self.updateShape)
        self.mwfw.show()


    def customWF(self, channel):
        self.cwfw = CustomWaveform(channel)
        self.cwfw.fromFile.connect()
        
    def cwfFromFile(self,channel,path):
        pass


    def changeIpAddress(self,address):
        self.properties['main']['ip'] = address

    def ipPopup(self):
        self.ipw = IpWindow(self.properties['main']['ip'])
        self.ipw.addressChanged.connect(self.changeIpAddress)
        self.ipw.show()

    def openConfig(self):
        self.fdlcfg = QtGui.QFileDialog()
        self.fdlcfg.setFilter('Source configuration file (*.sourcecfg);;All files (*) ')
        self.fdlcfg.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        if self.fdlcfg.exec_():
            self.properties.load(self.fdlcfg.selectedFiles()[0])
            self._setLeText()

    def saveConfig(self):
        self.fdscfg = QtGui.QFileDialog()
        self.fdscfg.setFilter('Source configuration file (*.sourcecfg);;All files (*)')
        self.fdscfg.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        if self.fdscfg.exec_():
            self.properties.save(self.fdscfg.selectedFiles()[0])

    def loadDefaults(self):
        self.properties.value = self.properties.defaultValue
        self._setLeText()

    def setEnabledObjects(self,channel,waveform):

        obj={1:{'amp':self.s1_v,
                  'frq':self.s1_frq,
                  'phase':self.s1_phase,
                  'offset':self.s1_offset,
                  'duty':self.s1_duty,
                  'symmetry':self.s1_simm},
             2:{'amp':self.s2_v,
                  'frq':self.s2_frq,
                  'phase':self.s2_phase,
                  'offset':self.s2_offset,
                  'duty':self.s2_duty,
                  'symmetry':self.s2_simm}}


        if waveform == 'noise':
            for o in ('amp','offset'):
                obj[channel][o].setEnabled(True)
            for o in ('frq','phase','duty','symmetry'):
                obj[channel][o].setEnabled(False)
        elif waveform == 'pulse':
            for o in ('amp','offset','frq','phase','duty'):
                obj[channel][o].setEnabled(True)
            obj[channel]['symmetry'].setEnabled(False)
        elif waveform == 'ramp':
            for o in ('amp','offset','frq','phase','symmetry'):
                obj[channel][o].setEnabled(True)            
            obj[channel]['duty'].setEnabled(False)
        else:
            for o in ('amp','offset','frq','phase'):
                obj[channel][o].setEnabled(True)
            for o in ('duty','symmetry'):
                obj[channel][o].setEnabled(False)
        
        

    def _setLeText(self):

        self.s1_v.setText(str(self.properties['source1']['voltage']))
        self.s1_frq.setText(str(self.properties['source1']['frequency']))
        self.s1_phase.setText(str(self.properties['source1']['phase']))
        self.s1_offset.setText(str(self.properties['source1']['offset']))
        self.s1_duty.setText(str(self.properties['source1']['duty']))
        self.s1_simm.setText(str(self.properties['source1']['symmetry']))

        self.s2_v.setText(str(self.properties['source2']['voltage']))
        self.s2_frq.setText(str(self.properties['source2']['frequency']))
        self.s2_phase.setText(str(self.properties['source2']['phase']))
        self.s2_offset.setText(str(self.properties['source2']['offset']))
        self.s2_duty.setText(str(self.properties['source2']['duty']))
        self.s2_simm.setText(str(self.properties['source2']['symmetry']))

    def _setLeValidator(self):

        PHASE_VALIDATOR = QtGui.QIntValidator()
        PHASE_VALIDATOR.setRange(0,359)

        DUTY_VALIDATOR = DutyValidator()

        SYMM_VALIDATOR = QtGui.QIntValidator()
        SYMM_VALIDATOR.setRange(0,100)

        self.s1_v.setValidator(INPUT_VALIDATOR)
        self.s1_frq.setValidator(INPUT_VALIDATOR)
        self.s1_phase.setValidator(PHASE_VALIDATOR)
        self.s1_offset.setValidator(INPUT_VALIDATOR)
        self.s1_duty.setValidator(DUTY_VALIDATOR)
        self.s1_simm.setValidator(SYMM_VALIDATOR)

        self.s2_v.setValidator(INPUT_VALIDATOR)
        self.s2_frq.setValidator(INPUT_VALIDATOR)
        self.s2_phase.setValidator(PHASE_VALIDATOR)
        self.s2_offset.setValidator(INPUT_VALIDATOR)
        self.s2_duty.setValidator(DUTY_VALIDATOR)
        self.s2_simm.setValidator(SYMM_VALIDATOR)

    def closeEvent(self, event):
        self.app.closeAllWindows()
        event.accept()


    def _connections(self):
        
        self.s1_moreShapes.clicked.connect(lambda: self.moreShapes(1))
        self.s2_moreShapes.clicked.connect(lambda: self.moreShapes(2))
        self.s1_shape.currentIndexChanged.connect(lambda: self.updateShape(1))
        self.s2_shape.currentIndexChanged.connect(lambda: self.updateShape(2))

        self.s1_enable.clicked.connect(lambda: self.sourceEnable(1,True if self.s1_enable.checkState() == 2 else False))
        self.s2_enable.clicked.connect(lambda: self.sourceEnable(2,True if self.s2_enable.checkState() == 2 else False))


        
        for le in (self.s1_v,self.s1_simm,self.s1_frq,self.s1_offset,self.s1_duty,self.s1_phase):
            le.returnPressed.connect(self.updateProps1)
        for le in (self.s2_v,self.s2_simm,self.s2_frq,self.s2_offset,self.s2_duty,self.s2_phase):
            le.returnPressed.connect(self.updateProps2)

        self._menuConnections()

    def _menuConnections(self):

        self.actionIP_Address.triggered.connect(self.ipPopup)
        self.action_Open_config.triggered.connect(self.openConfig)
        self.action_Save_config.triggered.connect(self.saveConfig)
        self.actionFrom_File.triggered.connect(self.openConfig)
        self.action_Defaults.triggered.connect(self.loadDefaults)
        self.action_Quit.triggered.connect(self.app.closeAllWindows)
        


def main():

    app = QtGui.QApplication(sys.argv)
    GUI = MainWindow()
    GUI.show()
    app.exec_()



if '__main__' == __name__:
    main()
