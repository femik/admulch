from queue import Queue
import Parser
import Stats

# A program to find the keywords/keyword density associated with various brands ads
# it creates a filtered word dictionary for each page and sums the keywords 
# associated with each brand across domains and globally
# You can use this to compare which keywords companies are purchasing ads on
# across domains and globally

# It determines which brand the ad is for by following the ad redirects to 
# its destination

# If i had a per-page traffic estimate i might use this to weight the results.

# Femi King


class KeywordMulcher:
	url_queue = Queue()
	stats = Stats()

    def __init__(self):
            self.url_queue.put('http://www.yahoo.com')
            self.url_queue.put('http://www.espn.com')
            self.started = False

    def start(self):
        self.started = True
        while !self.url_queue.empty() and self.started:
            url = self.url_queue.get()
            mulch_thread = threading.Thread(target=Parser.analyze_page, args=(url, self.stats))
            mulch_thread.start()

    def stop(self):
        self.started = False

    def empty(self):
        self.url_queue = Queue()
        
    def get_data(self):
        return stats.get()

    def process(self, data):
        for url in data:
            self.url_queue.put(url)

# should split into list parser, crawler, mulcher and reader classes
# crawler shoudl run in background thread or process 


	def do_print(self):
		for brand in self.brand_keywords_all.keys():
			print 'Ads for: ' + brand
			print self.brand_keywords_all[brand].most_common(40)

		for brand in self.brand_keywords_by_domain.keys():
			print 'Ads for: ' + brand
			for domain in self.brand_keywords_by_domain[brand].keys():
				print 'Ads found on this domain:' + domain
				print self.brand_keywords_by_domain[brand][domain].most_common(40)



#sample output
#Ads for: www.grantland.com
#Ads found on this domain:www.espn.com
#Top 40 keywords
#[(u'espn', 13), (u'watch', 12), (u'et', 9), (u'sports', 8), (u'nba', 6), (u'mlb', 6), (u'fantasy', 5), (u'games', 5), (u'baseball', 5), (u'pm', 5), (u'thu', 5), (u'video', 4), (u'nfl', 4), (u'nhl', 4), (u'draft', 4), (u'8', 4), (u'x', 4), (u'college', 4), (u'00', 4), (u'com', 4), (u'vs', 4), (u'tennis', 4), (u'sportsnation', 4), (u'insider', 3), (u'live', 3), (u'6', 3), (u'spelling', 3), (u'espn2', 3), (u'texas', 3), (u'golf', 3), (u'get', 3), (u'greatest', 3), (u'column', 3), (u'stories', 3), (u'm', 3), (u'finals', 3), (u'coach', 2), (u'skate', 2), (u'tv', 2), (u'p', 2)]
#Ads for: www.meetic.com
#Ads found on this domain:www.yahoo.com
#Top 40 keywords
#[(u'shareremove', 19), (u'5', 15), (u'yahoo', 13), (u'f', 12), (u'new', 9), (u'sign', 8), (u'weekend', 8), (u'0', 7), (u'kelly', 7), (u'news', 7), (u'may', 6), (u'celebrities', 6), (u'3', 6), (u'mlb', 6), (u'sports', 6), (u'hansen', 5), (u'high', 5), (u'johnson', 5), (u'28', 5), (u'bieber', 5), (u'permission', 5), (u'facebookwe', 5), (u'without', 5), (u'y', 5), (u'post', 5), (u'anything', 5), (u'stories', 5), (u'delete', 5), (u'time', 5), (u'cyprus', 4), (u'bryant', 4), (u'nba', 4), (u'healthy', 4), (u'bob', 4), (u'omg', 4), (u'today', 4), (u'man', 4), (u'year', 4), (u'one', 4), (u'dole', 4)]

# currently an ad for a companies facebook/twitter/aol page will be counted as an ad for facebook/twitter/aol
# the data might be cleaner if i use a whitelist for keywords instead of a blacklist
# this would simplify the data storage
# also remove the page name (yahoo/espn) from keywords
# i might amend this to store and compare other data about the ad campaign such as date/location/ad networks used/ad type
# i should connect this to some kind of crawler and some kind of database and some kind of front end
# lots of refactoring needed for this
# i'm ignoring js ads for now



