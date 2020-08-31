#!/usr/bin/python
# -*- encoding: utf-8 -*- 

from impacket import smb, smbconnection, nt_errors
from impacket.uuid import uuidtup_to_bin
from impacket.dcerpc.v5.rpcrt import DCERPCException
from struct import pack
import argparse, sys

from netaddr import IPNetwork

sys.path.insert(0, 'lib/')
import logger, banner
from mysmb import MYSMB

parser = argparse.ArgumentParser(description="MS17-010 Checker")
parser.add_argument("-t","--targets", metavar="",required=True, help="Target(s) to attack")
parser.add_argument("-u", "--user", type=str, metavar="",help="username to authenticate with")
parser.add_argument("-p", "--password", type=str, metavar="",help="password for specified user")
parser.add_argument("-d", "--domain", type=str, metavar="",help="domain for specified user")
args = parser.parse_args()

if args.user:
	if args.password == None:
		logger.red('Please specify username and password')
		quit()
	else:
		username = args.user
		password = args.password
else:
	username = ''

if args.password:
	if args.user == None:
		logger.red('Please specify username and password')
		quit()
	else:
		username = args.user
		password = args.password
else:
	password = ''

if args.domain:
	domain = args.domain
else:
	domain = ''

vulnerable = {}

NDR64Syntax = ('71710533-BEBA-4937-8319-B5DBEF9CCC36', '1.0')

MSRPC_UUID_BROWSER  = uuidtup_to_bin(('6BFFD098-A112-3610-9833-012892020162','0.0'))
MSRPC_UUID_SPOOLSS  = uuidtup_to_bin(('12345678-1234-ABCD-EF00-0123456789AB','1.0'))
MSRPC_UUID_NETLOGON = uuidtup_to_bin(('12345678-1234-ABCD-EF00-01234567CFFB','1.0'))
MSRPC_UUID_LSARPC   = uuidtup_to_bin(('12345778-1234-ABCD-EF00-0123456789AB','0.0'))
MSRPC_UUID_SAMR     = uuidtup_to_bin(('12345778-1234-ABCD-EF00-0123456789AC','1.0'))

pipes = {
	'browser'  : MSRPC_UUID_BROWSER,
	'spoolss'  : MSRPC_UUID_SPOOLSS,
	'netlogon' : MSRPC_UUID_NETLOGON,
	'lsarpc'   : MSRPC_UUID_LSARPC,
	'samr'     : MSRPC_UUID_SAMR,
}

def get_targets(targets):
    # parses an input of targets to get a list of all possible ips
    target_list = []

    try:
        with open(targets, 'r') as file:
            contents = file.readlines()
            for i in (contents):
                target = i.rstrip()
                target_list.append(target)
            return target_list
    except Exception as e:
        try:
            if "/" in targets:
                try:
                    subnet = IPNetwork(targets)
                except Exception as e:
                    logger.red('failed to parse:')
                    logger.red(str(e))
                    quit()

                for i in subnet:
                    tmp_str = str(i)
                    last_octet = str(tmp_str.split('.')[3])
                    if last_octet == '0' or last_octet == '255':
                        pass
                    else:
                        target_list.append(str(i))
                return target_list
            elif "," in targets:
                ips=targets.split(',')
                for ip in ips:
                    target_list.append(ip)
                return target_list

            else:
                target_list.append(targets)
                return target_list
        except Exception as e:
            logger.red('Failed to parse targets:')
            logger.red(str(e))
            quit()

