#!/usr/bin/python
# -*- coding: utf-8 -*- 
import logger,sys
sys.path.insert(0, 'lib/')

def show(mode):
	print(logger.RED(''))
	print(logger.RED('███╗   ███╗███████╗ ██╗███████╗       ██████╗  ██╗ ██████╗ ...zzz_%s' % logger.RED(mode)))
	print(logger.RED('████╗ ████║██╔════╝███║╚════██║      ██╔═████╗███║██╔═████╗'))
	print(logger.RED('██╔████╔██║███████╗╚██║    ██╔╝█████╗██║██╔██║╚██║██║██╔██║'))
	print(logger.RED('██║╚██╔╝██║╚════██║ ██║   ██╔╝ ╚════╝████╔╝██║ ██║████╔╝██║'))
	print(logger.RED('██║ ╚═╝ ██║███████║ ██║   ██║        ╚██████╔╝ ██║╚██████╔╝'))
	print(logger.RED('╚═╝     ╚═╝╚══════╝ ╚═╝   ╚═╝         ╚═════╝  ╚═╝ ╚═════╝ '))
	print(logger.RED(''))
