import socket
import threading
import database as db
from server_logic import *
from serializer import serialize, deserialize

HEADER = 64
PORT = 5055
SERVER = "192.168.0.12"  # IPV4 of local server
ADDR = (SERVER, PORT)  # Address to be bound
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
KICK_MESSAGE = "!KICK"
VERIFY_MESSAGE = "!VERIFY"
WAIT_MESSAGE = "!WAIT"
START_MESSAGE = "!START"
START_STATE = False

# Stream data through socket (Using IPV4)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)  # Bind socket to address

# To keep track of which players are connected
# (WARNING: USING ADDRESS OF USER FOR NOW!)
players_ls = []

db_players = db.fetch("players")

def send(conn, msg):
    """
    For server to send message to clients.

    :param conn: Connection IPV4
    :param msg: message to send to clients
    :return: NONE
    """

    message = msg.encode(FORMAT)
    msg_length = len(message)  # Get length of message (in bytes)
    send_length = str(msg_length).encode(FORMAT)  # Encode Message Length
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)


def handle_client(conn, addr):
    START_STATE = False
    """
    Handles client threading for server functions (Listens for client message)

    :param connection: Connection IPV4
    :param addr: Address of User
    :return: NONE
    """
    print(f"[NEW CONNECTION] {addr} connected...")

    connected = True
    while connected:

        # How many BYTES to receive from the client
        # Wait till receive message from client before continuing

        # Get the length of message
        # (i.e. "124....." -> indicates 124 bytes for message)
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:  # Check if message is NONE (First Connection)
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)  # Get actual message

            if not START_STATE:
                reply = ""

                if msg == WAIT_MESSAGE:
                    if len(players_ls) == num_players:
                        START_STATE = True
                        reply = START_MESSAGE
                    else:
                        reply = "Waiting for others to join..."

                # For disconnecting client
                elif msg == DISCONNECT_MESSAGE:
                    connected = False

                else:
                    data = deserialize(msg)
                    name = data["pname"]
                    hashed_pw = data["password"]
                    verifier = {}
                    for row in db_players:
                        k,v = row["pname"], row["password"]
                        verifier[k] = v
                    if name in verifier.keys():
                        if hashed_pw == verifier[name]:
                            print(name,"verified")
                            reply = VERIFY_MESSAGE
                            players_ls.append(name)
                        else:
                            reply = KICK_MESSAGE
                    else:
                        print(name,hashed_pw,"is new")
                        reply = VERIFY_MESSAGE
                        db.insert("players",pname=name,password=hashed_pw,points=0)
                        players_ls.append(name)

                    game.addPlayer(Player(name,len(players_ls)-1,0))

                print(players_ls)

                print(f"[{addr}] {msg}")

                # To get server to send message
                send(conn, reply)
            else:
                print(msg)
                data = json.loads(msg)
                pname = data["name"]
                extra = data["extra"]
                for player in game.players:
                    if player.name == pname:
                        if extra["action"] == "query":
                            send(conn,player.toJSON())
                        elif extra["action"] == "draw":
                            game.draw(pname,extra["amt"]) if "amt" in extra.keys() else game.draw(pname)
                            send(conn,player.toJSON())
                        elif extra["action"] == "discard":
                            game.discard(pname,extra["index"])
                            send(conn,game.toJSON())
                        elif extra["action"] == "point":
                            newpoints = int(extra["amt"])
                            db.update("pname",pname,points=newpoints)
                            send(conn,game.toJSON())
                        else:
                            send(conn,game.toJSON())
                #send(conn,"hello")

        else:
            # To keep track of client connected (Using address of user):
            pass

    conn.close()


def start(num_players):
    """
    Gets server to listen for connections, threads handle_client() if
    there is a connection request.
    :return: NONE
    """

    server.listen()  # Get server to listen for connections
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:
        # Get server to wait for connection, take connection info if present
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
num_players = 2
game = Game()
start(num_players)



