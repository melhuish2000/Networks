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
    send(client, get_hello_message(username))
    start_message = recieve(client)
    id = start_message["id"]
    print("This is the game id: " + id + "\n")
    
    words = get_word_list()
    secret_flag = ""
   # attempt = []
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    attempt_chars = []
    live_game = True
    fg = True
    guess = "oreas"
    send(client, get_guess_message(guess, id));
    while(live_game) :
        game_message = recieve(client)
        if game_message["type"] == "bye":
            secret_flag = game_message["flag"]
            live_game = False
            print(secret_flag)
            break
        if game_message["type"] == "retry":
            words.remove(guess)
            guesses = game_message["guesses"]
            last_guess = guesses[len(guesses)-1]
            marks = last_guess["marks"]
            print(marks)
            last_guess_char = list(guess)
            print(last_guess_char[0])

            for num in range(len(marks)):
                if(marks[num] == 2 | marks[num] == 1 ):
                    if(last_guess_char[num] in attempt_chars):
                        pass
                    else:
                        attempt_chars.append(last_guess_char[num])
                else:
                    if(last_guess_char[num] in alphabet):
                        alphabet.remove(last_guess_char[num])

      #              attempt[num] = last_guess_char[num]
       #         elif(marks[num] == 1):
        #            if(last_guess_char[num] in attempt):
         #               pass
          #          else:
           #     alphabet.remove(last_guess_char[num])
    #        for num in range(len(marks)):
     #           if(marks[num] == 2):
      #              attempt[num] = last_guess_char[num]
       #         elif(marks[num] == 1):
        #            if(last_guess_char[num] in attempt):
         #               pass
          #          else:
           #     alphabet.remove(last_guess_char[num])
            next_guess = get_next_guess(alphabet, attempt_chars, words)
            guess = next_guess
            print(next_guess)
            send(client, get_guess_message(guess, id));

                    
            

             
            
            

    

    


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

def get_word_list():
    with open("Wordlist.txt", "r") as file:
        words = []
        for line in file:
            words.append(line.strip())
    return words


def get_next_guess(alphabet, attempt_chars, words:list):
    print(alphabet)
    print(attempt_chars)
    next_guess = ""
    if len(attempt_chars) == 5:
        for word in words:
            for char in word:
                if char not in attempt_chars:
                    break
            else:
                next_guess = word
                return next_guess

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
        if use_default_port:
            port = 27994
        
    hostname = sys.argv[counter]
    counter+=1
    username = sys.argv[counter]

    play_game(port, tls, hostname, username)




    #{"type": "retry",
    #  "id": <string>,
    #  "guesses": [{ "word": <string>, "marks": <array> },
    #              { "word": <string>, "marks": <array> }, ... ]}\n