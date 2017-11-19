import threading

class Stats
    def __init__(self):
        self.brand_keywords_all = {}
        self.brand_keywords_by_domain = {}
        self.brand_keywords_by_page = {}
        self.lock = threading.Lock()

	def update_dict(self, the_word_counts, ad_links, the_page):
	    with self.lock:
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

    def get():
        return self.brand_keywords_by_domain, self.brand_keywords_all