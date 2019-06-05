import time, datetime
import RPi.GPIO as GPIO
import telepot
from telepot.loop import MessageLoop

relePortao = 18
now = datetime.datetime.now()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(relePortao, GPIO.OUT)
GPIO.output(relePortao, 0) #Off initially

def pulsoPortao():
        GPIO.output(relePortao, 1)
        time.sleep(1)
        GPIO.output(relePortao, 0)

def action(msg):
        chat_id = msg['chat']['id']
        command = msg['text']
        print 'Received: %s' % command

        if 'Abrir' in command:
                message = "Portao aberto "
                if 'portao' in command:
                        message = message + "com sucesso"
                        pulsoPortao()
                        #GPIO.output(relePortao, 1)
                        telegram_bot.sendMessage (chat_id, message)

        if 'Fechar' in command:
                message = "Portao fechado "
                if 'portao' in command:
                        message = message + "com sucesso"
                        pulsoPortao()
                        #GPIO.output(relePortao, 0)
                        telegram_bot.sendMessage (chat_id, message)

telegram_bot = telepot.Bot('812788093:AAExMbZKwLDp_AHbwlaf7CVn6cWo-ci_tnc')
print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print 'Up and Running....'

while 1:
        time.sleep(10)
