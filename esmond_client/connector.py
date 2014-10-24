'''
Created on 2014.10.23

@author: Jarvis Zhang
'''
import requests
from querier_server.models import IntFloatPoint

class EsmondConn(object):
    '''
    classdocs
    '''


    def __init__(self, hostname):
        '''
        Constructor
        '''
        
        self.hostname = hostname
        
    def getThroughputData(self, dst, timeStart, timeEnd):
        eventType = 'throughput'
        metaUrl = 'http://%s/esmond/perfsonar/archive/' % self.hostname
        uri = ''
        metadata = self.__getMetadata(metaUrl, dst, eventType)
        try:
            for eventTypeDict in metadata[0]['event-types']:
                if eventTypeDict['event-type'] == 'throughput':
                    uri = eventTypeDict['base-uri']
                    break
        except Exception:
            # TO DO
            return []
        dataUrl = 'http://%s%s' % (self.hostname, uri)
        data = self.__getData(dataUrl, timeStart, timeEnd)
        throughputData = []
        try:
            throughputData = [
                IntFloatPoint(point['ts'], point['val']) for point in data
            ]
        except Exception:
            # TO DO
            pass
        finally:
            return throughputData
        return throughputData
    
    def __getMetadata(self, url, dst, eventType):
        parameters = {
            'event-type': eventType,
            'destination': dst,
            'format': 'json',
        }
        metadata = []
        try:
            metadata = requests.get(url, params=parameters).json()     
        except Exception:
            # TO DO
            pass
        finally:
            return metadata
        
    def __getData(self, url, timeStart, timeEnd):
        parameters = {
            'time-start': timeStart,
            'time-end': timeEnd,
            'format': 'json',
        }
        data = []
        try:
            data = requests.get(url, params=parameters).json()
        except Exception:
            # TO DO
            pass
        finally:
            return data