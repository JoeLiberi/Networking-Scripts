#!/usr/local/bin/python3

import paramiko, time, os, sys, re, socket


class ConnectToASA():

	def __init__(self, ip, username, password, enablepasswd, cmd):
		self.ip = ip
		self.username = username
		self.password = password
		self.enablepasswd = enablepasswd
		self.cmd = cmd
		self.tport = 23

		if self.enablepasswd is None:
			self.enablepasswd = self.password

	def ConnectASA(self):

		self.ssh=paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		print("Opening connection to {ip} please wait.....\n".format(ip=self.ip))
		self.ssh.connect(self.ip, username=self.username, password=self.password,look_for_keys=False, allow_agent=False)

		self.remote_conn = self.ssh.invoke_shell()
		self.remote_conn.send_ready()	
		send_enable(self.remote_conn, self.enablepasswd)

		# return self.remote_conn

	def SendASA(self):
		self.remote_conn.send_ready()
		self.output = send_command(self.remote_conn, self.cmd)

	def PrintOutput(self):

		print(self.output.decode('ascii'))

	def CheckOS(self):
		self.remote_conn.send_ready()

		# Turn off paging
		disable_paging(self.remote_conn)

		self.output = send_command(self.remote_conn, "sh ver")
		asa_regex = re.compile(r'(Adaptive Security Appliance)')
		self.output = self.output.decode('ascii')

		if asa_regex.search(self.output):
			return True
		else:
			return False

def send_command(shell, cmd):

	if type(cmd) is list:
		for c in cmd:
			print("Executing command: " + c)
			shell.send(c + '\n')
			# stdin, stdout, stderr = shell.exec_command(cmd + '\n')
			time.sleep(1)
			output = shell.recv(10000)
	else:
		print("Executing command: " + cmd)
		shell.send(cmd + '\n')
		# stdin, stdout, stderr = shell.exec_command(cmd + '\n')
		time.sleep(1)
		output = shell.recv(10000)
	# output = stdout.read()

	return output

def send_enable(shell, password):
	print("Sending enable.....\n")
	shell.send('\n')
	shell.send('enable\n')
	shell.send(password + '\n')
	time.sleep(1)

def disable_paging(remote_conn):
	'''Disable paging on a ASA firewall'''

	remote_conn.send("config t\n")
	time.sleep(1)
	remote_conn.send("pager 0\n")
	time.sleep(1)
	remote_conn.send("end\n")

	# Clear the buffer on the screen
	output = remote_conn.recv(1000)

	return output