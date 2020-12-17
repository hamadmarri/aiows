
import sys
import os
from subprocess import Popen, PIPE
import threading
import time

import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
import urllib

width = os.get_terminal_size().columns
tmp_file = None
text = ""
result_number = 1
result_max = 30

p = Popen('less', stdin=PIPE, bufsize=0)

def google_fetch(search, start=0):
	
	if start == 0:
		search = f'https://www.google.com/search?hl=en-US&q={search}'
	else:
		search = f'https://www.google.com/search?hl=en-US&q={search}&start={start}'

	html = requests.get(search)
	
	if html.status_code==200:
		soup = BeautifulSoup(html.text, 'lxml')
		h3s = soup.find_all('h3')

		for h3 in h3s:
			e = {}

			title = h3.find("div").text
			a = h3.parent
			href = a.get("href")
			
			if not href:
				continue
			
			try:
				sub_title = h3.nextSibling.text
			except:
				sub_title = ""
	
			try:
				desciption = a.parent.nextSibling.nextSibling

				for i in range(0, 5):
					try:
						child = desciption.find("div")
						if child:
							desciption = desciption.find("div")
						else:
							break
					except:
						pass

				desciption = desciption.text
			except:
				desciption = ""


			e["title"]		= title
			e["sub_title"]	= sub_title
			e["link"]		= urllib.parse.unquote(href[len("/url?q="):href.index("&")])
			e["desciption"]	= desciption
			
			format(e, "\033[0;4;31mG\033[0m")
		
		# next page
		if result_number < result_max:
			time.sleep(5)
			google_fetch(search, result_number)
	
	p.stdin.close()
	

def format(e, prefix="?"):
	global result_number
	text	= str(result_number) + ":"
	
	for i in range(0, width - (3 + len(str(result_number)))):
		text += " "
	
	text	+= prefix								+ "\n"
	text	+= "\033[1;32m" 	+ e["title"]		+ "\033[0m\n"
	text	+= "\033[0;33m"		+ e["sub_title"]	+ "\033[0m\n"
	text	+= "\033[0;34m"		+ e["link"]			+ "\033[0m\n\n"
	text	+= e["desciption"]

	# print(text)
	print_less(text)
	print_separator()
	
	result_number += 1




def print_separator():
	print_less("\n\33[0;35m")
	for i in range(0, width):
		print_less("-")
	print_less("\33[0m\n")


def print_less(text):
	p.stdin.write(str.encode(text))


search = " ".join(sys.argv[1:])
print_less(f"Search: {search}")
print_separator()

google_fetch(search)


p.wait()
