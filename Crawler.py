#!/usr/bin/python

# Desenvolvido por Adriel Freud!
# Contato: businessc0rp2k17@gmail.com
# FB: http://www.facebook.com/xrn401
#   =>DebutySecTeamSecurity<=
#conding: utf-8

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
import urllib2

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

parse = argparse.ArgumentParser(description="For Get Informations of WebSite")
parse.add_argument("-u", "--url", help="Url for get Informations! ")
parse.add_argument("-p", "--proxy", help="Set a proxy! ")
parse.add_argument("-c", "--cookie", help="Set a Cookie ")
parse.add_argument("-d", "--data", help="Set a forms ")
args = parse.parse_args()

header = {'user-agent': 'Mozilla/5.0 (X11; Linux i686; rv:43.0) Gecko/10100101 Firefox/43.0 Iceweasel/43.0.4'}

def printar_detalhes(url):
	IP = socket.gethostbyname(url.strip('https://'))
	req = requests.get('http://ip-api.com/json/'+IP, headers=header)
	Geo = json.loads(req.text)
	print('\nIP: %s\n'%Geo['query'])
	print('Country: %s\n'%Geo['country'])
	print('Country code: %s\n'%Geo['countryCode'])
	print('Region: %s\n'%Geo['regionName'])
	print('Region code: %s\n'%Geo['region'])
	print('City: %s\n'%Geo['city'])
	print('Zip Code: %s\n'%Geo['zip'])
	print('Latitude: %s\n'%Geo['lat'])
	print('Longitude: %s\n'%Geo['lon'])
	print('Timezone: %s\n'%Geo['timezone'])
	print('ISP: %s\n'%Geo['isp'])
	print('Organization: %s\n'%Geo['org'])
	print('AS number/name: %s\n'%Geo['as'])

def email_extrator(url):
	print("\n\033[1;36m<==================== Emails! ====================>")
	abrir = requests.get(url, headers=header)
	code = abrir.text
	e_mail = re.findall(r"[\w.]+[\w-]+[\w_]+[\w.]+[\w-]+[\w_]@[\w.]+[\w-]+[\w_]+[\w.]+[\w-]+[\w_]",code)
	
	if e_mail:
		for emails in e_mail:
			try:
				print('\n\033[31m'+t+'[==>] Email: %s'%emails)
			except:
				pass
	else:
		exit(0)

def whois(url):
	site = 'https://www.whois.com/whois/{0}'.format(url)
	req = requests.get(site, headers=header)
	code = req.status_code
	if code == 200:
		print("")
		html = req.text
		bs = BeautifulSoup(html, "html.parser")
		div = bs.find_all("pre", {"class":"df-raw"})
		for divs in div:
			print('\033[1;36m<==================== info ==================>\n\n%s'%divs.get_text().encode('utf-8'))

def capture(url):
	req = requests.get(url, headers=header)
	code = req.status_code
	if code == 200:
		html = req.text
		print("\n[*]Request Succefully!\n")
		bt = BeautifulSoup(html, "html.parser")
		urls = re.findall('(?<=href=["\'])https?://.+?(?=["\'])', html)
		print("\033[1;36m<==================== Links ====================>\n\n")
		for u in urls:
			print("\033[31m"+t+"[==>] Links: %s"%u)
	else:
		print("\n\033[31m[!]Request Failed, Exiting Program...\n ")
		sleep(3)
		exit(1)

def grabbining(url, proxy, cookie, form):

	exec("forms = %s"%form)
	esc = raw_input("GET/POST | [p][g] | \\[G]: ")
	if esc.lower() == "p":
		req = requests.post(url, headers=header, proxies={'http': proxy,'https': proxy}, params=forms, cookies={'Cookie':cookie})
	else:
		req = requests.get(url, headers=header, proxies={'http': proxy,'https': proxy}, params=forms, cookies={'Cookie':cookie})

	code = req.status_code
	if code == 200:
		html = req.text
		print("\n[*]Request Succefully!\n")
		print("\033[1;36m<==================== Information ====================>\n\n\n")
		print(html.encode('utf-8'))
	else:
		print("\n\033[31m[!]Request Failed, Exiting Program...\n ")
		sleep(3)
		exit(1)

if args.url:
	print(menu)
	if len(sys.argv) > 3:
		url = sys.argv[2]
		proxy = sys.argv[4]
		cookie = sys.argv[6]
		parametros = sys.argv[8]
		grabbining(url, proxy, cookie, parametros)
	else:
		print(urllib2.urlopen(args.url).info())
		capture(args.url)

		try:
			printar_detalhes(args.url)
		except:
			pass
		whois(args.url)
		email_extrator(args.url)
else:
	print(menu)
	parse.print_help()
