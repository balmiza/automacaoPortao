#!/usr/bin/env python

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

def checkPortao():
        if (GPIO.input(abertoPortao) == 1):
                return "aberto"                 # portao aberto
        elif (GPIO.input(abertoPortao) == 0):
                return "fechado"                # portao fechado

def action(msg):
        global ultimoAcionamento
        chat_id = msg['chat']['id']
        command = msg['text']
        print 'Received: %s' % command

        if (('Abrir' in command) or ('abrir' in command)):
                message = "Portao aberto "
                #if 'portao' in command:
                message = message + "com sucesso"
                if (checkPortao() == "aberto"):
                        message = "Portao ja esta aberto."
                else:
                        pulsoPortao()
                        ultimoAcionamento = datetime.datetime.now()
                telegram_bot.sendMessage (chat_id, message)

        if (('Fechar' in command) or ('fechar' in command)):
                message = "Portao fechado "
                #if 'portao' in command:
                message = message + "com sucesso"
                if (checkPortao() == "fechado"):
                        message = "Portao ja esta fechado."
                else:
                        pulsoPortao()
                        ultimoAcionamento = datetime.datetime.now()
                telegram_bot.sendMessage (chat_id, message)

        if (('Portao' in command) or ('portao' in command)):
                if(GPIO.input(abertoPortao) == 1):
                        message = "O portao esta aberto"
                elif(GPIO.input(abertoPortao) == 0):
                        message = "O portao esta fechado"
                else:
                        message = "Nem aberto e nem fechado"
                telegram_bot.sendMessage (chat_id, message)

        if (('Relatorio' in command) or ('relatorio' in command)):
                telegram_bot.sendMessage (chat_id, "Ultimo acionamento: " + str(ultimoAcionamento))

        if (('Ajuda' in command) or ('ajuda' in command)):
                telegram_bot.sendMessage (chat_id, "Abrir | abrir")
                telegram_bot.sendMessage (chat_id, "Fechar | fechar")
                telegram_bot.sendMessage (chat_id, "Portao | portao")
                telegram_bot.sendMessage (chat_id, "Relatorio | relatorio")
                telegram_bot.sendMessage (chat_id, "Ajuda | ajuda")
                telegram_bot.sendMessage (chat_id, "Duvidas ou problemas, entrar em contato com Felipe pelo telefone (11)965370735 ou via email: balmiza.felipe@gmail.com")

telegram_bot = telepot.Bot('812788093:AAExMbZKwLDp_AHbwlaf7CVn6cWo-ci_tnc')
#print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print 'Up and Running....'

while 1:
        time.sleep(10)
