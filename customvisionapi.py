########### Python 2.7 #############
''' This example shows how to use the custom api programatically
    No sdk library is needed.
'''
import sys
import httplib
import urllib
import json


params = urllib.urlencode({
})


def check_tag(tagname):
    '''This function check if the tagname parameter exist otherwise
    create one a return the id
    '''
    value = ""
    try:
        conn = httplib.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
        conn.request("GET", "/customvision/v1.2/Training/projects/" + projectid + "/tags?%s" % params, "{}", headers)
        response = conn.getresponse()
        data = response.read()
        print data
        dataformat = json.loads(data)
        for keys in dataformat['Tags']:
            if tagname == keys['Name']:
                value = keys['Id']
        conn.close()
        return value
    except Exception as exceptioncatch:
        print exceptioncatch


def upload_imgurl(url):
    '''This function upload the image and retunr
    the image id
    '''
    try:
        conn = httplib.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
        bodyurl = "{ \"Images\": [ { \"Url\": \"%s\", \"TagIDs\": \"pug\"}],\"TagIds\": [\"pug\"]}"
        #bodyurl = "{ \"Images\": [ { \"Url\": \"%s\", \"TagIDs\": \"None\"}]}"
        bodyurlformat = bodyurl % url
        print bodyurlformat
        conn.request("POST", "/customvision/v1.2/Training/projects/" + projectid +"/images/urls?%s" % params, bodyurlformat, headers)
        response = conn.getresponse()
        data = response.read()
        dataformat = json.loads(data)
        print dataformat
        imageid = dataformat['Images'][0]['Image']['Id']
        conn.close()
        return imageid
    except Exception as exceptioncatch:
        print exceptioncatch

def assign_tag(imageid, tagid):
    '''This function assign the tagid to the imageid
    '''
    bodytag = "{\"Tags\": [{\"ImageId\": \"%s\",\"TagId\": \"%s\"}]}"
    bodytagformat = bodytag %(imageid, tagid)
    print bodytagformat
    try:
        conn = httplib.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/customvision/v1.2/Training/projects/" + projectid +"/images/tags?%s" % params, bodytagformat, headers)
        response = conn.getresponse()
        data = response.read()
        dataformat = json.loads(data)
        print dataformat
        conn.close()
    except Exception as exceptioncatch:
        print exceptioncatch



def create_tag(tagname):
    '''This function create the tagname and retunr the tagid created
    '''
    try:
        conn = httplib.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/customvision/v1.2/Training/projects/" + projectid +"/tags?name=" + tagname + "&%s" % params, "{}", headers)
        response = conn.getresponse()
        data = response.read()
        dataformat = json.loads(data)
        print dataformat
        conn.close()
        return dataformat['Id']
    except Exception as exceptioncatch:
        print exceptioncatch


def readfile(file_name):
    '''This function reads the file and call rest of functions
    '''
    with open(file_name, 'r') as data:
        for line in data:
            pvalues = line.split(',')
            url = pvalues[0]
            tag = pvalues[1]
            tagid = check_tag(tag.rstrip())
            print tagid
            if tagid == '':
                tagid = create_tag(tag)
            imageid = upload_imgurl(url)
            print tagid
            print imageid
            assign_tag(imageid, tagid)



print "Training key: ", sys.argv[1]
print "ProjectID", sys.argv[2]
print "File Name: ", sys.argv[3]
trainingkey = sys.argv[1]
projectid = sys.argv[2]
filename = sys.argv[3]


headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Training-key': trainingkey,
}
readfile(filename)

