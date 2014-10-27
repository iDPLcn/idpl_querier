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
        
        if '.' in hostname:
            self.hostname = hostname
        else:
            self.hostname = '[%s]' % hostname
        self.metaUrl = 'http://%s/esmond/perfsonar/archive/' % self.hostname
        
    def getThroughputData(self, dst, timeStart, timeEnd):
        eventType = 'throughput'
        uri = ''
        metadataList = self.__getMetadata(self.metaUrl, dst, eventType)
        try:
            eventTypeDict = self.__getEventTypeDict(metadataList[0], eventType)
            uri = eventTypeDict['base-uri']
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
    
    def getOwdelayData(self, dst, timeStart, timeEnd):
        eventType = 'histogram-owdelay'
        uri = ''
        metadataList = self.__getMetadata(self.metaUrl, dst, eventType)
        try:
            eventTypeDict = self.__getEventTypeDict(metadataList[0], eventType)
            summaryDict = self.__getSummaryDict(eventTypeDict['summaries'],
                                                'statistics', '0')
            uri = summaryDict['uri']
        except Exception:
            # TO DO
            return []
        
        dataUrl = 'http://%s%s' % (self.hostname, uri)
        data = self.__getData(dataUrl, timeStart, timeEnd)
        owdelayData = []
        try:
            owdelayData = [
                IntFloatPoint(point['ts'], point['val']['minimum']) 
                    for point in data
            ]
        except Exception:
            # TO DO
            pass
        finally:
            return owdelayData
        
    def getPingData(self, dst, timeStart, timeEnd):
        eventType = 'histogram-rtt'
        uri = ''
        metadataList = self.__getMetadata(self.metaUrl, dst, eventType)
        try:
            eventTypeDict = self.__getEventTypeDict(metadataList[0], eventType)
            summaryDict = self.__getSummaryDict(eventTypeDict['summaries'],
                                                'statistics', '0')
            uri = summaryDict['uri']
        except Exception:
            # TO DO
            return []
        dataUrl = 'http://%s%s' % (self.hostname, uri)
        data = self.__getData(dataUrl, timeStart, timeEnd)
        pingData = []
        try:
            pingData = [
                IntFloatPoint(point['ts'], point['val']['minimum'])
                    for point in data
            ]
        except Exception:
            # TO DO
            pass
        finally:
            return pingData
    
    def getLossData(self, dst, timeStart, timeEnd):
        eventType = 'packet-loss-rate'
        uri = ''
        metadataList = self.__getMetadata(self.metaUrl, dst, eventType)
        try:
            eventTypeDict = self.__getEventTypeDict(metadataList[0], eventType)
            uri = eventTypeDict['base-uri']
        except Exception:
            # TO DO
            return []
        dataUrl = 'http://%s%s' % (self.hostname, uri)
        data = self.__getData(dataUrl, timeStart, timeEnd)
        lossData = []
        try:
            lossData = [
                IntFloatPoint(point['ts'], point['val'])
                    for point in data
            ]
        except Exception:
            # TO DO
            pass
        finally:
            return lossData

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
        
    def __getEventTypeDict(self, metadata, eventType):
        for eventTypeDict in metadata['event-types']:
            if self.__dictCheck(eventTypeDict, {'event-type': eventType}):
                return eventTypeDict
        return {}
    
    def __getSummaryDict(self, summaryList, summaryType, summaryWindow):
        for summaryDict in summaryList:
            if self.__dictCheck(summaryDict, {
                'summary-type': summaryType,
                'summary-window': summaryWindow,                              
            }):
                return summaryDict
        return {}
    
    def __dictCheck(self, rawDict, conditionDict):
        for condition in conditionDict:
            if rawDict[condition] != conditionDict[condition]:
                return False
        return True
        
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