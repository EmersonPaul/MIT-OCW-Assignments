# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self. description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()
    
    def is_phrase_in(self, text):
        new_text = ''
        for character in text.lower():
            if character in string.punctuation:
                new_text += ' '
            else:
                new_text += character
                
        new_text = new_text.split()
        key_phrase = self.phrase.split()

        end = len(key_phrase)

        for i in range(len(new_text)):
            if key_phrase == new_text[i:i+end] and len(new_text) - i >= end:
                return True
        return False
        
# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def evaluate(self, title):
        story_title = NewsStory.get_title(title)
        return super().is_phrase_in(story_title)
    
# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, description):
        story_description = NewsStory.get_description(description)
        return super().is_phrase_in(story_description)

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, date_and_time):
        self.date = datetime.strptime(date_and_time, '%d %b %Y %H:%M:%S')
    
    def get_date_and_time(self):
        return self.date.replace(tzinfo=pytz.UTC)

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self,date_and_time):
        super().__init__(date_and_time)
    
    def evaluate(self, NewsStory):
        story_date_and_time = NewsStory.get_pubdate()
        return story_date_and_time.replace(tzinfo=pytz.UTC) < super().get_date_and_time()

class AfterTrigger(TimeTrigger):
    def __init__(self,date_and_time):
        super().__init__(date_and_time)
    
    def evaluate(self, NewsStory):
        story_date_and_time = NewsStory.get_pubdate()
        return story_date_and_time.replace(tzinfo=pytz.UTC) > super().get_date_and_time()

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, TriggerVariant):
        self.Trigger_Type = TriggerVariant
    
    def evaluate(self, NewsStory):
        return not self.Trigger_Type.evaluate(NewsStory)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, FirstTrigger, SecondTrigger):
        self.First_Operand = FirstTrigger
        self.Second_Operand = SecondTrigger
    
    def evaluate(self, NewsStory):
        return (self.First_Operand.evaluate(NewsStory) and 
                self.Second_Operand.evaluate(NewsStory))

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, FirstTrigger, SecondTrigger):
        self.First_Operand = FirstTrigger
        self.Second_Operand = SecondTrigger
    
    def evaluate(self, NewsStory):
        return (self.First_Operand.evaluate(NewsStory) or 
                self.Second_Operand.evaluate(NewsStory))

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    
    valid_stories = []
    for trigger_type in triggerlist:
        for story in stories:
            if trigger_type.evaluate(story) and story not in valid_stories:
                valid_stories.append(story)
                continue
    
    return valid_stories

#======================
# User-Specified Triggers
#======================
# Problem 11
    
def trigger_to_use(config):
    trigger_types = {'TITLE':TitleTrigger,
                     'DESCRIPTION': DescriptionTrigger,
                     'AFTER': AfterTrigger,
                     'BEFORE': BeforeTrigger,
                     'AND': AndTrigger,
                     'OR': OrTrigger,
                     'NOT': NotTrigger,}
    
    return trigger_types[config]

def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    
    temp_trig = {}
    trig_list = []
    
    # Following the configuration file format per line:
    # [triggerName, triggerType, argument, argument(2) <- if using AND/OR triggers]
    # [ ^index 0  , ^index 1   , ^index 2, ^index 3 ] <- trig_config
    
    for line in lines:
        trig_config = line.split(',')
        if 'ADD' in line:
            configs = line.split(',')[1:]
            for element in configs:
                trig_list.append(temp_trig.values(element))
            
        elif 'AND' in line or 'OR' in line:
            first_cond = temp_trig.values(trig_config[2])
            second_cond = temp_trig.values(trig_config[3])
            will_be_used = trigger_to_use(trig_config[1])
            temp_trig[trig_config[0]] = will_be_used(first_cond, second_cond)
            
        else:
            will_be_used = trigger_to_use(trig_config[1])
            temp_trig[trig_config[0]] = will_be_used(trig_config[2])
    
    print(lines) # for now, print it so you see what it contains!
    return trig_list


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

