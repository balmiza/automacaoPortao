#!/usr/bin/env python

import time, datetime
import RPi.GPIO as GPIO
import telepot
from telepot.loop import MessageLoop

# variaveis globais teste1
relePortao = 18
abertoPortao = 23
ultimoAcionamento = "Portao ainda nao foi acionado"
ultimo_usuario = 1
ativado = 0     # 0 - Ativado     1 - Desativado

# configurando IOs
now = datetime.datetime.now()
GPIO.setmode(GPIO.BCM)                                          # set tipo de GPIO
GPIO.setwarnings(False)
GPIO.setup(relePortao, GPIO.OUT)                                # gpio 18 como saida para rele do portao
GPIO.output(relePortao, 0)                                      # inicia o tele no estado 0 (desligado)
GPIO.setup(abertoPortao, GPIO.IN)                               # gpio 23 como entrada
GPIO.setup(abertoPortao, GPIO.IN, pull_up_down=GPIO.PUD_UP)     # gpio 23 pull up

def log(texto):
        try:
                file = open("/home/pi/Documents/email-server/log.txt","a")
                file.write(texto + "\n")
                file.close()
        except:
                print "Falha ao gravar log"

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
        usuario_lista = [892724002, 873945561, 875826898, 843302394]
        chat_id = msg['chat']['id']

        # Poderia ter usado a variavel chat_id, mas estava sem tempo para analisar o impacto
        # entao criei outra variavel e carreguei com o mesmo valor.
        usuario = msg['chat']['id']
        print usuario

        ultimo_usuario = "nada"
        command = msg['text']
        print 'Received: %s' % command
        texto = str(chat_id) + " Received: " + command + " " + str(datetime.datetime.now())
        log(texto)

        if (usuario in usuario_lista):
                if ((('Abrir' in command) or ('abrir' in command)) and (len(command) > 6)):
                        try:
                                ultimo_usuario = chat_id
                                lista_command = command.split()
                                tempo = float(lista_command[1])
                                if (tempo < 11):
                                        print "Favor inserir tempo maior que 10 s"
                                        telegram_bot.sendMessage (chat_id, "Favor inserir tempo maior que 10 s")
                                        texto = str(chat_id) + " Favor inserir tempo maior que 10 s " + str(datetime.datetime.now())
                                        log(texto)
                                else:
                                        print "Abrindo.."
                                        telegram_bot.sendMessage (chat_id, "Abrindo..")
                                        texto = str(chat_id) + " Abrindo.. " + str(datetime.datetime.now())
                                        log(texto)
                                        pulsoPortao()
                                        time.sleep(tempo)
                                        print "Fechando.."
                                        telegram_bot.sendMessage (chat_id, "Fechando..")
                                        texto = str(chat_id) + " Fechando.. " + str(datetime.datetime.now())
                                        log(texto)
                                        pulsoPortao()
                                        time.sleep(5)
                                        if (checkPortao() == "fechado"):
                                                print "Portao fechado com sucesso."
                                                telegram_bot.sendMessage (chat_id, "Portao fechado com sucesso.")
                                                ultimoAcionamento = datetime.datetime.now()
                                                texto = str(chat_id) + " Portao fechado com sucesso " + str(datetime.datetime.now())
                                                log(texto)
                                        else:
                                                print "Houve um erro ao fechar o portao, favor checar se esta mesmo fechado."
                                                telegram_bot.sendMessage (chat_id, "Houve um erro ao fechar o portao, favor checar se esta mesmo fechado.")
                                                texto = str(chat_id) + " Falha ao fechar o portao " + str(datetime.datetime.now())
                                                log(texto)
                        except:
                                print "Desculpe, nao entendi!"
                                telegram_bot.sendMessage (chat_id, "Desculpe, nao entendi!")
                                texto = str(chat_id) + " Comando invalido " + str(datetime.datetime.now())
                                log(texto)

                elif ((command == 'Abrir') or (command == 'abrir')):
                        ultimo_usuario = chat_id
                        message = "Portao aberto "
                        message = message + "com sucesso."
                        if (checkPortao() == "aberto"):
                                message = "Portao ja esta aberto."
                                texto = str(chat_id) + " Abrir - portao ja estava aberto " + str(datetime.datetime.now())
                                log(texto)
                        else:
                                pulsoPortao()
                                ultimoAcionamento = datetime.datetime.now()
                                texto = str(chat_id) + " Abrir - portao aberto com sucesso " + str(datetime.datetime.now())
                                log(texto)
                        telegram_bot.sendMessage (chat_id, message)

                elif ((command == 'Fechar') or (command == 'fechar')):
                        ultimo_usuario = chat_id
                        message = "Portao fechado "
                        message = message + "com sucesso."
                        if (checkPortao() == "fechado"):
                                message = "Portao ja esta fechado."
                                texto = str(chat_id) + " Fechar - portao ja estava fechado " + str(datetime.datetime.now())
                                log(texto)
                        else:
                                pulsoPortao()
                                ultimoAcionamento = datetime.datetime.now()
                                texto = str(chat_id) + " Fechar - portao fechado com sucesso " + str(datetime.datetime.now())
                                log(texto)
                        telegram_bot.sendMessage (chat_id, message)

                elif ((command == 'Portao') or (command == 'portao')):
                        if(GPIO.input(abertoPortao) == 1):
                                message = "O portao esta aberto."
                                texto = str(chat_id) + " Portao - portao esta aberto " + str(datetime.datetime.now())
                                log(texto)
                        elif(GPIO.input(abertoPortao) == 0):
                                message = "O portao esta fechado."
                                texto = str(chat_id) + " Portao - portao esta fechado " + str(datetime.datetime.now())
                                log(texto)
                        else:
                                message = "Nem aberto e nem fechado."
                                texto = str(chat_id) + " Portao - Nem aberto e nem fechado " + str(datetime.datetime.now())
                                log(texto)
                        telegram_bot.sendMessage (chat_id, message)

                elif ((command == 'Relatorio') or (command == 'relatorio')):
                        telegram_bot.sendMessage (chat_id, "Ultimo acionamento: " + str(ultimoAcionamento))
                        texto = str(chat_id) + " Relatorio " + str(datetime.datetime.now())
                        log(texto)

                elif (('Ajuda' in command) or ('ajuda' in command)):
                        telegram_bot.sendMessage (chat_id, "Abrir [tempo em segundos]")
                        telegram_bot.sendMessage (chat_id, "Abrir | abrir")
                        telegram_bot.sendMessage (chat_id, "Fechar | fechar")
                        telegram_bot.sendMessage (chat_id, "Portao | portao")
                        telegram_bot.sendMessage (chat_id, "Relatorio | relatorio")
                        telegram_bot.sendMessage (chat_id, "Ajuda | ajuda")
                        telegram_bot.sendMessage (chat_id, "Duvidas ou problemas, entrar em contato com Felipe pelo telefone (11)965370735 ou via email: balmiza.felipe@gmail.com")
                        texto = str(chat_id) + " Ajuda - enviado com sucesso " + str(datetime.datetime.now())
                        log(texto)

                elif ((command == "Ativar") or (command == "ativar")):
                        if (ativado == 0):
                                telegram_bot.sendMessage (chat_id, "Ja esta ativado")
                                texto = str(chat_id) + " Ativar - ja esta ativado " + str(datetime.datetime.now())
                                log(texto)
                        else:
                                telegram_bot.sendMessage (chat_id, "Sistema ativado")
                                ativado = 0
                                texto = str(chat_id) + " Ativar - sistema ativado com sucesso " + str(datetime.datetime.now())
                                log(texto)

                elif ((command == "Desativar") or (command == "desativar")):
                        if (ativado == 1):
                                telegram_bot.sendMessage (chat_id, "Ja esta desativado")
                                texto = str(chat_id) + " Desativar - ja esta desativado " + str(datetime.datetime.now())
                                log(texto)
                        else:
                                telegram_bot.sendMessage (chat_id, "Sistema desativado")
                                ativado = 1
                                texto = str(chat_id) + " Desativar - desativado com sucesso " + str(datetime.datetime.now())
                                log(texto)

                else:
                        print "Desculpe, nao entendi!!!"
                        telegram_bot.sendMessage (chat_id, "Desculpe, nao entendi!!!")

        else:
                telegram_bot.sendMessage (usuario_lista[0], "Estao tentando nos hackear")
                telegram_bot.sendMessage (usuario_lista[1], "Estao tentando nos hackear")
                telegram_bot.sendMessage (usuario_lista[2], "Estao tentando nos hackear")
                telegram_bot.sendMessage (usuario_lista[3], "Estao tentando nos hackear")

