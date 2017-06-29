import urllib.request
import os
import json
import sys
import requests
import base64

ACCESS_TOKEN = "access_token";
LIMIT = str(25)
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

def createTitle(title , count) :
    return str(10000 + count)[1:] + '. ' + str(title) + '.jpg'

def profile_pics(pageId, pageName) :
    print("Downloading " + pageName + "'s profile pics")
    os.mkdir(pageName + os.sep + 'Profile Pics')
    after = ''
    totalFilesDownloaded = 0
    api_request_url = "https://graph.facebook.com/v2.9/AnushkaShetty/photos?access_token="+ACCESS_TOKEN+"&debug=all&fields=created_time%2Csource&format=json&limit="+LIMIT+"&method=get&pretty=0&suppress_http_code=1"
    print("Files Downloaded : \n#0000")
    while True :
        with urllib.request.urlopen(api_request_url) as response :
            jsonObject = json.loads(response.read().decode('utf-8'))
            picsObjectArray = jsonObject['data']
            numberOfPics = len(picsObjectArray)
            for i in range(numberOfPics) :
                photo = picsObjectArray[i]
                downloadUrl = photo['source'];
                totalFilesDownloaded = totalFilesDownloaded + 1
                photoSaveTitle = createTitle(photo['created_time'], totalFilesDownloaded)
                urllib.request.urlretrieve(downloadUrl,os.getcwd()  + os.sep + pageName + os.sep + 'Profile Pics' + os.sep + photoSaveTitle)
                print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
                print("#" + str(10000 + totalFilesDownloaded)[1:])
        try :
            api_request_url = str(jsonObject['paging']['next'])
        except KeyError :
            print("All profile pics downloaded");
            break;

def uploaded_pics(pageId, pageName):
    url = "https://graph.facebook.com/v2.9/AnushkaShetty/photos?access_token="+ACCESS_TOKEN+"&debug=all&fields=created_time%2Csource&format=json&limit="+LIMIT+"&method=get&pretty=0&suppress_http_code=1&type=uploaded"
    print("Downloading " + pageName + "'s Uploaded pics")
    os.mkdir(pageName + os.sep + 'Uploaded Pics')
    after = ''
    totalFilesDownloaded = 0
    print("Files Downloaded : \n#0000")
    while True :
        with urllib.request.urlopen(url) as response :
            jsonObject = json.loads(response.read().decode('utf-8'))
            picsObjectArray = jsonObject['data']
            numberOfPics = len(picsObjectArray)
            for i in range(numberOfPics) :
                photo = picsObjectArray[i]
                downloadUrl = photo['source'];
                totalFilesDownloaded = totalFilesDownloaded + 1
                photoSaveTitle = createTitle(photo['created_time'], totalFilesDownloaded)
                urllib.request.urlretrieve(downloadUrl,os.getcwd()  + os.sep + pageName + os.sep + 'Uploaded Pics' + os.sep + photoSaveTitle)
                print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
                print("#" + str(10000 + totalFilesDownloaded)[1:])
        try :
            url = str(jsonObject['paging']['next'])
        except KeyError :
            print("All Uploaded pics downloaded");
            break;

def all_pics(pageId, pageName) :
    url = "https://graph.facebook.com/v2.9/"+ pageId + "/photos?access_token="+ACCESS_TOKEN+"&debug=all&fields=created_time%2Csource&format=json&limit=200&method=get&pretty=0&suppress_http_code=1&type=uploaded"
    print("Downloading " + pageName + "'s All pictures")
    os.mkdir(pageName + os.sep + 'Pictures')
    after = ''
    totalFilesDownloaded = 0
    print("Files Downloaded : \n#0000")
    while True :
        with urllib.request.urlopen(url) as response :
            jsonObject = json.loads(response.read().decode('utf-8'))
            picsObjectArray = jsonObject['data']
            numberOfPics = len(picsObjectArray)
            for i in range(numberOfPics) :
                photo = picsObjectArray[i]
                downloadUrl = photo['source'];
                totalFilesDownloaded = totalFilesDownloaded + 1
                photoSaveTitle = createTitle(photo['created_time'], totalFilesDownloaded)
                urllib.request.urlretrieve(downloadUrl,os.getcwd()  + os.sep + pageName + os.sep + 'Pictures' + os.sep + photoSaveTitle)
                print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
                print("#" + str(10000 + totalFilesDownloaded)[1:])
        try :
            url = str(jsonObject['paging']['next'])
        except KeyError :
            print("All pictures downloaded successfully");
            break;
        except :
            print("Some error occured");

def getTextFromImage():
	payload = {'isOverlayRequired':True,'apikey':'webocr3'}
	filename = "/home/makkar/Desktop/It's a Virgo Thing/Pictures/1000.jpg"
	with open(filename,'rb') as f:
		r = requests.post('https://api.ocr.space/parse/image',files={filename:f},data=payload)
	return r.content.decode()

def postStatusOnPage(status):
	PAGE_ACCESS_TOKEN = "page_access_token"
	post_url = "https://graph.facebook.com/v2.9/666999723509273/feed/?access_token=" + PAGE_ACCESS_TOKEN
	payload = {'message' : status}
	r = requests.post(post_url, data=payload)
	try :
		post_id = (json.loads(r.content.decode('utf-8')))['id']
		print("Posted successfully : " + post_id)
	except KeyError :
		print("Status not posted. Error ocurred.")

if __name__ == '__main__':
	content = getTextFromImage()
	jsonObject = json.loads(content)
	parsedText = jsonObject["ParsedResults"][0]["ParsedText"]
	postStatusOnPage(parsedText)

if __name__ == '__magn__':
    pageUrl = sys.argv[1]
    pageId = pageUrl.split('/')[3]
    pageName =''
    api_request_url = "https://graph.facebook.com/v2.9/"+ pageId +"/?access_token="+ ACCESS_TOKEN +"&fields=name&format=json&method=get&pretty=0&suppress_http_code=1"
    with urllib.request.urlopen(api_request_url) as response :
        jsonObject = json.loads(response.read().decode('utf-8'));
        pageName = jsonObject['name']
    print(pageName)
    os.mkdir(pageName)
    all_pics(pageId, pageName)
    #profile_pics(pageId,pageName)
    #uploaded_pics(pageId, pageName)
