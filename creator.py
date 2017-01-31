# -*- coding: utf-8 -*-

import os
import re
import logging

from jinja2 import Template
from lxml import etree
from collections import namedtuple
from constants import DIR, FT, IH, HD, IT, PT


logging.basicConfig(level=logging.ERROR)

Book = namedtuple('Book', ['book_directory', 'book_author', 'book_title', 'book_data'])

Chapter = namedtuple('Chapter', ['chapter_number', 'chapter_name', 'chapter_text'])


def xml_reader():
	"""Read XML files in the main directory, return books."""
	# Several XML files could be processed at once.
	# Makes sure XML files are properly formatted.
	# Modify the program to use different tags or file structure.
	files = os.listdir('.')
	books_list = []
	for fl in files:
		if fl.endswith('.xml'):
			# get book_directory, book author and book title.
			# if not given, use default values.
			book_directory = fl.split('.')[0]
			context = etree.iterparse(fl, tag='BookAuthor')
			tree = etree.parse(fl)
			for book in tree.xpath('//Book'):
				try:
					book_author = book.xpath('BookAuthor/text()')[0]
				except IndexError:
					book_author = 'Anonymous'
				try:
					book_title = book.xpath('BookTitle/text()')[0]
				except IndexError:
					book_title = 'An Unknown Book'
			# Get data for each chapter. If not given, use empty strings.
			chap_num_list = []
			chap_name_list = []
			chap_txt_list = []	
			context = etree.iterparse(fl, tag='ChapterNumber')
			for index, elem in context:
				num = elem.text
				chap_num_list.append(num) if num else chap_num_list.append('')
			context = etree.iterparse(fl, tag='ChapterName')
			for index, elem in context:
				name = elem.text
				chap_name_list.append(name) if name else chap_name_list.append('')
			context = etree.iterparse(fl, tag='ChapterText')
			for index, elem in context:
				txt = etree.tostring(elem)
				chap_txt_list.append(txt) if txt else chap_txt_list.append('')		
			
			try:
				assert (len(chap_num_list) == len(chap_name_list) == len(chap_txt_list))
			except AssertionError:
				logging.error(
					"XML file '{file}' is not formatted correctly. " 
					"A book cannot be created.".format(file=fl))
			# book_data is the main book content. It is a tuple of tuples,
			# representing each chapter.
			book_data = tuple(zip(chap_num_list, chap_name_list, chap_txt_list))
			try:
				assert len(book_data) > 0
			except AssertionError:
				logging.error('A book without content cannot be created.')
			# create a book
			xml_book = Book(
				book_directory=book_directory,
				book_author=book_author,
				book_title=book_title,
				book_data=book_data,
			)

			books_list.append(xml_book)
	return books_list


def file_factory(book):
	"""Create the index file and chapter files, write content."""
	# Create the list with chapter names and numbers. It will be used in the TOC.
	# if only a number or a name (like "Introduction") is given, it will also work. 
	chapters = []
	for book_chunk in book.book_data:
		if book_chunk[0] and book_chunk[1]:
			chapter = '. '.join(book_chunk[:2])
			chapters.append(chapter)
		else:
			chapter = book_chunk[0] or book_chunk[1]
			chapters.append(chapter)

	# chapter_string is used at the index page and in menus.
	chapter_string = '\n'.join(
		'<li><a href="{dir}{num}.html">'
		'{chapter}</a></li>'.format(
			dir=book.book_directory, 
			num=num, 
			chapter=chapter
			) for num, chapter in enumerate(chapters))

	footer_html = FT.render()

	ih_html = IH.render()

	# Create the index page (TOC), using the index template.
	index_html = IT.render(
		author=book.book_author, 
		title=book.book_title, 
		chapters=chapter_string, 
		index_header=ih_html, 
		footer=footer_html
		)
	# Write the index page.
	with open('index.html', 'w') as f:
		f.write(index_html)
	# Create individual chapter pages.
	for index, book_chunk in enumerate(book.book_data):
		file_name = '{dir}{index}.html'.format(dir=book.book_directory, index=index)
		# Create links to connect pages.
		# The index page (TOC) is the default. 
		previous = '{dir}{num}.html'.format(dir=book.book_directory, num=(index-1))
		next = '{dir}{num}.html'.format(dir=book.book_directory, num=(index+1))
		if index == 0:
			previous = 'index.html'
		if index == (len(book.book_data) - 1):
			next = 'index.html'
		# Write chapter pages, using the page template.
		with open(file_name, 'w') as g:
			page_html = PT.render(
				author=book.book_author, 
				title=book.book_title, 
				header=HD.render(),
				text=book.book_data[index][2], 
				chapters=chapter_string, 
				chapter=chapters[index], 
				prev=previous, 
				next=next,
				footer=footer_html
				)
			g.write(page_html)


def dir_factory(book):
	"""Create a book directory, call the function to create files."""
	if not os.path.exists(book.book_directory):
		os.makedirs(book.book_directory)
		os.chdir(book.book_directory)
		file_factory(book)
		os.chdir(DIR)
	else:
		os.chdir(book.book_directory)
		file_factory(book)
		os.chdir(DIR)


def creator():
	"""The main function that converts XML files into HTML books."""
	# XML files should be properly formatted and put into the main directory.
	# HTML books are using Twitter Bootstraps templates.
	books = xml_reader()
	for book in books:
		dir_factory(book)


if __name__=="__main__":
	creator()
