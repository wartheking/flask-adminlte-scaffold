#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from app import create_app

def jinja_max(iterable):
    return max(iterable)

def jinja_min(iterable):
    return min(iterable)


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.jinja_env.filters['max'] = jinja_max
app.jinja_env.filters['min'] = jinja_min

if __name__ == '__main__':
    app.run(debug=True)
