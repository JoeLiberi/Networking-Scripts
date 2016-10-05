#!/usr/local/bin/python3

import paramiko, time, os, sys


class ConnectToASA():

	def __init__(self, ip, username, password, cmd):
		self.ip = ip
		self.username = username
		self.password = password
		self.cmd = cmd

	def ConnectAndSendASA(self):

		ssh=paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		print("Opening connection please wait.....\n")
		ssh.connect(self.ip, username=self.username, password=self.password,look_for_keys=False, allow_agent=False)

		remote_conn = ssh.invoke_shell()
		send_enable(remote_conn, password)
		self.output = send_command(remote_conn, sys.argv[1])

		return remote_conn

	def PrintOutput(self):

		print(self.output.decode('ascii'))

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