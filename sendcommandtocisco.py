#!/usr/local/bin/python3


import argparse, re

ipaddress_regex = re.compile(r'(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)')


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument("-a", "--asa", help="send command to ASA device", type=str)
	parser.add_argument("-i", "--ios", help="send command to IOS device", type=str)
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


