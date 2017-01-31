import os
from jinja2 import Template

DIR = os.getcwd()

# Get data from template files in 'templates' directory.

footer = os.path.sep.join(['templates', 'footer.html']) 
FT = Template(open(footer).read())

index_header = os.path.sep.join(['templates', 'index_header.html'])
IH = Template(open(index_header).read())

header = os.path.sep.join(['templates', 'header.html'])
HD = Template(open(header).read())

index_template = os.path.sep.join(['templates', 'index_template.html'])
IT = Template(open(index_template).read())

page_template = os.path.sep.join(['templates', 'page_template.html'])
PT = Template(open(page_template).read())