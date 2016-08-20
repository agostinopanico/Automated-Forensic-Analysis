'''
1st and 2st Rule - Given a specific timeframe search every file in MFT to find information about what happend that exact timeframe
           Then look at the Registry information
           Finally, store all info to an Array in descending order based on timestamp.
'''
#!/usr/bin/env python
from datetime import datetime


def insideTimeframe(timestamp, mintime, maxtime):
    
    #It will hit the exception when it finds 1601-01-01 00:00:00
    try:
        time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    except:
        return False
    
    #Compare times with given timeframe
    if (time - mintime).total_seconds() > 0 and (maxtime - time).total_seconds() > 0 :
        return 1
    return 0
        

def registrySpots(array):
    ''' Parse all timestamps in the results array and store them in another array in a descending order
        array              - contains all the timestamps that has to do with the specific file we are searching
        @eventArray        - return array in descending order based on timestamps
    '''
    eventArray = []
    cnt = 0
    
    for i in xrange(len(array)):
        eventArray.append([])
        eventArray[cnt].append(array[i][4] + ' ' + array[i][1])
        eventArray[cnt].append(array[i][0])
        cnt += 1
        
    return eventArray 
    

def sortRecents(recents):
    ''' Parse all timestamps in the results array and store them in another array in a descending order
        results            - contains all the timestamps that has to do with the specific file we are searching
        @eventArray        - return array in descending order based on timestamps
    '''
    results = []
    
    for i in xrange(len(recents)):
        if recents[i][2] == 'RootMRU':
            results.append(recents[i])
    
    eventArray = []
    minV = [] 
    while(results):
        t1 = int(results[0][3])
        minV = [t1, 0]
        for i in xrange(len(results)):
            t2 = int(results[i][3])
            if t2 < t1:
                t1 = t2
                minV = [t2, i]
        eventArray.append(results[minV[1]])    
        results.pop(minV[1])
            
    return eventArray 

def event(results):
    ''' Parse all timestamps in the results array and store them in another array in a descending order
        results            - contains all the timestamps that has to do with the specific file we are searching
        @eventArray        - return array in descending order based on timestamps
    '''

    eventArray = []
    minV = [] 
    while(results):
        t1 = datetime.strptime(results[0][1], "%Y-%m-%d %H:%M:%S.%f")
        minV = [t1, 0]
        for i in xrange(len(results)):
            t2 = datetime.strptime(results[i][1], "%Y-%m-%d %H:%M:%S.%f")
            if t2 == min(t1,t2):
                t1 = t2
                minV = [t2, i]

        #A few of the entries (Registry) store a newline at the end so I remove it
        eventArray.append(results[minV[1]][0])
        eventArray.append(results[minV[1]][1])
    
        results.pop(minV[1])
            
    return eventArray


def searchTimeFrame(mintime, maxtime, mftArray, userAssist, recents, lastvisitedmru, runmru):
    ''' Find every timestamp and info that has to do with the name argument
        name            - The name of the file to search
        mftArray        - The mft array
        userAssist      - The user assist array
        recents         - The recents array
    '''    
    results = []
    checkresults = []
    cnt = 0
    
    print userAssist
    print
    print lastvisitedmru
    print
    print runmru
    
    
    if lastvisitedmru != []:
        checkresults = registrySpots(lastvisitedmru)
        for i in xrange(len(checkresults)):
            timestamp = checkresults[i][1]
            if insideTimeframe(timestamp, mintime, maxtime) == 1:
                results.append([]) 
                results[cnt].append(checkresults[i][0])
                results[cnt].append(checkresults[i][1])
                cnt += 1
                
    if runmru != []:
        checkresults = registrySpots(runmru)
        for i in xrange(len(checkresults)):
            timestamp = checkresults[i][1]
            if insideTimeframe(timestamp, mintime, maxtime) == 1:
                results.append([]) 
                results[cnt].append(checkresults[i][0])
                results[cnt].append(checkresults[i][1])
                cnt += 1 
    
    #Search for a specific file name in the MFT table
    for i in xrange(len(userAssist)):
        timestamp = userAssist[i][3]
        if insideTimeframe(timestamp, mintime, maxtime):
            results.append([]) 
            #format is [Name, timestamp] - [text.txt, 2015-01-02 22:49:35.829651]
            filenamePath = userAssist[i][4]
            #From {7C5A40EF-A0FB-4BFC-874A-C0F2E0B9FA8E}\\AccessData\\FTK Imager\\FTK Imager.exe store FTK Imager.exe
            filename = filenamePath[filenamePath.rfind('\\')+1:]
            #Store results to array
            results[cnt].append(filename)
            results[cnt].append(userAssist[i][3])
            cnt += 1
    
    print
    print results
    print
    
    results = event(results)
    
    print sortRecents(recents)
    print
    print results
    
    print len(results)
    '''
    results holds all info about userassist,runmru and lastvisitedmru
    recents holds info about recent
    '''
    
    print '[*] Finished Search Time Frame Rule'
    
    return results