#!/usr/bin/env python

import time, datetime
import RPi.GPIO as GPIO
import telepot
from telepot.loop import MessageLoop

# variaveis globais
relePortao = 18
abertoPortao = 23
ultimoAcionamento = "Portao ainda nao foi acionado"
ultimo_usuario = 1
ativado = 0     # 0 - Ativado     1 - Desativado
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
        global ultimo_usuario
        global ultimoAcionamento
        global ativado
        chat_id = msg['chat']['id']
        ultimo_usuario = chat_id
        #print chat_id
        command = msg['text']
        print 'Received: %s' % command

        if ((('Abrir' in command) or ('abrir' in command)) and (len(command) > 6)):
                #print 'Entrou no if'
                try:
                        lista_command = command.split()
                        tempo = float(lista_command[1])
                        if (tempo < 11):
                                print "Favor inserir tempo maior que 10 s"
                                telegram_bot.sendMessage (chat_id, "Favor inserir tempo maior que 10 s")
                        else:
                                print "Abrindo.."
                                telegram_bot.sendMessage (chat_id, "Abrindo..")
                                pulsoPortao()
                                time.sleep(tempo)
                                print "Fechando.."
                                telegram_bot.sendMessage (chat_id, "Fechando..")
                                pulsoPortao()
                                time.sleep(5)
                                if (checkPortao() == "fechado"):
                                        print "Portao fechado com sucesso."
                                        telegram_bot.sendMessage (chat_id, "Portao fechado com sucesso.")
                                        ultimoAcionamento = datetime.datetime.now()
                                else:
                                        print "Houve um erro ao fechar o portao, favor checar se esta mesmo fechado."
                                        telegram_bot.sendMessage (chat_id, "Houve um erro ao fechar o portao, favor checar se esta mesmo fechado.")

                except:
                        print "Desculpe, nao entendi!"
                        telegram_bot.sendMessage (chat_id, "Desculpe, nao entendi!")

        elif ((command == 'Abrir') or (command == 'abrir')):
                message = "Portao aberto "
                #if 'portao' in command:
                message = message + "com sucesso."
                if (checkPortao() == "aberto"):
                        message = "Portao ja esta aberto."
                else:
                        pulsoPortao()
                        ultimoAcionamento = datetime.datetime.now()
                telegram_bot.sendMessage (chat_id, message)

        elif ((command == 'Fechar') or (command == 'fechar')):
                message = "Portao fechado "
                #if 'portao' in command:
                message = message + "com sucesso."
                if (checkPortao() == "fechado"):
                        message = "Portao ja esta fechado."
                else:
                        pulsoPortao()
                        ultimoAcionamento = datetime.datetime.now()
                telegram_bot.sendMessage (chat_id, message)

        elif ((command == 'Portao') or (command == 'portao')):
                if(GPIO.input(abertoPortao) == 1):
                        message = "O portao esta aberto."
                elif(GPIO.input(abertoPortao) == 0):
                        message = "O portao esta fechado."
                else:
                        message = "Nem aberto e nem fechado."
                telegram_bot.sendMessage (chat_id, message)

        elif ((command == 'Relatorio') or (command == 'relatorio')):
                telegram_bot.sendMessage (chat_id, "Ultimo acionamento: " + str(ultimoAcionamento))

        elif (('Ajuda' in command) or ('ajuda' in command)):
                telegram_bot.sendMessage (chat_id, "Abrir [tempo em segundos]")
                telegram_bot.sendMessage (chat_id, "Abrir | abrir")
                telegram_bot.sendMessage (chat_id, "Fechar | fechar")
                telegram_bot.sendMessage (chat_id, "Portao | portao")
                telegram_bot.sendMessage (chat_id, "Relatorio | relatorio")
                telegram_bot.sendMessage (chat_id, "Ajuda | ajuda")
                telegram_bot.sendMessage (chat_id, "Duvidas ou problemas, entrar em contato com Felipe pelo telefone (11)965370735 ou via email: balmiza.felipe@gmail.com")

        elif ((command == "Ativar") or (command == "ativar")):
                if (ativado == 0):
                        telegram_bot.sendMessage (chat_id, "Ja esta ativado")
                else:
                        telegram_bot.sendMessage (chat_id, "Sistema ativado")
                        ativado = 0

        elif ((command == "Desativar") or (command == "desativar")):
                if (ativado == 1):
                        telegram_bot.sendMessage (chat_id, "Ja esta desativado")
                else:
                        telegram_bot.sendMessage (chat_id, "Sistema desativado")
                        ativado = 1
        else:
                print "Desculpe, nao entendi!!!"
                telegram_bot.sendMessage (chat_id, "Desculpe, nao entendi!!!")

telegram_bot = telepot.Bot('812788093:AAExMbZKwLDp_AHbwlaf7CVn6cWo-ci_tnc')
#print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print 'Up and Running....'
chat_id_lista = [892724002, 873945561, 875826898]
tamanho_lista = len(chat_id_lista)
portao_inicial = checkPortao()

while 1:
        time.sleep(1)
        #print ultimo_usuario
        portao = checkPortao()
        if ((portao != portao_inicial) and (ativado == 0)):
                if (portao == "aberto"):
                        for i in range(tamanho_lista):
                                if (chat_id_lista[i] != ultimo_usuario):
                                        telegram_bot.sendMessage (chat_id_lista[i], "Portao foi aberto")
                                portao_inicial = portao
                elif (portao == "fechado"):
                        for i in range(tamanho_lista):
                                if (chat_id_lista[i] != ultimo_usuario):
                                        telegram_bot.sendMessage (chat_id_lista[i], "Portao foi fechado")
