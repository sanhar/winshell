import socket, os

def downloadFile(c, filename, red, default):
    if "/" in filename:
        filename = filename.split("/")
        for i in filename:
            pass
        filename = i
    c.send(filename)
    data = c.recv(1024)
    if data[:6] == "EXISTS":
        filesize = long(data[6:])
	if filesize == 0:
		print "{}[-]{} The file contains 0 Byte :/".format(red, default)
		c.send("ERR")
		c.recv(1024)
		return "F"
        c.send("OK")
        with open("{}".format(filename), "wb") as f:
        	data = c.recv(8096)
        	totalRecv = len(data)
        	f.write(data)
        	while totalRecv < filesize:
        	        data = c.recv(4096)
        	        totalRecv += len(data)
        	        f.write(data)
		return "T"
    else:
        print "{}[-]{} File does not Exists!".format(red, default)
	return "F"

def uploadFile(c, filename, red, default, path="None"):
	if os.path.isfile(filename):
		if "/" in filename:
			filename = filename.split("/")
			for i in filename:
				pass
			filename = i
        	c.send(filename)
		c.send(path)
		if c.recv(1024) == "ERR":
			print "{}[-]{} '{}' doesn't exists".format(red, default, path)
			return "F"
	    	filesize = os.path.getsize(filename)
	    	if filesize == 0:
			print "{}[-]{} The file contains 0 Byte :/".format(red, default)
			c.send("ERR")
			c.recv(1024)
			return "F"

		fileS = "EXISTS {}".format(filesize)
		c.send(fileS)
		userResponse = c.recv(1024)
		if userResponse[:2] == "OK":
			with open(filename, "rb") as f:
		    		bytesToSend = f.read(1024)
		        	c.send(bytesToSend)
		        	while bytesToSend != "":
		        		bytesToSend = f.read(4096)
		        		c.send(bytesToSend)
		        	return "T"
	else:
		c.send("ERR")
		c.recv(1024)
		print "{}[-]{} File does not Exists!".format(red, default)
		return "F"
