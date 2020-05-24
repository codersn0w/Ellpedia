#!/home/ellpedia/.pyenv/versions/anaconda3-4.4.0/bin/python
from wsgiref.handlers import CGIHandler
from webapp import app
CGIHandler().run(app)