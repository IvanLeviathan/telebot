class logger:
    def log(msg):
        import os.path as path
        import sys
        from datetime import datetime

        d_now = datetime.now()

        logFileName = sys.path[0] + "\logs\{0}-{1}-{2}_log.log".format(d_now.year, d_now.month, d_now.day)

        if (path.isfile(logFileName)):
            logFile = open(logFileName, "a")
        else:
            logFile = open(logFileName, "w")
		try:
			logFile.write("{0}-{1}-{2} {3}:{4}:{5} \n".format(d_now.year, d_now.month, d_now.day, d_now.hour, d_now.minute,d_now.second) + str(msg) + "\n\n")
	        logFile.close()
		except Exception as e:


    def consoleLog(message, answer):
        print("\n=========")
        from datetime import datetime
        print(datetime.now())
        print("Сообщение от {0} {1}, id = {2}\nТекст сообщения - {3}".format(message.from_user.first_name,message.from_user.last_name,str(message.from_user.id), message.text))
        if(type(answer) is dict and 'text' in answer):
            print("Текст ответа - " + answer['text'])
        else:
            print("Текст ответа - " + answer)
