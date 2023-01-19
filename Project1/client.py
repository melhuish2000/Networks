import socket
import json
import ssl
import sys



def play_game(port: int, tls: bool, hostname: str, username: str):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if tls:
        context = ssl.create_default_context()
        client = context.wrap_socket(client, server_hostname = hostname)
    server = (hostname, port)

    client.connect(server)
    send(client, get_hello_message())
    start_message = recieve(client)
    id = start_message["id"]
    print(id)


    


def get_hello_message(username):
    return {"type": "hello", "northeastern_username": username}


def get_guess_message(guess, game_id):
    return {"type": "guess", "id": game_id, "word": guess}


#formats and sends
def send(client, dictionary):
    data = json.dumps(dictionary)
    encoded = f"{data}\n".encode("utf-8")
    client.send(encoded)



#Recieve
def recieve(client) -> dict:
    return json.loads(client.recv(1000000).decode("utf-8").strip())




if __name__ == "__main__":
    counter = 1

    port = 27993
    tls = False
    use_default_port = True

    if sys.argv[counter] == "-p":
        port = int(sys.arv[counter])
        counter += 1
        use_default_port = False

    if sys.argv[counter] == "-s":
        tls = True
        if use_default_port:
            port = 27994
        
    hostname = sys.argv[counter]
    counter+=1
    username = sys.argv[counter]

    play_game(port, tls, hostname, username)




    