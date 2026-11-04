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
      client.send(str(len(data)).zfill(data_len_byte).encode())
      client.send(data)
    except Exception as e:
        print(f"error in recv/send try again {str(e)}")

def get_url_img(answer):
    """
    get the image name
    :param answer: the url
    :return: image name
    """
    lines = answer.split('\r\n')[0]
    img_name = lines.split(' ')[1]
    img_name = img_name.split('=')[1]
    img_name = os.path.basename(img_name)
    return img_name


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

def check_GET_POST_packet(answer):
    """
    check if the msg is in GET protocol
    :param answer: the request
    :return: the URL
    """

    valid = None
    lines = answer.split('\r\n')[0]
    params = lines.split(' ')
    if len(params) == 3  and params[2] == 'HTTP/1.1':
        if params[0] == 'GET':
            valid = "GET"
        elif params[0] == 'POST':
            valid = "POST"
    return valid

def check_POST_packet(answer):
    """
    check if the msg is in POST protocol
    :param answer: the msg from client
    :return: true if it POST
    """

    valid = False
    lines = answer.split('\r\n')[0]
    params = lines.split(' ')
    if len(params) == 3 and params[0] == 'POST' and params[2] == 'HTTP/1.1' and 'secret?' in params[1]:
        valid=True
    return valid

def recv_http_request(sock):
    """reads the headers up to \r\n\r\n, then exactly Content-Length bytes of body"""
    data = b''
    while b'\r\n\r\n' not in data:
        chunk = sock.recv(1024)
        if not chunk:
            return None, None
        data += chunk
    header, body = data.split(b'\r\n\r\n', 1)
    header = header.decode()
    length = 0
    for line in header.split('\r\n')[1:]:
        if line.lower().startswith('content-length:'):
            length = int(line.split(':')[1])
    while len(body) < length:
        chunk = sock.recv(min(4096, length - len(body)))
        if not chunk:
            break
        body += chunk
    return header, body

def save_image(img_name, img_data):
    """
    save the image data (bytes) to a file in the images folder
    :param img_name: the image file name
    :param img_data: the image content (bytes) - the body of the POST
    :return: None
    """
    os.makedirs("images_http_3", exist_ok=True)
    with open(os.path.join("images_http_3", img_name), "wb") as f:
        f.write(img_data)
    with open("http_3_images", "a") as f2:
        f2.write(img_name + "\n")



server_sock = socket.socket()
server_sock.bind(("0.0.0.0", 80)) # 8080
server_sock.listen(3)

do_not_touch_files = ["C:/Users/adipe/Downloads/1.txt"] # files that not valid to get
moved_files = {"C:/Users/adipe/Downloads/client_image.py" : "C:/Users/adipe/Downloads/server_image.py"} # files that were moved
while True:
    client_sock, addr = server_sock.accept()
    print(f"{addr[0]} - connected")
    while True:
        try:
            header, body = recv_http_request(client_sock)
        except Exception as e:
            print(f"error in recv {str(e)}")
            header, body = None, None
        if header is None:
            client_sock.close()
            print("disconnected")
            break
        data = header + '\r\n\r\n'  # text only: the headers
        print(f"data - {header}")

        valid = check_GET_POST_packet(data)
        if not valid:
            client_sock.close()
            break
        print(f"data - {data}")

        valid = check_GET_POST_packet(data)
        if not valid:
            client_sock.close()

        elif valid == "GET":

            url = get_url(data)
            print(url)

            if url == '':
                try:
                    send_file("my_first_web.html") # the html to open
                    continue # back to while
                except Exception as e:
                    print(f"error in send - {str(e)}")
                    continue
            elif os.path.exists(url) and url not in do_not_touch_files and url not in moved_files:
                try:
                    send_file(url)
                    continue # back to while
                except Exception as e:
                    print(f"error in send - {str(e)}")
                    continue
            elif url == 'calculate-next':
                msg = '5'
            elif 'calculate-next?num=' in url:
                number = url[15::]
                key, value = number.split('=')
                try:
                    num = int(value)
                except Exception as e:
                    print(f"does not a number - {str(e)}")
                    msg = "please enter only numbers!!!"
                    try:
                        send_data(client_sock, 2, msg)
                        continue
                    except Exception as e:
                        print(f"error in send - {str(e)}")
                        continue
                num += 1
                msg = str(num)
            elif 'calculate-area?' in url :
                first_split = url.split('?')[1]
                print(first_split)
                try:
                    second_split = first_split.split('&')
                    print(second_split)
                except Exception as e:
                    print(f"not valid input - {str(e)}")
                    msg = "not valid input please put - '&' between the params"
                    try:
                        send_data(client_sock, 2, msg)
                        continue
                    except Exception as e:
                        print(f"error in send - {str(e)}")
                        continue
                params_dict = {}
                not_valid = False
                for param in second_split:
                    if '=' in param:
                        key, value = param.split('=')
                        if key in params_dict:
                            msg = 'not valid input, check yourself!!!'
                            try:
                                send_data(client_sock, 2, msg)
                                not_valid = True
                                break
                            except Exception as e:
                                print(f"error in send - {str(e)}")
                                not_valid = True
                                break

                        params_dict[key] = value

                if  not not_valid and len(params_dict) == 2 and "height" in params_dict and "width" in params_dict:
                    try:
                        height = float(params_dict['height'])
                        width = float(params_dict['width'])
                    except Exception as e:
                        print(f"does not a number - {str(e)}")
                        msg = "please enter only numbers!!!"
                        try:
                            send_data(client_sock, 2, msg)
                            continue
                        except Exception as e:
                            print(f"error in send - {str(e)}")
                            continue
                    msg = str((width * height) / 2)
                else:
                    if not not_valid:
                        msg = 'not valid input, check yourself!!!'
                        try:
                            send_data(client_sock, 2, msg)
                            continue
                        except Exception as e:
                            print(f"error in send - {str(e)}")
                            continue
                    else:
                        client_sock.close()
                        continue
            elif url in do_not_touch_files:
                msg = f"HTTP/1.1 403 Forbidden\r\nContent - Length: {str(len(url))}\r\n\r\n" # msg = forbidden message
            elif url in moved_files:
                new_location = moved_files[url]
                msg = f"HTTP/1.1 301 Moved Permanently\r\nLocation: {new_location}\r\nContent - Length: {str(len(url))}\r\n\r\n"  # msg = file moved message
            elif url == 'server':
                msg = f"HTTP/1.1 500 Internal Server Error\r\nContent - Length: {str(len(url))}\r\n\r\n" # msg = server message
            else:
                msg = f"HTTP/1.1 404 Not Found\r\nContent - Length: {str(len(url))}\r\n\r\n" # msg = file not found message

            try:
                send_data(client_sock, 2, msg)
            except Exception as e:
                print(f"error in send {str(e)}")

            client_sock.close()
        else:

            url = get_url(data)
            print(f"url in post: {url}")

            if not 'http_server_part3' in url:
                client_sock.close()
                break

            elif url == 'http_server_part3?secret':
                secret = body.decode()
                print(secret)
                with open("http_3_secret_words", "a") as file:
                    file.write(secret+"\n")

            elif 'http_server_part3?img_name=' in url:
                img_name = get_url_img(data)
                print(img_name)

                save_image(img_name, body)