"""
Simple Methods for Searching Elasticsearch

TODO: Applying search filters is butt...clean that up.
"""


from elasticsearch import Elasticsearch
import math


class Search():

    #Set Elasticsearch, Page, Items, and Page Offset
    def __init__(self, page):
        #Elasticsearch Connection
        self.es = Elasticsearch()

        # Set page
        self.page = int(page)

        # Set request size
        self.items = 20

        # Set Page Offset
        if self.page == 1:
            self.pageOffset = 0
        else:
            self.pageOffset = (self.items * self.page) - self.items

    # Search by Keyword
    def keyword(self, keyword):

        # Build Query
        query = self.buildQuery(keyword)

        # # Get fields
        # type = self.queryType(keyword)

        # # Set fields
        # fields = self.setFields(type)

        # # Get Keyword
        # searchKeyword = self.getKeyword(keyword)

        # # Set query
        # query = self.getQuery(type, fields, searchKeyword)

        # Search for keyword
        results = self.es.search(
            index='ufo',
            body={
                "from": self.pageOffset,
                "size": self.items,
                "sort": [{"occurred": "desc"}],
                "query": {
                    "bool": {
                        "must": [ eval(query) ],
                        "minimum_should_match": 1,
                        "boost": 1
                    }
                }
            })

        # Get Pages
        pages = math.ceil(float(results['hits']['total']) / self.items)

        # Format Results
        data = {
            'results': results['hits']['hits'],
            'page': self.page,
            'query': keyword,
            'pages': pages,
            'count': results['hits']['total']
        }

        return data

    # Build Query
    def buildQuery(self, keyword):
        indicator = keyword.split('^')

        if len(indicator) > 1:
            query = ''
            for keyword in indicator:
                # Get fields
                type = self.queryType(keyword.strip())

                # Set fields
                fields = self.setFields(type)

                # Get Keyword
                searchKeyword = self.getKeyword(keyword.strip())

                # Set query
                query += str(self.getQuery(type, fields, searchKeyword)) + ','

            return query
        else:
            # Get fields
            type = self.queryType(keyword)

            # Set fields
            fields = self.setFields(type)

            # Get Keyword
            searchKeyword = self.getKeyword(keyword)

            # Set query
            return str(self.getQuery(type, fields, searchKeyword))

    # Get Keyword
    def getKeyword(self, keyword):
        indicator = keyword.split(':')

        if len(indicator) > 1:
            return indicator[0]
        else:
            return keyword

    # Get Query
    def getQuery(self, type, fields, keyword):
        if type is None:
            query = {
                "multi_match": {
                    "query": keyword,
                    "fields": fields
                }
            }
        else:
            query = {
                "multi_match": {
                    "query": keyword,
                    "type": "phrase",
                    "fields": fields
                }
            }

        return query

    # Get query type (:location: :description:)
    def queryType(self, keyword):

        # Get type indicator
        indicator = keyword.split(':')

        # Determine indicator
        if len(indicator) > 1:
            type = indicator[1]
        else:
            type = None

        return type

    # Set fields for search
    def setFields(self, type):

        # Set fields
        if type is None:
            return ['city', 'state', 'description']
        else:
            return [type]
