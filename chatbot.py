


import string
import pylast

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account for Last.fm
API_KEY = "3d7f0e1033546757976a8b2cc8c19c75"
API_SECRET = "76442e531a8653998d9202e4d1982ba0"

# In order to perform a write operation you need to authenticate yourself
username = "cs140winter"
password_hash = pylast.md5("lastfmchatbot")

network = pylast.get_lastfm_network(api_key = API_KEY, api_secret = API_SECRET, username = username, password_hash = password_hash)

import re
# textchange.py

# list names
# order in topic = [band, album]
#order in subTopic = [song, info, popularity, concert, similar, album]
# contains common synoymns of keyword. Feel free to add more. Lower case 

band =  ["who","band","artist","group","singer", "ensemble", "team", "orchestra", "troupe", "musician", "composer", "performer", "creator", "virtuoso",  "vocalist"]

song = ["song", "songs","track", "melody", "anthem", "ballad", "chant", "lullaby", "piece","poem", "psalm", "round", "tune", "verse", "title", "air", "aria", "chorus", "hymn", "arrangement", "score", "soundtrack", "theme"]

album = ["album","albums","cds","cd","record","compact disk", "demo","recording","disk","release", "edition", "lp", "cassette", "tape", "ep", "anthology", "vinyl"]

similar = ["alike","similar","close","same","corresponding","akin"]

concert =  ["when","events","where","concert", "concerts","event", "gig","jam", "session", "musical", "recital", "show", "performance","gigs","jams", "sessions", "musicals", "recitals", "shows", "performances"]

similiar = ["similar", "close", "sound", "like", "love", "enjoy", "match", "matching", "akin", "alike" ,"close", "same"]

popularity = ["top", "popular", "well known", "best" , "popularity", "chart", "billboard", "hot"]

info = ["info","tell", "biography", "about","history", "account", "life", "profile" ]

makeList = ["write", "release", "distridute","distributed", "create", "created", "arrange", "arranged","created", "put together", "compose", "made","by","released"]


topic = [False, False]
subTopic = [False, False,False,False,False,False,False,False]
make = False

SONG = 0
INFO = 1
POPULARITY = 2
CONCERT = 3
SIMILAR = 4
ALBUM  = 5

#Main functions
# call this with each string in user prompt to see if any are keywords
# will have to loop each string in user prompt, can change so that 
# the function will take the line and the function will loop each string
# Sets corresponding list element to True if contains a key word
# Means this is the subject of the item in quotes

def whatTopic(word):
    word = word.lower()
    if isBand(word):
        topic[0] = True
    if isAlbum(word):
        topic[1] = True

def whatSubTopic(word):
    word = word.lower()
    if isSong(word):
       subTopic[SONG] = True
    if isInfo(word):
       subTopic[INFO] = True
    if isPopularity(word):
       subTopic[POPULARITY] = True
    if isConcert(word):
       subTopic[CONCERT] = True
    if isSimilar(word):
       subTopic[SIMILAR] = True
    if isAlbum(word):
      subTopic[ALBUM] = True   
    if isMake(word):
        make = True

#helper 
def isBand(word):
    i = 0
    for i in range(len(band)):
        if word == band[i]:
            return True
    return False

def isAlbum(word):
    for i in range(len(album)):
        if word == album[i]:
            return True
    return False

def isSong(word):
    for i in range(len(song)):
        if word == song[i]:
            return True
    return False

def isInfo(word):
    for i in range(len(info)):
        if word == info[i]:
            return True
    return False

def isPopularity(word):
    for i in range(len(popularity)):
        if word == popularity[i]:
            return True
    return False

def isConcert(word):
    for i in range(len(concert)):
        if word == concert[i]:
            return True
    return False

def isSimilar(word):
    for i in range(len(similar)):
        if word == similar[i]:
            return True
    return False

def isMake(word):
    for i in range(len(makeList)):
        if word == makeList[i]:
            make = True

def reset():
    for i in range(len(topic)):
        topic[i]=False
    for i in range(len(subTopic)):
        subTopic[i]= False
    make = False


