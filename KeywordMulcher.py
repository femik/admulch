
import re
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup 
import nltk
import pattern.web 
from pattern.web import URL, extension, plaintext
from nltk.corpus import stopwords
from urlparse import urlparse
import collections

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
	page_list = ['http://www.yahoo.com', 'http://www.espn.com']
	brand_keywords_all = {}
	brand_keywords_by_domain = {}
	brand_keywords_by_page = {}

	def mulch(self):
		for page in self.page_list:
			print page
			self.analyze_page(page)
		print 'mulched'

	def is_ad_link(self, node, domain): #if its a link to anohter domain using a pic or swf, assume its an ad
		if node.img or node.embed:
			if domain not in node['href']:
				if 'http' in node['href']:
					return True
		return False

	def get_domain_stem(self, current_page):
		o = urlparse(current_page)
		return o.netloc.split('.')[-2]
		# this should use tldextract

	def get_domain(self, current_page):
		o = urlparse(current_page)
		return o.netloc

	def get_ad_links(self, htmlsoup, current_page):
		linkset = set()
		for a in htmlsoup.findAll('a', href=True):
			if self.is_ad_link(a, self.get_domain_stem(current_page)):
				g = urllib2.urlopen(a['href'])
				linkset.add(self.get_domain(g.geturl()))
		return linkset


	def build_counter(self, page_data): #strip text from web page, build dictionary/counter from it
		s = pattern.web.plaintext(page_data).lower()
		s = re.findall("\w+", s, re.U)
		# strip punct, remove stopwords
		# maybe this should be a whitelist of the top 10000 most common keywords instead of a blacklist

		punctuation = re.compile(r'[.?!,":;]') 
		stopwords = ['all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once', 're', 've', 'll']

		newlist = list()
		freq = collections.Counter()

		for word in s:
			word = punctuation.sub("", word)
			if word not in stopwords:
				newlist.append(word)
		freq.update(newlist)
		return freq


	def analyze_page(self, the_page):

		opener = urllib.FancyURLopener({})
		f = opener.open(the_page)
		soup = BeautifulSoup(f.read())
		s = URL(the_page).download()
		#i use both types of url opener
		self.update_dict(self.build_counter(s), self.get_ad_links(soup, the_page), the_page)
		print 'Done'

	def update_dict(self, the_word_counts, ad_links, the_page):
		for ad in ad_links:
			if ad in self.brand_keywords_all:
				self.brand_keywords_all[ad] = self.brand_keywords_all[ad] + the_word_counts
			else:
				self.brand_keywords_all[ad] = the_word_counts

		dm = self.get_domain(the_page)

		for ad in ad_links:
			if ad in self.brand_keywords_by_domain:
				if dm in self.brand_keywords_by_domain[ad]:
					self.brand_keywords_by_domain[ad][dm] = self.brand_keywords_by_domain[ad][dm] + the_word_counts
				else:
					self.brand_keywords_by_domain[ad][dm] = the_word_counts
			else:
				self.brand_keywords_by_domain[ad] = {}
				self.brand_keywords_by_domain[ad][dm] = the_word_counts

	def do_print(self):
		for brand in self.brand_keywords_all.keys():
			print 'Ads for: ' + brand
			print self.brand_keywords_all[brand].most_common(40)

		for brand in self.brand_keywords_by_domain.keys():
			print 'Ads for: ' + brand
			for domain in self.brand_keywords_by_domain[brand].keys():
				print 'Ads found on this domain:' + domain
				print self.brand_keywords_by_domain[brand][domain].most_common(40)



a = KeywordMulcher()
a.mulch()
a.do_print()
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



