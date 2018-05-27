#!/usr/bin/python

import os
import sys
import argparse
import requests
import threading

def banner():
 	print "\n ____        _     ____             _       "
 	print "/ ___| _   _| |__ | __ ) _ __ _   _| |_ ___ "
 	print "\___ \| | | | '_ \|  _ \| '__| | | | __/ _ \\"
	print " ___) | |_| | |_) | |_) | |  | |_| | ||  __/"
	print "|____/ \__,_|_.__/|____/|_|   \__,_|\__\___|Coded by: mqc\n\n"

def check(sub):
	try:
		requests.get(sub)
		return 0
	except requests.exceptions.ConnectionError:
		return 1

def brute():
	while 1:
		with lock:
			sub = wordlist.readline().strip()
			if sub == "":
				break
			sub = "http://" + sub + "." + url
		o = check(sub)
		with lock:
			if o == 1:
				print "[!] Incorrect: " + sub
			else:
				print "[+] Found: " + sub

def main():
	banner()
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--url", dest="url", type=str, help="target url")
	parser.add_argument("-w", "--wordlist", dest="wordlist", type=str, help="wordlist file")
	parser.add_argument("-t", "--threads", dest="threads", type=int, help="threads number")
	args = parser.parse_args()
	if args.url and args.wordlist:
		global url
		global lock
		global wordlist
		url = args.url
		lock = threading.Lock()
		wordlist = args.wordlist
		try:
			wordlist = open(wordlist, "r")
			print "[+] Testing connection to target url"
			requests.get("http://" + url)
			print "[+] Starting brute force on: " + url
			if args.threads:
				for i in range(args.threads):
					threading.Thread(target=brute).start()
			else:
				brute()
		except IOError:
			print "[!] Error: wrong wordlist file"
		except requests.exceptions.ConnectionError:
			print "[!] Error: cannot connect to target url"
	else:
		print "[!] Usage1: python SubBrute.py -u <example.com> -w <wordlist.lst>"
		print "[!] Usage2: python SubBrute.py -u <example.com> -w <wordlist.lst> -t <threads_number>"

try:
	main()
except KeyboardInterrupt:
	sys.exit()
