# -*- coding: utf-8 -*-

from time import gmtime, strftime
import os

colour_red = "\033[1;31m"
colour_blue = "\033[1;34m"
colour_yellow = "\033[1;33m"
colour_green = "\033[1;32m"
colour_magenta = "\033[1;35m"
colour_remove= "\033[0m"
cur_dir=os.path.dirname(os.path.abspath(__file__))
verbose_switch = False

def RED(string):
	string=str(string)
	return (colour_red + string + colour_remove)

def BLUE(string):
	string=str(string)
	return (colour_blue + string + colour_remove)

def YELLOW(string):
	string=str(string)
	return (colour_yellow + string + colour_remove)

def GREEN(string):
	string=str(string)
	return (colour_green + string + colour_remove)

def blue(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+BLUE(' >> ' )+string)

def green(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+GREEN(' >> ' )+string)

def red(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+RED(' >> ' )+string)

def yellow(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+YELLOW(' >> ' )+string)

def verbose(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	if verbose_switch:
		print('['+log_time+']'+BLUE(' >> ' )+string)

def dump(vulnerable):
	for target,pipes in vulnerable.items():
		if len(pipes) == 0:
			print('%s: %s' % (GREEN(target),RED('no pipes accessible')))
		else:
			print('%s: %s' % (GREEN(target),pipes))



