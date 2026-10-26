import socket


def send_data(client, data):
    """

    :param client:
    :param data_len_byte:
    :param data:
    :return:
    """
    if type(data) == str:
        data = data.encode()
    try:
       client.send(data)
    except Exception as e:
        print(f"error in recv/send try again {str(e)}")



my_sock = socket.socket()

try:
    my_sock.connect(("127.0.0.1", 80))
except Exception as e:
    print(f"error in connected - {str(e)}")
    my_sock.close()

msg = "choose:\n1 - secret message\nchoose: "

while True:
    func = input(msg)

    if func == '1':
        secret_msg = input("enter message: ")
        msg_to_send = f"POST /http_server_part3?secret HTTP/1.1\r\nContent-Length: {len(secret_msg)}\r\n\r\n{secret_msg}"
        try:
            send_data(my_sock,  msg_to_send)
        except Exception as e:
            print(f"error in send - {str(e)}")
            my_sock.close()