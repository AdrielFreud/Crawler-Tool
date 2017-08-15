#/usr/bin/python

# Desenvolvido por Adriel Freud!
# Contato: usuariocargo2016@gmail.com 
# FB: http://www.facebook.com/xrn401
#   =>DebutySecTeamSecurity<=

# MODO DE USO: crawler.py http://site.com/
# OBS: Nao esqueca do 'HTTP' or 'HTTPS'

import re
import argparse
from bs4 import BeautifulSoup
from time import sleep
import requests
import socket
import json
import sys
import time, datetime

ts = time.time()
dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
today = datetime.datetime.today()
t = today.strftime("[%H:%M:%S] - ")

menu = """\033[1;36m
  ____                    _            __        __   _     
 / ___|_ __ __ ___      _| | ___ _ __  \ \      / /__| |__  
| |   | '__/ _` \ \ /\ / / |/ _ \ '__|  \ \ /\ / / _ \ '_ \ 
| |___| | | (_| |\ V  V /| |  __/ |      \ V  V /  __/ |_) |
 \____|_|  \__,_| \_/\_/ |_|\___|_|       \_/\_/ \___|_.__/ 
                                                            
Powered by Adriel Freud\n""" 

parse = argparse.ArgumentParser(description="Url for Get Informations of WebSite")
parse.add_argument("-u", "--url", help="Url for get Informations! ")
args = parse.parse_args()

header = {'user-agent': 'Mozilla/5.0 (X11; Linux i686; rv:43.0) Gecko/10100101 Firefox/43.0 Iceweasel/43.0.4'}

def printar_detalhes(url):
	if 'https://' in url:
		IP = socket.gethostbyname(url.strip('https://'))

	elif 'http://' in url:
		IP = socket.gethostbyname(url.strip('http://'))

	req = requests.get('http://ip-api.com/json/'+IP, headers=header)
	Geo = json.loads(req.text)
	print('')
	print('IP: %s'%Geo['query']+'\n')
	print('Country: %s'%Geo['country']+'\n')
	print('Country code: %s'%Geo['countryCode']+'\n')
	print('Region: %s'%Geo['regionName']+'\n')
	print('Region code: %s'%Geo['region']+'\n')
	print('City: %s'%Geo['city']+'\n')
	print('Zip Code: %s'%Geo['zip']+'\n')
	print('Latitude: %s'%Geo['lat']+'\n')
	print('Longitude: %s'%Geo['lon']+'\n')
	print('Timezone: %s'%Geo['timezone']+'\n')
	print('ISP: %s'%Geo['isp']+'\n')
	print('Organization: %s'%Geo['org']+'\n')
	print('AS number/name: %s'%Geo['as']+'\n')

def email_extrator(url):
	print("\n\033[1;36m<==================== Emails! ====================>")
	abrir = requests.get(url, headers=header)
	code = abrir.text
	e_mail = re.findall(r"[\w.]+[\w-]+[\w_]+[\w.]+[\w-]+[\w_]@[\w.]+[\w-]+[\w_]+[\w.]+[\w-]+[\w_]",code)
	for emails in e_mail:
		print('\n\033[31m'+t+'[==>] Email: \033[1;m' + str(emails))

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
			print('\033[1;36m<==================== info ==================>\n\n%s'%divs.get_text())

def capture(url):
	req = requests.get(url, headers=header)
	code = req.status_code
	html = req.text
	if code == 200:
		print("\n[*]Request Succefully!\n")
		bt = BeautifulSoup(html, "lxml")
		allinks = bt.find_all('a')
		try:
			allinks0 = bt.find_all('meta')
			print("\033[1;36m<================== Information ==================>\n\n")
			for link in allinks0:
				print("\033[31m"+t+"[==>] Information: "+ str(link['content']))
				print("")
		except:
			pass		

		link1 = bt.link['href']
		link2 = bt.img['src']

		html = req.text
		l = re.findall(r'<a href="?\'?(https?:\/\/[^"\'>]*)', html)
		print("\033[1;36m<==================== Links ====================>\n\n")
		print("\033[31m"+t+"[==>] Links Externos:"+ str(link1))
		print("")
		print("\033[31m"+t+"[==>] Links Locais: "+ str(link2))
		for o in l:
			print("\033[31m"+t+"[==>] Link: "+ str(o))
			print("")
			print("")
		for link in allinks:
			try:
				print("\033[31m"+t+"[==>] Link: "+ str(link['href']))
				print("")
			except:
				continue

	else:
		print("\n\033[31m[!]Request Failed, Exiting Program...\n ")
		sleep(5)
		sys.exit()

if args.url:
	print(menu)
	req = requests.get(args.url, headers=header)
	print('\033[31m[+] Connection: %s'%req.request.headers['Connection']) 
	print('\033[31m[+] Accept-Encoding: %s'%req.request.headers['Accept-Encoding'])
	print('\033[31m[+] Accept: %s'%req.request.headers['Accept'])
	print('\033[31m[+] User-Agent: %s'%req.request.headers['user-agent'])
	capture(args.url)
	printar_detalhes(args.url)
	whois(args.url)
	email_extrator(args.url)
else:
	print(menu)
	parse.print_help()
