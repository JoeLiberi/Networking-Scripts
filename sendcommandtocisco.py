#!/usr/local/bin/python3


import argparse, re, os, sys
from connecttoasa import ConnectToASA
from connecttoios import ConnectToIOS

ipaddress_regex = re.compile(r'(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)')


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("-a", "--asa", help="send command to ASA device", action='store_true')
	parser.add_argument("-i", "--ios", help="send command to IOS device", action='store_true')
	parser.add_argument("-ip", "--ipaddress", type=str)
	parser.add_argument("-p", "--password", type=str)
	parser.add_argument("-ep", "--enablepasswd", type=str)
	parser.add_argument("-u", "--username", type=str)
	parser.add_argument("-c", "--command", type=str)
	parser.add_argument("-f", "--file", type=str)
	parser.add_argument("-cf", "--command_file", type=str)


	args = parser.parse_args()

	# Input Checks
	if args.file is None:
		if args.ipaddress is None:
			print(parser.print_help())
			sys.exit("Please enter a IP address")
		elif type(args.ipaddress) is not str:
			print(parser.print_help())
			sys.exit("Please enter a valid IP address")
		elif ipaddress_regex.match(args.ipaddress) is None:
			print(parser.print_help())
			sys.exit("Please enter a valid IP address")
	else:
		with open(args.file, mode='r') as infile:
			for line in infile:
				if ipaddress_regex.match(line) is None:
					print(parser.print_help())
					sys.exit("There is a non IP address in your file. Please reveiw and re-run")

	if args.password is None:
		print(parser.print_help())
		sys.exit("Please enter a Password")
	elif args.username is None:
		print(parser.print_help())
		sys.exit("Please enter a Username")
	elif args.command is None and args.command_file is None:
		print(parser.print_help())
		sys.exit("Please enter a command to run")

	'''
	Read command file into a list
	'''
	cmd_list = []
	if args.command_file:
		with open(args.command_file, mode='r') as cmdfile:
			cmd_list = cmdfile.readlines()

	
	if args.asa:
		if args.file:
			with open(args.file, mode='r') as infile:
				for line in infile:
					if not cmd_list:
						asa_conn = ConnectToASA(line.rstrip(), args.username, args.password, args.enablepasswd, args.command)
					else:
						asa_conn = ConnectToASA(line.rstrip(), args.username, args.password, args.enablepasswd, cmd_list)
				
					try:
						asa_conn.ConnectASA()
					except Exception as e:
						print("Ran into an error on {ip}, moving on".format(ip=line.rstrip()))
						continue

					if asa_conn.CheckOS():
						asa_conn.SendASA()
						asa_conn.PrintOutput()
					else:
						print(parser.print_help())
						sys.exit("You are using the wrong arg, this is for ASA devices, use -i")
		else:
			asa_conn = ConnectToASA(args.ipaddress, args.username, args.password, args.enablepasswd, args.command)
			try:
				asa_conn.ConnectASA()
			except Exception as e:
				sys.exit("Shit Broke")

			if asa_conn.CheckOS():
				asa_conn.SendASA()
				asa_conn.PrintOutput()
			else:
				print(parser.print_help())
				sys.exit("You are using the wrong arg, this is for ASA devices, use -i")


	elif args.ios:
		if args.file:
			with open(args.file, mode='r') as infile:
				for line in infile:
					if not cmd_list:
						ios_conn = ConnectToIOS(line.rstrip(), args.username, args.password, args.enablepasswd, args.command)
					else:
						ios_conn = ConnectToASA(line.rstrip(), args.username, args.password, args.enablepasswd, cmd_list)

					try:
						ios_conn.ConnectIOS()
					except Exception as e:
						print("Ran into an error on {ip}, moving on".format(ip=line.rstrip()))
						continue
					
					if ios_conn.CheckOS():
						ios_conn.SendIOS()
						ios_conn.PrintOutput()
					else:
						print(parser.print_help())
						sys.exit("You are using the wrong arg, this is for IOS devices, use -a")
		else:
			ios_conn = ConnectToIOS(args.ipaddress, args.username, args.password, args.enablepasswd, args.command)
			try:
				ios_conn.ConnectIOS()
			except Exception as e:
				print(e)
				sys.exit()
			
			if ios_conn.CheckOS():
				ios_conn.SendIOS()
				ios_conn.PrintOutput()
			else:
				print(parser.print_help())
				sys.exit("You are using the wrong arg, this is for IOS devices, use -a")

	else:
		print(parser.print_help())
		sys.exit("Select ASA or IOS...")


