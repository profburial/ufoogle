from flask import request, redirect, url_for, render_template
from ..models import search
import json


class Search:

    def keyword(self, type=''):
        # Get search query
        keyword = request.args.get('q', '')

        # Get Page
        page = request.args.get('page', '')

        # If no query, they are dicks
        if not keyword:
            return redirect(url_for('home'))

        # If page isn't set, it's page 1
        if not page:
            page = '1'

        # Execute search and get results
        results = search.Search(page).keyword(keyword)

        # Return Response with Search Results
        if type == 'json':
            return json.dumps(dict(results))
        else:
            return render_template('results.html', data=results)
