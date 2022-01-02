import socket, gui, json, hashlib
from serializer import serialize, deserialize
from time import sleep

HEADER = 64
PORT = 5055
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
WAIT_MESSAGE = "!WAIT"
START_MESSAGE = "!START"
KICK_MESSAGE = "!KICK"
VERIFY_MESSAGE = "!VERIFY"
SERVER = "132.147.94.36"
ADDR = (SERVER, PORT)
name = ""
extra = {}

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    """ For client to send message to server """
    message = msg.encode(FORMAT)
    msg_length = len(message)  # Get length of message (in bytes)
    send_length = str(msg_length).encode(FORMAT)  # Encode Message Length
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        #print(f"{msg}")

    return msg

login = False
while not login:
    name = input("What is your name? ")
    password = input("Password: ").encode('UTF-8')
    hashed_pw = hashlib.sha256(password).hexdigest()
    data = {"pname": name, "password": hashed_pw}
    reply = send(serialize(data))
    if reply == KICK_MESSAGE:
        print("Wrong Password!")
    elif reply == VERIFY_MESSAGE:
        print("Successfully logged in as",name)
        login = True
    else:
        print("Unknown Error")


reply = ""
while not reply == START_MESSAGE:
    reply = send(WAIT_MESSAGE)
    sleep(1)

print("Game Started!")
extra = {"action": "draw", "amt": 13}
data = {"name" : name, "extra" : extra}
hand = deserialize(send(serialize(data)))["hand"]

root = gui.Tk()
root.geometry("1920x1080+0+0")
app = gui.Application(master=root)
app.displayHand(hand)

while True:
    data = {"name" : name, "extra": {"action":""}}
    if app.selected is not None:
        extra = {"action": "discard", "index": app.selected}
        data = {"name" : name, "extra" : extra}
        reply = send(serialize(data))
        try:
            game = deserialize(reply)
            players = game["players"]
            for player in players:
                if player["name"] == name:
                    hand = player["hand"]
                    app.displayHand(hand)
            app.selected = None
        except:
            pass
    else:
        reply = send(serialize(data))
        try:
            game = deserialize(reply)
        except:
            pass

    try:
        pile1 = game["pile1"]["cards"]
        pile2 = game["pile2"]["cards"]
        app.displayPileCards(pile1,pile2)
    except:
        pass
    sleep(0.1)
    app.update()

'''
while True:
    extra = {"action": "query"}
    data = {"name" : name, "extra" : extra}
    send(json.dumps(data))
    sleep(1)
'''
