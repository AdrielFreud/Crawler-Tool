#/usr/bin/python

# Desenvolvido por Adriel Freud!
# Contato: usuariocargo2016@gmail.com 
# FB: http://www.facebook.com/xrn401
#   =>DebutySecTeamSecurity<=

# MODO DE USO: crawler.py http://site.com/
# OBS: Nao esqueca do 'HTTP' or 'HTTPS'

import urllib
import re
import argparse
from bs4 import BeautifulSoup
from time import sleep
import requests

menu = """\033[1;36m
  ____                    _            __        __   _     
 / ___|_ __ __ ___      _| | ___ _ __  \ \      / /__| |__  
| |   | '__/ _` \ \ /\ / / |/ _ \ '__|  \ \ /\ / / _ \ '_ \ 
| |___| | | (_| |\ V  V /| |  __/ |      \ V  V /  __/ |_) |
 \____|_|  \__,_| \_/\_/ |_|\___|_|       \_/\_/ \___|_.__/ 
                                                            
Powered by Adriel Freud\n\033[1;m""" 

parse = argparse.ArgumentParser(description="Url for Get Informations of WebSite")
parse.add_argument("-u", "--url", help="Url for get Informations! ")
args = parse.parse_args()

header = {'user-agent': 'Mozilla/5.0 (X11; Linux i686; rv:43.0) Gecko/10100101 Firefox/43.0 Iceweasel/43.0.4'}

def email_extrator(url):
	print("\n\033[1;36m<==================== Emails! ====================> \033[1;m")
	abrir = requests.get(url, headers=header)
	code = abrir.text
	e_mail = re.findall(r"[\w.]+[\w-]+[\w_]+[\w.]+[\w-]+[\w_]@[\w.]+[\w-]+[\w_]+[\w.]+[\w-]+[\w_]",code)
	for emails in e_mail:
		print('\n\033[31m[*][==>] Email: \033[1;m' + str(emails))

def whois(url):
	site = 'https://www.whois.com/whois/{0}'.format(url)
	req = requests.get(site, headers=header)
	code = req.status_code
	if code == 200:
		print("")
		html = req.text
		bs = BeautifulSoup(html, 'lxml')
		div = bs.find_all('pre', {'class':'df-raw'})
		for divs in div:
			print('\033[1;36m<==================== info ==================>\n\n \033[1;m \n%s'%divs.get_text())

def capture(url):
	abrir = urllib.urlopen(url)
	resp = abrir.code
	if resp == 200:
		print("\n[*]Request Succefully!\n")
		bt = BeautifulSoup(abrir.read(), "lxml")
		allinks = bt.find_all('a')
		try:
			allinks0 = bt.find_all('meta')
			print("\033[1;36m<================== Information ==================>\n\n \033[1;m ")
			for link in allinks0:
				print("\033[31m[!][==>] Information: \033[1;m"+ str(link['content']))
				print("")
		except:
			pass		

		link1 = bt.link['href']
		link2 = bt.img['src']

		html = abrir.read()
		l = re.findall(r'<a href="?\'?(https?:\/\/[^"\'>]*)', html)
		print("\033[1;36m<==================== Links ====================>\n\n \033[1;m ")
		print("\033[31m[+][==>] Links Externos: \033[1;m"+ str(link1))
		print("")
		print("\033[31m[+][==>] Links Locais: \033[1;m"+ str(link2))
		for o in l:
			print("\033[31m[+][==>] Link: \033[1;m"+ str(o))
			print("")
			print("")
		for link in allinks:
			try:
				print("\033[31m[+][==>] Link: \033[1;m"+ str(link['href']))
				print("")
			except:
				continue

	else:
		print("\n\033[31m[!]Request Failed, Exiting Program...\n \033[1;m")
		sleep(5)
		exit()

if args.url:
	print(menu)
	req = requests.get(args.url, headers=header)
	print('[+] Connection: %s'%req.request.headers['Connection']) 
	print('[+] Accept-Encoding: %s'%req.request.headers['Accept-Encoding'])
	print('[+] Accept: %s'%req.request.headers['Accept'])
	print('[+] User-Agent: %s'%req.request.headers['user-agent'])
	capture(args.url)
	whois(args.url)
	email_extrator(args.url)
else:
	print(menu)
	parse.print_help()
