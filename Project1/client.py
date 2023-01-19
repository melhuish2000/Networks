import socket
import json
import ssl
import sys


#Runs the game
def play_game(port: int, tls: bool, hostname: str, username: str):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if tls:
        context = ssl.create_default_context()
        client = context.wrap_socket(client, server_hostname = hostname)
    server = (hostname, port)
    client.connect(server)
    send(client, get_hello_message(username))
    start_message = recieve(client)
    id = start_message["id"]
    
    words = get_word_list()
    secret_flag = ""
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    attempt_chars = []
    live_game = True
    fg = True

    #First guess
    guess = "oreas"
    send(client, get_guess_message(guess, id))

    #The guessing loop
    while(live_game) :
        game_message = recieve(client)
        if game_message["type"] == "bye":
            secret_flag = game_message["flag"]
            live_game = False
            print(secret_flag)
            break
        if game_message["type"] == "retry":

            #Unpack JSON
            words.remove(guess)
            guesses = game_message["guesses"]
            last_guess = guesses[len(guesses)-1]
            marks = last_guess["marks"]

            #Turn the last guess into a list of characters
            last_guess_char = list(guess)

            #Check attempt and add correct characters to list
            for num in range(len(marks)):
                if(marks[num] == 2 or marks[num] == 1 ):
                    if(last_guess_char[num] in attempt_chars):
                        pass
                    else:
                        attempt_chars.append(last_guess_char[num])
            
            #Remove incorrect letters from alphabet list
            for num in range(len(marks)):
                 if(last_guess_char[num] in alphabet and marks[num] == 0 and last_guess_char[num] not in attempt_chars):
                    alphabet.remove(last_guess_char[num])

            #Prepare and send next guess
            next_guess = get_next_guess(alphabet, attempt_chars, words)
            guess = next_guess
            send(client, get_guess_message(guess, id));

                    
            

             
            
            

    

    

#Hello message
def get_hello_message(username):
    return {"type": "hello", "northeastern_username": username}



#Format guess
def get_guess_message(guess, game_id):
    return {"type": "guess", "id": game_id, "word": guess}


#formats and sends
def send(client, dictionary):
    data = json.dumps(dictionary)
    encoded = f"{data}\n".encode("utf-8")
    client.send(encoded)


#Recieve message
def recieve(client) -> dict:
    return json.loads(client.recv(1000000).decode("utf-8").strip())

#Read list of words from file and put into list
def get_word_list():
    with open("Wordlist.txt", "r") as file:
        words = []
        for line in file:
            words.append(line.strip())
    return words

#Choose next Guess
def get_next_guess(alphabet, attempt_chars, words:list):
    next_guess = ""

    #If the list of known characters is 5, then it will only guess words with those 5 characters
    if len(attempt_chars) == 5:
        for word in words:
            for char in word:
                if char not in attempt_chars:
                    break
            else:
                next_guess = word
                return next_guess
    #Will search for the next word only using letters that have not had a 0 returned (the loop in the retry method accounts for double letters)
    for word in words:
        for char in word:
            if char not in alphabet:
                break
        else:
            next_guess = word
            return next_guess
                
            


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
        counter += 1
        if use_default_port:
            port = 27994
        
    hostname = sys.argv[counter]
    counter+=1
    username = sys.argv[counter]

    play_game(port, tls, hostname, username)




