#!/usr/local/bin/python3

import paramiko, time, os, sys

def send_command(shell, cmd):

	print("Executing command: " + cmd)
	shell.send(cmd + '\n')
	time.sleep(1)
	output = shell.recv(5000)

	return output

def send_enable(shell, password):
	print("Sending enable.....\n")
	shell.send('\n')
	shell.send('enable\n')
	shell.send(password + '\n')
	time.sleep(1)

if __name__ == '__main__':

	ip = '172.16.254.2'
	username = 'admin'
	password = '*******'
	ssh=paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	print("Opening connection please wait.....\n")
	ssh.connect(ip, username=username, password=password,look_for_keys=False, allow_agent=False)

	remote_conn = ssh.invoke_shell()

	send_enable(remote_conn, password)

	output = send_command(remote_conn, sys.argv[1])
	# output = remote_conn.recv(5000)

	print(output.decode('ascii'))
	# timeout = 3.0

	# endtime = time.time() + timeout

	# while not stdout.channel.eof_received:
	# 	time.sleep(1)
	# 	if time.time() > endtime:
	# 		stdout.channel.close()
	# 		break

	# print(stdout.read())