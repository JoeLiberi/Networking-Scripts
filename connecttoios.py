#!/usr/local/bin/python3

import paramiko, time, os, re, socket, select

class ConnectToIOS():

	def __init__(self, ip, username, password, enablepasswd, cmd):
		self.ip = ip
		self.username = username
		self.password = password
		self.enablepasswd = enablepasswd
		self.cmd = cmd
		self.tport = 23


		if self.enablepasswd is None:
			self.enablepasswd = self.password

	def ConnectIOS(self):

		self.ssh=paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		print("Opening connection to {ip} please wait.....\n".format(ip=self.ip))
		self.ssh.connect(self.ip, username=self.username, password=self.password,look_for_keys=False, allow_agent=False)

		self.remote_conn = self.ssh.invoke_shell()
		self.remote_conn.send_ready()	
		send_enable(self.remote_conn, self.enablepasswd)

	def ConnectTelnetIOS(self):

		self.remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.remote_conn.settimeout(5)

		try:
			self.remote_conn.connect((self.ip, self.tport))
		except Exception as e:
			print(e)

		send_command(self.remote_conn, self.username)
		send_command(self.remote_conn, self.password)
		send_enable(self.remote_conn, self.enablepasswd)

		# self.output = send_command(self.remote_conn, self.cmd)

	def SendIOS(self, args):
		if not args.telnet:
			self.remote_conn.send_ready()

		# Turn off paging
		disable_paging(self.remote_conn)
		self.output = send_command(self.remote_conn, self.cmd)

	def PrintOutput(self):

		print(self.output.decode('ascii'))

	def CheckOS(self):
		self.remote_conn.send_ready()
		# Turn off paging
		disable_paging(self.remote_conn)

		self.output = send_command(self.remote_conn, "sh ver")
		ios_regex = re.compile('Cisco IOS Software')
		self.output = self.output.decode('ascii')

		if ios_regex.search(self.output):
			return True
		else:
			return False

def send_command(shell, cmd):

	if type(cmd) is list:
		for c in cmd:
			print("Executing command: " + c)
			c = bytes(c, "utf-8")
			shell.send(c + "\n".encode('ascii'))
			# stdin, stdout, stderr = shell.exec_command(cmd + '\n')
			time.sleep(1)
			output = shell.recv(10000)

			print(output.decode('ascii'))
	else:
		print("Executing command: " + cmd)
		cmd = bytes(cmd, "utf-8")
		shell.send(cmd + "\n".encode('ascii'))
		# stdin, stdout, stderr = shell.exec_command(cmd + '\n')
		time.sleep(1)
		output = shell.recv(10000)
	# output = stdout.read()

	return output

def send_enable(shell, password):
	print("Sending enable.....\n")
	shell.send('\n'.encode('ascii'))
	shell.send('enable\n'.encode('ascii'))
	password = bytes(password, "utf-8")
	shell.send(password + '\n'.encode('ascii'))
	time.sleep(2)

def disable_paging(remote_conn):
	'''Disable paging on a Cisco router'''

	remote_conn.send("terminal length 0\n".encode('ascii'))
	time.sleep(1)

	# Clear the buffer on the screen
	output = remote_conn.recv(1000)

	return output