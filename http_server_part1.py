#git link = https://github.com/harelnutman-collab/http
import socket
import os



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
    if lines.split(' ')[1] == "/":
        url_data = ''
    else:
        url_data = lines.split(' ')[1][1: ]
    return url_data


def send_file(file_name):
    """
    the func send file to client
    :param file_name: the file name
    :return: none
    """
    with open(file_name, 'rb') as file:
        file_data = file.read()

    answer = f"HTTP/1.1 200 OK\r\nContent - Length: {str(len(file_data))}\r\n\r\n".encode() + file_data
    try:
        send_data(client_sock, 6, answer)
    except Exception as e:
        print(f"error in sending {str(e)}")

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

        if url == '':
            send_file("my_first_web.html")
        elif os.path.exists(url):
            send_file(url)
        else:
            error = f"HTTP/1.1 404 Not Found\r\nContent - Length: {str(len(url))}\r\n\r\n"
            try:
                send_data(client_sock, 1, error)
            except Exception as e:
                print(f"error in send {str(e)}")

        client_sock.close()
