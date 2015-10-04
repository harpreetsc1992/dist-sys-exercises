#******************************************************************************##  CS 6421 - Conversion server b to in [HW4]#  Execution:    python <programName.py> <Port: Conversion server> <IP:Discovery Server> <Port: Discovery server>##  Initial: Wenhui (Thank you!)##******************************************************************************## Students: Phani, Teo, Harpreet, Ashwini, Mruganka, Changle#import socketimport sys## Function to process requestsdef process(conn):    # read userInput from client    conn.send("Welcome, you are connected to b-in server.\n")    userInput = conn.recv(BUFFER_SIZE)    if not userInput:        print "Error reading message"        sys.exit(1)        print ("Received message: ", userInput)    reply = func(userInput)def func(userInput):    print "In func"    if not userInput:        print "Error reading message"        return    mysplit = userInput.split(" ")#split the input string    try:						#checking for numerals        countTokens = 0        fromConv = ""        toConv = ""        inputVal = ""        # TODO: add convertion function here, reply = func(userInput)        reqTokens = userInput.split(" ")        for item in reqTokens:            if countTokens == 0: #first token, from conv.                fromConv = item                countTokens += 1            elif countTokens == 1: #second token, to conv.                toConv = item                countTokens += 1            elif countTokens == 2: #third token, input value.                inputVal = item.strip()                countTokens += 1            else: #more tokens? invalid input.                print "Invalid input", userInput                conn.close()                return            if countTokens != 3: #very few tokens? invalid input.            print "Invalid input", userInput            conn.close()            return        #convert value..        response = convert(fromConv, toConv, inputVal)        if response == "":            print "Failed to convert"            conn.close() #close connection.. no standard defined to return response in failure.            return                print inputVal, fromConv, "=", response, toConv        #send converted value to client and close client socket..        conn.send(response + str("\n"))        conn.close()    except ValueError:			#if not a numeral        print "No Number Entered, Closing this Connection"        conn.send("Enter a number")        conn.close()        return nulldef convert(fromConv, toConv, inpVal):    if fromConv == "b" and toConv == "in":        return str((float(inpVal) * 5.0))    elif fromConv == "in" and toConv == "b":        return str((float(inpVal) / 5.0))    else:        return str() #error..return empty string.class Register(object):    def __init__(self, discportnum, myport, myip,discip):        # Discov Server        # Phani:        # Discovery IP and PORT no, you've to read it from command line as well.        # Discovery IP is not same as your IP.        self.discov_ip = discip        self.discov_portnum = discportnum        self.myip =myip        self.myport = myport        self.unit1 = "b"        self.unit2 = "in"    #******************************************************************************    #   Register Request at Discov Server    #******************************************************************************    def register(self):        # send discov msg when turned on        try:            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            sock.connect((discip, self.discov_portnum))            # Phani:            # Request will be "ADD " + unit1 + space + unit2 + space + ip + portno            # i don't know if sys.argv[] can be used here.. no idea..            # You've to read IP address from command line and not through socket interface.            self.msg = "ADD "+self.unit1 + ' ' + self.unit2 + ' ' + self.myip + ' ' + str(self.myport)+"\n"            sock.send(self.msg)            # Phani: Read response!            print "registered"            disc_response= sock.recv(BUFFER_SIZE)            print disc_response            sock.close()        except KeyboardInterrupt:            sock.close()            sys.exit(1)        except IOError:            # Close the client connection socket            sock.close()            sys.exit(1)    #******************************************************************************    #   Unregister Request at Discov Server    #******************************************************************************    def unregister(self):        # send discov msg when turned off        try:            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            sock.connect((self.discov_ip, self.discov_portnum))            # Phani:            # REMOVE protocol: REMOVE SPACE IP SPACE PORT            # No unit1 and unit2. And read response.            self.msg = "REMOVE "+ self.myip + ' ' + str(self.myport)+"\n"            sock.send(self.msg)            print "unregisted"            disc_response= sock.recv(BUFFER_SIZE)            print disc_response            sock.close()        except KeyboardInterrupt:            sock.close()            sys.exit(1)        except IOError:            # Close the client connection socket            sock.close()            sys.exit(1)### Main code run when program is startedBUFFER_SIZE = 1024interface = ""# if input arguments are wrong, print out usageif len(sys.argv) != 4:    print >> sys.stderr, "usage: python <programName.py> <Port: Conversion server> <IP:Discovery Server> <Port: Discovery server>\n",format(sys.argv[0])    sys.exit(1)portnum = int(sys.argv[3])discip =sys.argv[2]myport = int(sys.argv[1])# create sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)s.bind((socket.gethostname(), myport))R = Register(portnum, myport, socket.gethostname(),discip)R.register()s.listen(5)print "Started server on ",myportwhile True:    try:        # accept connection and print out info of client        conn, addr = s.accept()        print 'Accepted connection from client', addr                try:            process(conn)        except Exception as errmsg:            print "Caught exception:", errmsg            R.unregister()            conn.close()            continue #don't need to terminate..if we failed to handle one client.    except Exception as errmsg: #if failed..        print "Caught exception:", errmsg        R.unregister()        s.close() #cleanup..        sys.exit(-1) #terminate..s.close()