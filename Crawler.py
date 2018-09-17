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
args = parse.parse_args()

header = {'user-agent': 'Mozilla/5.0 (X11; Linux i686; rv:43.0) Gecko/10100101 Firefox/43.0 Iceweasel/43.0.4'}

def printar_detalhes(url):
	IP = socket.gethostbyname(url.strip('https://'))
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

		a_ref = bt.find_all('a')
		meta = bt.find_all('link')
		try:
			href = bt.link['href']
			img = bt.img['src']
			if href != None:
				print("\033[1;36m<==================== Links ====================>\n\n")
				if 'http' in href:
					print("\033[31m"+t+"[==>] Links Externos: %s"%href)

				print("\033[31m"+t+"[==>] Links Externos: http://%s"%href)
				if img != None:
					print("\033[31m"+t+"[==>] Links Locais: http://%s"%img)
		except:
			pass

		if a_ref != None:
			for link in a_ref:
				try:
					if 'http' in link['href']:
						print("\033[31m"+t+"[==>] Link: %s"%link['href'])
				except:
					pass

		if meta != None:
			print("\033[1;36m<================== Information ==================>\n\n")
			for link in meta:
				try:
					print("\033[31m"+t+"[==>] Information: %s"%link['href'])
					print("")
				except:
					pass
	else:
		print("\n\033[31m[!]Request Failed, Exiting Program...\n ")
		sleep(5)
		sys.exit()

if args.url:
	print(menu)
	req = requests.get(args.url, headers=header)
	c = urllib2.urlopen(args.url)
	print(c.info())
	capture(args.url)
	try:
		printar_detalhes(args.url)
	except:
		print("Impossivel Resolver Servidor DNS!\n")
	whois(args.url)
	email_extrator(args.url)
else:
	print(menu)
	parse.print_help()
