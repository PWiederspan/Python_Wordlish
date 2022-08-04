# Peyton Wiederspan
# Socket Portfolio Project
# CS 372


# SOURCES:
####################################################################
# Socket Server/Client setup based on this tutorial:
# https://realpython.com/python-sockets/
# 
# Idea to send a initial set-length packet to determine packet size base on this Stack Overflow thread:
# https://stackoverflow.com/questions/1708835/python-socket-receive-incoming-packets-always-have-a-different-size
# 
# Word bank downloaded from Copylists.com:
# https://copylists.com/words/list-of-5-letter-words/
# 
# Using Json to send array over socket base on this Stack Overflow thread:
# https://stackoverflow.com/questions/24423162/how-to-send-an-array-over-a-socket-in-python  
####################################################################


import socket
import json
from time import sleep

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65423 # Port to listen on (non-privileged ports are > 1023)
data = bytes('', 'ascii')
count = 0
data_arr = []
win = 0

print("\n     Welcome to a game that isn't Wordle but plays exactly the same way.")
print("\n     A Random 5 letter word has been chosen and it is you mission to figure out what it is within 6 guesses")
print("\n     Type your guess and hit enter, we will respond with an array where each")
print("     value corresponds with that letter in your guess. Here is the key to help you guess")
print("\n         # = That letter isn't in the answer")
print("         + = Correct letter and in the correct spot")
print("         - = That letter is in the answer, but not in that spot")
print("\n")
print("     Type /q at any point to quit the game.\n")

while data_arr != ['+', '+', '+', '+', '+'] and count < 6:
    count += 1
    # Get guess from User
    text = input("Type here:")
    if text == '/q':
        print("Goodbye!")
        text = text.encode()
        text_len = len(text)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(bytes(str(text_len), 'utf8'))
            s.sendall(text)
            break 
    text = text.encode()
    text_len = len(text)
    if text_len < 5:
        print("Word too short!")
        count -= 1
        continue
    if text_len > 5:
        print("Word too long!")
        count -= 1
        continue  
    
    # Send guess to server for processessing
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes(str(text_len), 'utf8'))
        s.sendall(text)
        # All text should be 5 letters, but to show how one could send variable length text
        # the client first sends a fixed length segment which contains the length of the text
        # so that the server knows what length of segment to expect in the second segment
        data = s.recv(1024)

        # Client/Server uses json to encode/decode the array for transporting over socket
        data = json.loads(data.decode())
        data_arr = data["response"]

    # Print the array received from the server
    print('Received', repr(data_arr))

if data_arr == ['+', '+', '+', '+', '+']:
    print("You Win, you got it in {0} tries".format(count))
    count +=1
if count == 6:
    # If the sixth guess if reached the server will send over the answer to be displayed
    # by the
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        test = ""
        text_len = len(text)
        s.sendall(bytes(str(text_len), 'utf8'))
        s.sendall(text)
        word = s.recv(1024).decode()
        print("Sorry, you're out of tries. The word was {0}".format(word))