def translateToLastFm (Name,Class,Subclass,By):
    try :
        
        if(By and Class[0] and Class[1]):
            myArtist=network.search_for_artist(Name).get_next_page()
            if(len(myArtist)>0):
                top=myArtist[0].get_top_albums()
                if(len(top)>0):
                    return str(top[0][0])
        elif((not By) and Class[0] and Class[1]):
            myAlbum=network.search_for_album(Name).get_next_page()
            if(len(myAlbum)>0):
                return myAlbum[0]
        
        if Class[0] :
            myArtist=network.search_for_artist(Name).get_next_page()[0]
            #myArtist=network.get_artist(Name)
            
            if  Subclass[CONCERT]:
                allmye=myArtist.get_upcoming_events()
                if(len(allmye)==0):
                    return("No Upcoming Events")
                mye=allmye[0]
                return str(str(myArtist)+" will play at venue#"+str(mye.get_venue().get_id())+" on "+mye.get_start_date()+" for " +str(mye))
            elif Subclass[SIMILAR]:
                return myArtist.get_similar()
            elif Subclass[SONG]:
                mysongs=myArtist.get_top_albums()
                if(len(mysongs)!=0):
                    return mysongs[0]
            elif Subclass[ALBUM]:
                myalbums=myArtist.get_top_albums()
                if(len(myalbums)!=0):
                    return myalbums[0]
            elif Subclass[POPULARITY]:
                return myArtist.get_playcount()
            elif Subclass[INFO]:
                return myArtist.get_bio_summary()
            else :
                return myArtist.get_bio_summary() 
            
        elif  Class[1] :
            #network.get_album(self, artist, title)
            myAlbum=network.search_for_album(Name).get_next_page()[0]
            if Subclass[SONG]:
               return myAlbum.get_tracks()[0]
            elif Subclass[INFO]:
                return myAlbum.get_wiki_summary()
                #get_wiki_content()
            elif Subclass[POPULARITY]:
                return myAlbum.get_playcount()
                #get_listener_count()
            else :
                return myAlbum.get_wiki_summary()
        return "fail"
    except ArithmeticError:
        print "didn't connect"
        return "fail"
#except BaseException :
#    return "Fail"ArithmeticError
# case "Venue" :
#                search_for_venue(Name, "United States"):
#case "Song" :
#    mySong=network.get_track(self, artist, title)
#    search_for_track(self, artist_name, track_name)
#def get_tag(self, name):
#def 
#def search_for_tag(self, tag_name):





def clean(mylist):
    newlist=[]
    for item in mylist:
        if(len(item)<3):
            if(newlist.count(mylist.index(item))==0):
                newlist.append(mylist.index(item))
                continue
        for comp in mylist:
            if(len(re.findall(comp, item))>0):
                if(newlist.count(mylist.index(comp))==0):
                    if(mylist.index(comp)!=mylist.index(item)):
                        newlist.append(mylist.index(comp))
    newlist.sort()
    newlist.reverse()
    for number in newlist:
        mylist.pop(number)
    newlist=mylist
    return(newlist)


def listjibe(list1,list2):
    common=[]
    final=[]
    for fir in list1:
        for sec in list2:
            if(fir==sec):
                common.append(fir)
    common.append("NULLNULLNULL")
    for iterator in common:
        while 1==1:
            if(len(list1)<1):
                break
            fir = list1.pop()
            if(fir!=iterator):
                final.append(fir)
            else : break
            
        while 1==1:
            if(len(list2)<1):
                break
            sec = list2.pop()
            if(sec!=iterator):
                final.append(sec)
            else :break
        if iterator!="NULLNULLNULL":
            final.append(iterator)
    return(final)

def textchange(string1):
    string1=" "+string1+" "
    file = open("common.txt")
    for line in file:
        myregex = re.compile(" "+line.strip()+" ", re.IGNORECASE)
        string1 = myregex.sub(" ",string1)
    for line in band:
        myregex = re.compile(" "+line.strip()+" ", re.IGNORECASE)
        string1 = myregex.sub(" ",string1)
    for line in song:
        myregex = re.compile(" "+line.strip()+" ", re.IGNORECASE)
        string1 = myregex.sub(" ",string1)
    for line in album:
        myregex = re.compile(" "+line.strip()+" ", re.IGNORECASE)
        string1 = myregex.sub(" ",string1)
    for line in similar:
        myregex = re.compile(" "+line.strip()+" ", re.IGNORECASE)
        string1 = myregex.sub(" ",string1)
    for line in popularity:
        myregex = re.compile(" "+line.strip()+" ", re.IGNORECASE)
        string1 = myregex.sub(" ",string1)
    for line in info:
        myregex = re.compile(" "+line.strip()+" ", re.IGNORECASE)
        string1 = myregex.sub(" ",string1)
    for line in makeList:
        myregex = re.compile(" "+line.strip()+" ", re.IGNORECASE)
        string1 = myregex.sub(" ",string1)
    return(string1);

