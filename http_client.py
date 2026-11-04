import os
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

msg = "choose:\n1 - secret message\n2 - send image\nchoose: "

while True:
    func = input(msg)
    if func == '9':
        break
    if func == '1':
        secret_msg = input("enter message: ")
        msg_to_send = f"POST /http_server_part3?secret HTTP/1.1\r\nContent-Length: {len(secret_msg)}\r\n\r\n{secret_msg}"
        try:
            send_data(my_sock,  msg_to_send)
        except Exception as e:
            print(f"error in send - {str(e)}")
            my_sock.close()

    elif func == '2':
        img_path = input("enter image path: ")
        if os.path.exists(img_path):
            with open(img_path, "rb") as file:
                img_data = file.read()
            img_name = os.path.basename(img_path)
            msg_to_send = f"POST /http_server_part3?img_name={img_name} HTTP/1.1\r\nContent-Length: {len(img_data)}\r\n\r\n".encode() + img_data
            try:
                send_data(my_sock,  msg_to_send)
            except Exception as e:
                print(f"error in send - {str(e)}")
                my_sock.close()
        else:
            print("404 Not Found")

my_sock.close()
print("bye bye")