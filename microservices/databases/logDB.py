
import pickle


class logDB:

    def __init__(self, name):
        self.name = name
        try:
                f = open('bd_dump'+name, 'rb')
                self.logs = pickle.load(f)
                f.close()
        except IOError:
                self.logs = []

    def addLog(self, log):               
        self.logs.append(log)
        f = open('bd_dump'+self.name, 'wb')
        pickle.dump(self.logs, f)
        f.close()
        data={'msg': '200 - OK'}
        return data

    def showLogs(self):
        return self.logs 
     
