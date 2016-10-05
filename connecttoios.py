#!/usr/local/bin/python3

import paramiko, time, os, re

class ConnectToIOS():

	def __init__(self, ip, username, password, cmd):
		self.ip = ip
		self.username = username
		self.password = password
		self.cmd = cmd

	def ConnectIOS(self):

		self.ssh=paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		print("Opening connection please wait.....\n")
		self.ssh.connect(self.ip, username=self.username, password=self.password,look_for_keys=False, allow_agent=False)

		self.remote_conn = self.ssh.invoke_shell()
		self.remote_conn.send_ready()	
		send_enable(self.remote_conn, self.password)

	def SendIOS(self):
		self.remote_conn.send_ready()
		# Turn off paging
		disable_paging(self.remote_conn)
		self.output = send_command(self.remote_conn, self.cmd)

	def PrintOutput(self):

		print(self.output.decode('ascii'))

	def CheckOS(self):
		self.remote_conn.send_ready()
		self.output = send_command(self.remote_conn, "sh ver")
		ios_regex = re.compile(r'(Cisco IOS Software)')
		self.output = self.output.decode('ascii')

		if ios_regex.match(self.output):
			return True
		else:
			return False

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

def disable_paging(remote_conn):
	'''Disable paging on a Cisco router'''

	remote_conn.send("terminal length 0\n")
	time.sleep(1)

	# Clear the buffer on the screen
	output = remote_conn.recv(1000)

	return output