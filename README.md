
Static Site Creator
===================

This code converts a single XML file with a book into a directory with HTML files that can be published online. Twitter Bootstraps templates are used for HTML. The index file contains the table of contents with appropriate links. Other files contain chapters, and those files are linked to each other. 

In the 'demo' folder you will find a sample XML book converted into HTML files.

Once your XML file is ready, put it into the main directory, and run `creator.py`. You can also process several XML files at once.

Requirements
------------

Python 2.7

You also need to install Jinja2 and lxml libraries.

This code was tested on Windows and Mac OS X.


Notes
-----

Make sure the XML file is properly formatted. 

You also need to customise index header, header, and footer from 'templates', to avoid broken/missing links.

If some nodes in your XML file have different names, you can change the code to suit your needs. 

Author
-----_

Andrey Yashurin

Please write me to yashurin@gmail.com with your comments and suggestions.

License
-------

This work is licensed under a Creative Commons Attribution 3.0 Unported License.

http://creativecommons.org/licenses/by/3.0/deed.en_US
