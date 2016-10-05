#!/usr/local/bin/python3


import argparse, re
from connecttoasa import ConnectToASA
from connecttoios import ConnectToIOS

ipaddress_regex = re.compile(r'(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)')


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("-a", "--asa", help="send command to ASA device", action='store_true')
	parser.add_argument("-i", "--ios", help="send command to IOS device", action='store_true')
	parser.add_argument("-ip", "--ipaddress", type=str)
	parser.add_argument("-p", "--password", type=str)
	parser.add_argument("-u", "--username", type=str)
	parser.add_argument("-c", "--command", type=str)


	args = parser.parse_args()

	# Input Checks
	if args.ipaddress is None:
		print("Please enter a IP address")
		print(parser.print_help())
	elif type(args.ipaddress) is not str:
		print("Please enter a valid IP address")
		print(parser.print_help())
	elif ipaddress_regex.match(args.ipaddress) is None:
		print("Please enter a valid IP address")
		print(parser.print_help())
	
	if args.asa:
		asa_conn = ConnectToASA(args.ipaddress, args.username, args.password, args.command)
		asa_conn.ConnectASA()

		if asa_conn.CheckOS():
			asa_conn.SendASA()
			asa_conn.PrintOutput()
		else:
			print("You are using the wrong arg, this is for ASA devices, use -i")
			print(parser.print_help())

	elif args.ios:
		ios_conn = ConnectToIOS(args.ipaddress, args.username, args.password, args.command)
		ios_conn.ConnectIOS()
		check = ios_conn.CheckOS()
		print(ios_conn.PrintOutput())
		
		if check:
			ios_conn.SendIOS()
			ios_conn.PrintOutput()
		else:
			print("You are using the wrong arg, this is for IOS devices, use -a")
			print(parser.print_help())

	else:
		print("Select ASA or IOS...")
		print(parser.print_help())


