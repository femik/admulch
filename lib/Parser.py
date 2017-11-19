
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

class Parser
	def is_ad_link(node, domain): #if its a link to anohter domain using a pic or swf, assume its an ad
		if node.img or node.embed:
			if domain not in node['href']:
				if 'http' in node['href']:
					return True
		return False

	def get_domain_stem(current_page):
		o = urlparse(current_page)
		return o.netloc.split('.')[-2]
		# this should use tldextract

	def get_domain(current_page):
		o = urlparse(current_page)
		return o.netloc

	def get_ad_links(htmlsoup, current_page):
		linkset = set()
		for a in htmlsoup.findAll('a', href=True):
			if Parser.is_ad_link(a, Parser.get_domain_stem(current_page)):
				g = urllib2.urlopen(a['href'])
				linkset.add(Parser.get_domain(g.geturl()))
		return linkset


	def build_counter(page_data): #strip text from web page, build dictionary/counter from it
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


	def analyze_page(the_page, stats):

		opener = urllib.FancyURLopener({})
		f = opener.open(the_page)
		soup = BeautifulSoup(f.read())
		s = URL(the_page).download()
		#i use both types of url opener
		stats.update_dict(Parser.build_counter(s), Parser.get_ad_links(soup, the_page), the_page)
		print 'Done'
