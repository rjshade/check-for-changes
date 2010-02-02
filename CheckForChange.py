#!/usr/bin/python

import difflib
import smtplib
import time
import urllib2

################################################################################
# -- Get reference page
# -- Every 'secondsDelay' seconds download new page and compare with reference
# -- If different, send email message and update reference page with new page 
remoteURL = 'http://www.foo.com/bar.html'
localFile = 'ref.html'
localURL = 'file:./' + localFile

username = 'your_username@googlemail.com'
password = 'your_password'

sendTo = ['foo@bar.com','bar@foo.com']

secondsDelay = 30

################################################################################

def emailChanges(refHTML, newHTML, diffList):
    subject  = 'Change in site: %s' % remoteURL 
    
    msg = ('From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n'
           % (username, ', '.join(sendTo), subject) )
    msg += '-------------------------------------------------------\r\n'
    msg += '\r\n'
    msg += '\r\n'
    for line in diffList:
        msg += line
        msg += '\r\n'
    msg += '\r\n'
    msg += '\r\n'
    msg += '-------------------------------------------------------\r\n'
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, sendTo, msg)
    server.quit()

################################################################################
def getHTML( url ):
    req = urllib2.Request( url )

    try:
        response = urllib2.urlopen( req )
    except:
        print 'Uh-oh... urlopen raised an exception...'
        #if hasattr( e, 'reason' ):
        #    print 'Failed to reach server'
        #    print 'Reason: ', e.reason
        #elif hasattr( e, 'code' ):
        #    print 'Server failed to fulfil request'
        #    print 'Error code: ', e.code
        return False
    else:
        return response.read()
    

################################################################################
def writeHTML( fname, html ):
    f = open( fname, 'w' )
    f.write( html )
    f.close()

################################################################################

def main():
    print 'Getting initial reference file...'
    refHTML = getHTML( remoteURL )
    while( refHTML == False ):
        print '...retrying...'
        refHTML = getHTML( remoteURL )
    writeHTML( localFile, refHTML )
    
    while True:
            print 'Getting latest page...', time.strftime('%a, %d %b %Y %H:%M:%S',time.localtime())
            newHTML = getHTML( remoteURL )
            while( newHTML == False ):
                print '...retrying...'
                newHTML = getHTML( remoteURL )
    
            refHTML = getHTML( localURL )
        
            diffList = difflib.context_diff(
                            newHTML.splitlines(),
                            refHTML.splitlines() )
    
            listOfDiffs = list(diffList)
            numDiffs =  len( listOfDiffs )
    
            if numDiffs == 0:
                print "No change..."
                time.sleep(secondsDelay)
            else:
                print "Page changed: sending email"
                emailChanges(refHTML, newHTML, listOfDiffs)
    
                print "Updating reference page..."
                writeHTML( localFile, newHTML )

if __name__ == '__main__':
    main();

