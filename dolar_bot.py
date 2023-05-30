import telebot, telegram, requests, queue, threading, time, random

bot = telebot.TeleBot('6204169915:AAHO-Nh2HgMZk3h-NlyrNT1tLb4ioU1D44k')
q = queue.Queue()
txt = r"./users.txt"
frases_peronistas = ['"Al amigo todo, al enemigo ni justicia."',
'"Para un argentino no hay nada mejor que otro argentino."',
'"No existe para el peronismo más que una sola clase de hombres: los que trabajan."',
'"Hay distintas clases de lealtades: la que nace del corazón, que es la que más vale, y la de la que son leales cuando no les conviene ser desleales."',
'"Cuando los pueblos agotan su paciencia, hacen tronar el escarmiento."',
'"Yo he visto malos que se han vuelto buenos, pero no he visto jamás un bruto volverse inteligente."',
'"Sin independencia económica no hay posibilidad de justicia social."',
'"Quien le da pan a perro ajeno, pierde el pan y pierde al perro."',
'"Los precios suben por ascensor, los sueldos por escalera."',
'"Gobernar es fácil, lo difícil es conducir..."',
'"Para un peronista no puede haber nada mejor que otro peronista."',
'"Las revoluciones se hacen con tiempo, o con sangre."',
'"El Justicialismo no es un hombre, es una doctrina."',
'"El Justicialismo ha dejado de ser la causa de un hombre para ser la causa del pueblo, y por ella sí valdría la pena darlo todo, incluso la vida."',
'"Le prometían todo y no le daban nada. Entonces yo empleé un sistema distinto. No prometer nada y darles todo. En vez de la mentira, decirles la verdad. En vez del engaño, ser leal y sincero y cumplir con todo el mundo."',
'"No es que nosotros seamos tan buenos, sino que los demás son peores."',
'"La verdadera democracia es aquella donde el gobierno hace lo que el pueblo quiere y defiende un solo interés: el del pueblo."',
'"El que quiera conducir con éxito tiene que exponerse; el que quiere éxitos mediocres, que no se exponga nunca; y si no quiere cometer ningún error, lo mejor es que nunca haga nada."',
'"Para conducir a un pueblo la primera condición es que uno haya salido del pueblo, que sienta y piense como el pueblo. Quien se dedica a la conducción debe ser profundamente humanista: el conductor siempre trabaja para los demás, jamás para él."'
]


def lector(direction:str):
    file = open(direction, "r+")
    file_read = file.read()

    line = ""
    lines = []
    letters = list(file_read)

    for digit in letters:
        if not digit == "\n":
            line += digit
        if digit == "\n":
            lines.append(line)
            line = ""
    return lines

def escritor(direction:str, information):
    file = open(direction, "a")
    file.write(f"{information}\n")


def blue():
    moneda = requests.get('https://api.bluelytics.com.ar/v2/latest').json()
    return {
        'venta' : int(moneda['blue']['value_sell']),
        'compra' : int(moneda['blue']['value_buy'])
    }



def telegram_bot():
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, text=f'''
Hola soy InzaBot, usá /help para lista de comandos ✌️
CFK 2023!
''')


    @bot.message_handler(commands=['help'])
    def help(message):
        bot.reply_to(message, text= """
Comandos:
/bluenow: el dolar ahora
/addme: te añade a la lista de aviso de subida de dolar
/peron, peronismo, frase, fraseperoncha, fraseperonista: Frase random de Perón
""")


    @bot.message_handler(commands=['bluenow'])
    def bluenow(message):
        bot.reply_to(message, text=f'''
El dólar está {blue()['venta']} en venta y {blue()['compra']} en compra.
VIVA PERÓN ✌️
''')

    @bot.message_handler(commands=['addme'])
    def blueadv(message):

        if not str(message.chat.id) in lector(txt):
            escritor(txt, message.chat.id)
            bot.reply_to(message, text='Añadido')
        else:
            bot.reply_to(message, text='Ya estás añadido')

    @bot.message_handler(commands=["advlist"])
    def advlist(message):
        bot.reply_to(message, text= str(lector(txt)))

    @bot.message_handler(commands=["peron", "peronismo", "frase", "fraseperoncha", "fraseperonista"])
    def frase_peronista(message):
        bot.reply_to(message, f"""
{random.choice(frases_peronistas)}
- Juan Domingo Perón
""")

    @bot.message_handler(func=lambda message: True)
    def unknown_command(message):
        bot.reply_to(message, "No te entendí, usá /help para ver la lista de comandos!")


    bot.infinity_polling()



def message_send():
    tresshold = 480
    single_use = True
    while 1:
        if  blue()['venta'] == 505 and single_use:
            for user in lector(txt):
                bot.send_message(chat_id = user, text='''
EL DOLAR LLEGÓ A 505 - ARCTIC MONKEYS
https://www.youtube.com/watch?v=qU9mHegkTc4''')
            single_use = False

        elif blue()['venta'] >= tresshold and lector(txt):
            for user in lector(txt):
                bot.send_message(chat_id = user, text= f'El dolar subió a {tresshold} VIVA PERÓN ✌️. Está {blue()["venta"]}')
            tresshold += 10
        elif blue()['venta'] < tresshold -10 and lector(txt):
            tresshold -= 10
            for user in lector(txt):
                bot.send_message(chat_id = user, text= f'El dolar bajó de {tresshold} VIVA PERÓN ✌️. Está {blue()["venta"]}')


        if not blue()['venta'] == 505:
            single_use = True


t1 = threading.Thread(target=telegram_bot)
t2 = threading.Thread(target=message_send)
t1.start()
t2.start()