telegram_bot = telepot.Bot('812788093:AAExMbZKwLDp_AHbwlaf7CVn6cWo-ci_tnc')
#print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print 'Up and Running....'
chat_id_lista = [892724002, 873945561, 875826898, 843302394]
tamanho_lista = len(chat_id_lista)
portao_inicial = checkPortao()
while 1:
        try:
                # timer importante para evitar muitas leituras do sensor
                time.sleep(1)
                portao = checkPortao()
                if ((portao != portao_inicial) and (ativado == 0)):
                        if (portao == "aberto"):
                                for i in range(tamanho_lista):
                                        if (chat_id_lista[i] != ultimo_usuario):
                                                telegram_bot.sendMessage (chat_id_lista[i], "Portao foi aberto")
                                                texto = "Portao foi aberto " + str(datetime.datetime.now())
                                                log(texto)
                                        portao_inicial = portao
                        elif (portao == "fechado"):
                                for i in range(tamanho_lista):
                                        if (chat_id_lista[i] != ultimo_usuario):
                                                telegram_bot.sendMessage (chat_id_lista[i], "Portao foi fechado")
                                                texto = "Portao foi fechado " + str(datetime.datetime.now())
                                                log(texto)
                                        portao_inicial = portao
                        ultimo_usuario = "sem ultimo usuario "
        except:
                texto = "Falha ao enviar informacao de portao aberto ou fechado " + str(datetime.datetime.now())
                log(texto)
