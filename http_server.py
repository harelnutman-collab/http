import socket

def get_url(answer):
    """
    return the URL from client request
    :param answer: the request
    :return: the URL
    """
    url = None
    lines = answer.split('\r\n')[0]
    params = lines.split(' ')
    if len(params) == 3 and params[0] == 'GET' and params[2] == 'HTTP/1.1':
        url = params[1]
    return url[1:]



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
    else:
        print(data)
        url = get_url(data)
        if url:
            answer = f"HTTP/1.1 200 OK\r\nContent - Length: {str(len(url))}\r\n\r\n{url}"
            try:
                data = client_sock.send(answer.encode())
            except Exception as e:
                print(f"error in send {str(e)}")