def lastfm():
    greetingwords = ["hello","hi","yo","sup"];
    goodbyewords =["bye","later","lates","brb","goodbye"]
    greeted=0;
    greeting=0;
    
    
    
    print "Hello I am a lastfm chatbot"
    while(1==1):
        sentence=raw_input("");
        
        greeting=0
        confusion=0
        parting=0
        
        #null case
        if(len(sentence.split())<1):
            continue
            
        ###quotes case
        mylist=[]
        quotesfilter=""
        if((len(re.findall("\'",sentence))%2)==0 and len(re.findall("\'",sentence))>0):
            quotesfilter=re.findall("\'[\s\w\-]*\'",sentence)
        else :
            if((len(re.findall("\"",sentence))%2)==0):
                quotesfilter=re.findall('\"[\s\w\-]*\"',sentence)
        for object in quotesfilter:
            mylist.append(re.sub('\"',"",object))
        print("quot filter=" + str(mylist))
        ###
        
        ###Dictionary filter
        filter = re.sub("[\-\"\_\.\,\;\:]*","",sentence)
        filter=textchange(filter)
        print("Dict filter="+filter)
        ###
        
        ###uppercase case
        #caps lock check
        if((len(re.findall("[A-Z]", sentence))/len(sentence))>.8):
            casefilter=sentence.swapcase()
        else : casefilter=sentence
        #for some reason python doesn't like repetitions of white space
        temp=re.findall("[A-Z][\S]*\s[A-Z][\S]*\s[A-Z][\S]*\s[A-Z][\S]*", casefilter)
        temp.extend(re.findall("[A-Z][\S]*\s[A-Z][\S]*\s[A-Z][\S]*", casefilter))
        temp.extend(re.findall("[A-Z][\S]*\s[A-Z][\S]*", casefilter))
        temp.extend(re.findall("[A-Z][\S]*", casefilter))
        print("Case filter=" + str(temp))
        ####
        
        ###List Combiner
        if(len(quotesfilter)<4):
            quotesfilter=temp
        else :
            quotesfilter=[quotesfilter]
            quotesfilter.extend(temp)
        quotesfilter.extend([filter])
        ###
        
        
            
        
        #what is user talking about?
        #reset old thoughts
        reset()
        for word in sentence.split():
            word=word.lower()
            whatTopic(word)
            whatSubTopic(word)
            
            for term in greetingwords:
                if(term==word):
                    greeting=1
            for term in goodbyewords:
                if(term==word):
                    if(greeting==1):
                        confusion=1
                    parting=1
        
        
        ###Some Network brains
        for item in quotesfilter:
            item=re.sub("[^\w\s]*","",item)
            item=item.strip()
            #print(item)
            #print(topic)
            #print(make)
            #print(subTopic)
            info=translateToLastFm(item,topic,subTopic,make)
            try :
                info=str(info)
            except UnicodeEncodeError :
                info=info
            if(info=="fail"):
                continue
            info=re.sub("(\<[\w\s\'\"\:\;\,\.\?\/\=\+\-\_\@\!\#\$\%\^\&\*\(\)]*\>)*","",info)
            print("\nI have found something pertaining to the entity "+item+"\n\n"+info+"\n")
            break
        ###
        
        
        
        
        """
        if(confusion==1):
            print("Huh? ")
        if(parting==1):
            print("Bye ")
            break
        if(greeting==1):
            if(greeted==0):
                print("Hello, how are you doing? ")
            else :
                if(greeted<4):
                    print("Hello again ")
            greeted=greeted+1
        else:
            print "No response for that input"
        """

lastfm()
