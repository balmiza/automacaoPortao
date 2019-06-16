!/usr/bin/env python

import time, datetime
import RPi.GPIO as GPIO
import telepot
from telepot.loop import MessageLoop

# variaveis globais
relePortao = 18
abertoPortao = 23
ultimoAcionamento = "Portao ainda nao foi acionado"
#fechadoPortao = 24

# configurando IOs
now = datetime.datetime.now()
GPIO.setmode(GPIO.BCM)                                          # set tipo de GPIO
GPIO.setwarnings(False)
GPIO.setup(relePortao, GPIO.OUT)                                # gpio 18 como saida para rele do portao
GPIO.output(relePortao, 0)                                      # inicia o tele no estado 0 (desligado)
GPIO.setup(abertoPortao, GPIO.IN)                               # gpio 23 como entrada
GPIO.setup(abertoPortao, GPIO.IN, pull_up_down=GPIO.PUD_UP)     # gpio 23 pull up
#GPIO.setup(fechadoPortao, GPIO.IN)                             # gpio 24 como entrada
#GPIO.setup(fechadoPortao, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # gpio 24 pull up

def pulsoPortao():
        GPIO.output(relePortao, 1)
        time.sleep(1)
        GPIO.output(relePortao, 0)

def action(msg):
        global ultimoAcionamento
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
                ultimoAcionamento = datetime.datetime.now()

        if 'Fechar' in command:
                message = "Portao fechado "
                if 'portao' in command:
                        message = message + "com sucesso"
                        pulsoPortao()
                        #GPIO.output(relePortao, 0)
                        telegram_bot.sendMessage (chat_id, message)
                ultimoAcionamento = datetime.datetime.now()

        if 'Estado' in command:
                if(GPIO.input(abertoPortao) == 1):
                        message = "O portao esta aberto"
                elif(GPIO.input(abertoPortao) == 0):
                        message = "O portao esta fechado"
                else:
                        message = "Nem aberto e nem fechado"
                telegram_bot.sendMessage (chat_id, message)

        if 'Relatorio' in command:
                telegram_bot.sendMessage (chat_id, "Ultimo acionamento: " + str(ultimoAcionamento))

        if 'Ajuda' in command:
                telegram_bot.sendMessage (chat_id, "Abrir portao")
                telegram_bot.sendMessage (chat_id, "Fechar portao")
                telegram_bot.sendMessage (chat_id, "Estado")
                telegram_bot.sendMessage (chat_id, "Relatorio")
                telegram_bot.sendMessage (chat_id, "Ajuda")

telegram_bot = telepot.Bot('812788093:AAExMbZKwLDp_AHbwlaf7CVn6cWo-ci_tnc')
#print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print 'Up and Running....'

while 1:
        time.sleep(10)

