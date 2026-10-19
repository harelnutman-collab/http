import socket
import os
from flask import abort


def send_data(client, data_len_byte, data):
    """
    the func send to the client data from server and length
    :param client: where to send
    :param data_len_byte: message len
    :param data:the data to send
    :return:none
    """
    if type(data) == str:
        data = data.encode()
    try:
        client.send(data)
    except Exception as e:
        print(f"error in recv/send try again {str(e)}")


def get_url(answer):
    """
    return the URL from client request
    :param answer: the request
    :return: the URL
    """
    lines = answer.split('\r\n')[0]
    return lines.split(' ')[1][1: ]


def check_get_packet(answer):
    """
    return the URL from client request
    :param answer: the request
    :return: the URL
    """

    valid = False
    lines = answer.split('\r\n')[0]
    params = lines.split(' ')
    if len(params) == 3 and params[0] == 'GET' and params[2] == 'HTTP/1.1':
        valid = True
    return valid

server_sock = socket.socket()
server_sock.bind(("0.0.0.0", 80)) # 8080
server_sock.listen(3)

while True:
    client_sock, addr = server_sock.accept()
    print(f"{addr[0]} - connected")

    try:
        data = client_sock.recv(1024).decode()
    except Exception as e:
        print(f"error in recv {str(e)}")
        client_sock.close()
        continue

    if not check_get_packet(data):
        client_sock.close()
    else:

        url = get_url(data)
        print(url)
        if os.path.exists(url):
            # answer = f"HTTP/1.1 200 OK\r\nContent - Length: {str(len(url))}\r\n\r\n{url}"
            # try:
            #     data = client_sock.send(answer.encode())
            # except Exception as e:
            #     print(f"error in send {str(e)}")
            with open(url, 'rb') as file:
                image_data = file.read()

            answer = f"HTTP/1.1 200 OK\r\nContent - Length: {str(len(image_data))}\r\n\r\n".encode() + image_data
            try:
                send_data(client_sock, 6, answer)
            except Exception as e:
                print(f"error in sending {str(e)}")
        else:
            error = "404 / File Not Found"
            try:
                client_sock.send(error.encode())
            except Exception as e:
                print(f"error in send {str(e)}")

        client_sock.close()
