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
import word_bank
import random
import json

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65423  # Port to listen on (non-privileged ports are > 1023)

count = 0
win = 0

# Select the winning word for this round and make an array of its letters
ans = []
words = word_bank.get_wordbank()
word = words[random.randint(0,495)]

# Comment out this line if you want to play without being able to see the word
print(word)

for char in word:
    ans.append(char)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    while win == 0 and count < 6:
        print("Count: " + str(count))
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            header = conn.recv(1)
            # decode to unicode string 
            length = int(header)
            #print(length)

            while True:
                response = ['#', '#', '#', '#', '#']
                data = conn.recv(length)
                if not data:
                    break
                
                # Compare each letter in the received word with the letters in the answer.
                #
                # if the letter is in the answer and in the correct space set that index to + in the response array
                #
                # if the letter is in the answer but not in the right spot set that index to - in the response array
                #
                # if the letter is not in the answer set that index to # in the response array
                #
                data = data.decode()
                if data == '/q':
                    print("Closing Server")
                    win = 1
                    s.close()
                    break
                for index in range(5):
                    temp = data[index]
                    check = ans[index]
                    if temp == check:
                        response[index] = '+'
                    else:
                        if temp in ans:
                            response[index] = '-'
                print(data)
                print(response)
                if response == ['+', '+', '+', '+', '+']:
                    response_arr = json.dumps({"response":response})
                    conn.sendall(response_arr.encode())
                    win = 1
                else:
                    response_arr = json.dumps({"response":response})
                    conn.sendall(response_arr.encode())
                    count += 1
    if count == 6:
        conn, addr = s.accept()
        with conn:
            conn.sendall(word.encode())
    