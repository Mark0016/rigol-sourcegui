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

import re, os, shutil


class path():
    '''Path of certain files'''

    def gdefault():
        path = 'global_default.sourcecfg'
        return path

    def udefault():
        path = os.path.join(os.path.expanduser('~'),'.rigol-sourcegui','default.sourcecfg')
        if os.path.exists(path):
            return path
        else:
            try:
                os.mkdir(os.path.join(os.path.expanduser('~'),'.rigol-sourcegui'))
            except FileExistsError:
                pass
            shutil.copyfile('default.sourcecfg', path)
            return path


class Properties(object):
    '''Dictionary like database for properties of instrument and its objects'''

    def __init__(self,item = None):
        super(self.__class__,self).__init__()

        self.defaultValue = {}
        if item!=None:
            self.value = dict(item)
        else:
            self.value = {}

        self._loadDefault(path.gdefault())
        self.load(path.udefault())

    def __repr__(self):
        return str(self.value)
    
    def __getitem__(self,key):
        return self.value[key]

    def _defaults(self,numOfChannels = 2):

        self.value.setdefault('main',{})
        for i in range(numOfChannels):
            self.value.setdefault('source%d'%(i+1),{})

        self._mainDefaults()
        for i in range(numOfChannels):
            self._sourceDefaults(i+1)
        

    def _mainDefaults(self):

        self['main'].setdefault('ip',None)

    def _sourceDefaults(self,channel):

        d = self['source%d'%channel]

        d.setdefault('voltage',5)
        d.setdefault('shape','sin')
        d.setdefault('frequency',1000)
        d.setdefault('offset',0)
        d.setdefault('phase',0)
        d.setdefault('duty',50)
        d.setdefault('symmetry',10)

    def _toStr(self):
            
        retstr = ''

        for obj in self.value.items():

            if type(obj[1])!=dict:
                continue
            
            retstr+='[%s]\n\n'%obj[0]

            for stt in obj[1].items():
                retstr+= '%s = %s\n' % stt

            retstr+= '\n'

        return retstr

    def save(self,path = str):

        f = open(path,'w')
        f.write(self._toStr())
        f.close()



    def load(self,path = str):

        self.value = self._loadData(path)
        self._setDefault()

    def reset(self):

        self.value = self.defaultValue
        self._setDefault()

    def _loadDefault(self,path = str):

        self.defaultValue = self._loadData(path)

    def _loadData(self,path = str):

        
        f = open(path,'r')
        s = f.read()
        f.close()
        s = re.sub(r'#.*\n','\n',s)
        
        rv = {}
        objlist = s.split('[')[1:]

        for obj in objlist:

            obj = obj.split(']')
            objname = obj[0].strip()
            objstts = list(filter(''.__ne__,obj[1].split('\n')))

            rv[objname] = {}

            for stt in objstts:
                stt = stt.split('=')[:2]
                sttname = stt[0].strip()

                sttval = stt[1].strip()
                try:
                    sttval = int(sttval)
                except ValueError:
                    try:
                        sttval = float(sttval)
                    except ValueError:
                        if sttval.lower() in ('true','yes'):
                            sttval = True
                        elif sttval.lower() in ('false','no'):
                            sttval = False
                        elif sttval.lower() in ('none','n/a'):
                            sttval = None

                rv[objname][sttname] = sttval

        return rv


    def _setDefault(self):

        self.value.setdefault('main',{})
        self.value.setdefault('source1',{})
        self.value.setdefault('source2',{})
        

        for obj in self.defaultValue.items():

            objname = obj[0]
            objstts = obj[1]

            self.value.setdefault(objname,{})

            for stt in objstts.items():
                
                sttname = stt[0]
                sttval = stt[1]

                self.value[objname].setdefault(sttname,sttval)