def run(target):
	try:
		try:
			logger.verbose('Attempting to connect to %s' % logger.BLUE(target))
			conn = MYSMB(target, timeout=5)
			logger.verbose('Successfully connected to %s' % logger.BLUE(target))
		except Exception as e:
			logger.red('Failed to connect to [{}]'.format(logger.RED(target)))
			logger.verbose('Got error whilst connecting: %s' % logger.BLUE(str(e)))
			return False
		try:
			# login(self, user, password, domain='', lmhash='', nthash='', ntlm_fallback=True, maxBufferSize=None)
			# can add passthehash at some point
			logger.verbose('Attempting to authenticate to %s' % logger.BLUE(target))
			conn.login(username, password,domain)
			logger.verbose('Successfully authenticated to %s' % logger.BLUE(target))
		except Exception as e:
			logger.red('Failed to authenticate to [{}]'.format(logger.RED(target)))
			return False
		try:
			logger.verbose('Attempting to get OS for %s' % logger.BLUE(target))
			OS = conn.get_server_os()
			logger.verbose('Got Operting System: %s' % logger.BLUE(OS))
		except Exception as e:
			logger.verbose('Got error whilst getting Operting System: %s' % logger.BLUE(str(e)))
			logger.red('Failed to obtain operating system')

		try:
			tree_connect_andx = '\\\\' + target + '\\' + 'IPC$'
			logger.verbose('Attempting to connect to %s' % logger.BLUE(tree_connect_andx))
			tid = conn.tree_connect_andx(tree_connect_andx)
			conn.set_default_tid(tid)
			logger.verbose('Successfully connected to %s' % logger.BLUE(tree_connect_andx))

		except Exception as e:
			logger.verbose('Got error whilst connecting to %s: %s' % (tree_connect_andx,logger.BLUE(str(e))))
			return False

		# test if target is vulnerable
		logger.verbose('Testing if %s is vulnerable...' % logger.BLUE(target))
		try:
			TRANS_PEEK_NMPIPE = 0x23
			recvPkt = conn.send_trans(pack('<H', TRANS_PEEK_NMPIPE), maxParameterCount=0xffff, maxDataCount=0x800)
			status = recvPkt.getNTStatus()
			if status == 0xC0000205:  # STATUS_INSUFF_SERVER_RESOURCES
				logger.green('[%s] VULNERABLE' % logger.GREEN(target))
				vulnerable[target]=[]
			else:
				logger.red('[%s] PATCHED' % logger.RED(target))
		except Exception as e:
			logger.verbose('Got error whilst checking vulnerability status %s' % logger.BLUE(str(e)))
			return Falses

		pipes_found = []

		if target in vulnerable:
			logger.verbose('Checking pipes on %s' % logger.BLUE(target))
			for pipe_name, pipe_uuid in pipes.items():
				try:
					dce = conn.get_dce_rpc(pipe_name)
					dce.connect()
					try:
						dce.bind(pipe_uuid, transfer_syntax=NDR64Syntax)
						try:
							pipes_found.append(pipe_name)
						except Exception as e:
							logger.verbose('Got error whilst appending pipe to list %s' % logger.BLUE(str(e)))
							pass
					except DCERPCException as e:
						logger.verbose('Got error whilst binding to rpc: %s' % logger.BLUE(str(e)))
						if 'transfer_syntaxes_not_supported' in str(e):
							try:
								pipes_found.append(pipe_name)
							except Exception as e:
								logger.verbose('Got error whilst appending pipe to list %s (transfer_syntaxes_not_supported)' % logger.BLUE(str(e)))
								pass
						else:
							try:
								pipes_found.append(pipe_name)
							except Exception as e:
								logger.verbose('Got error whilst appending pipe to list %s !(transfer_syntaxes_not_supported)' % logger.BLUE(str(e)))
								pass
					except Exception as e:
						logger.verbose('Got error whilst binding to rpc: %s' % logger.BLUE(str(e)))
						pass
					finally:
						dce.disconnect()
					vulnerable[target]=pipes_found
				except smb.SessionError as e:
					logger.verbose('Got SMB Session error whilst connecting %s' % logger.BLUE(str(e)))
					continue
				except smbconnection.SessionError as e:
					logger.verbose('Got SMB Session error whilst connecting %s' % logger.BLUE(str(e)))
					continue
				except Exception as e:
					logger.verbose('Got SMB Session error whilst connecting %s' % logger.BLUE(str(e)))
					continue
		try:
			conn.disconnect_tree(tid)
			conn.logoff()
			conn.get_socket().close()
		except Exception as e:
			logger.verbose('Got error whilst disconnecting from rpc %s' % logger.BLUE(str(e)))
			pass
	except KeyboardInterrupt:
		logger.red('Keyboard interrupt received..')
		quit()

def do_scan(targets):
	for target in targets:
		run(target)

banner.show('checker')
t=args.targets
targets=get_targets(t)

if len(targets) == 1:
	logger.verbose_switch = True

do_scan(targets)

print('')
if len(vulnerable) == 0:
	print(logger.RED('No vulnerable hosts found'))
else:
	print(logger.BLUE('Results:'))
	logger.dump(vulnerable)
