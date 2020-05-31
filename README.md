# YelpScraper
Yelp fusion API to find points of interest in King County and Washington

example_config.json is a template to create config.json, which holds API access keys

### POI Scraping Workflow ###
 - yelp_query.py - to search business by location and category (loop through wa town files is an attempt to avoid the daily request limit)
 - query_spec_biz_terms.py - go back and use more specific category aliases to query any cities that had more than 1000 results for a general category _(this is a little hacky, but we're working around the 1,000 limit for query results while also keeping the daily request limit under 5,000)_
 - combine_restaurant_query_results.py - go back and pick up dataframes from various queries and deduplicate
