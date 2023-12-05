import json
import time
from socket import *


class TcpConnect:

    def __init__(self, user_type, server_name, server_port):
        self.user_type = user_type
        self.server_name = server_name
        self.server_port = server_port

        self.gen_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)

        # storage vars for user and micro
        self.total_recipes = []
        self.just_ingredients = []
        self.modified_data = []

        # storage vars for micro
        self.data_to_process = []

    def connect(self):
        if self.user_type == 'User':
            # self.gen_socket.connect((self.server_name, self.server_port))
            # self.tcp_socket = self.gen_socket

            self.tcp_socket.connect((self.server_name, self.server_port))

        else:
            self.gen_socket.bind((self.server_name, self.server_port))
            self.gen_socket.listen(1)
            self.tcp_socket, addr = self.gen_socket.accept()

    def disconnect(self):
        self.tcp_socket.close()

# -----------------------------------------------------------------------------------------------------------------
    # SEND DATA FUNCTION
    # function to handle send data prep and to wait for a reply

    # General send data function
    def send_data(self, data):
        string = json.dumps(data)
        encoded = string.encode()
        encoded_len = str(len(encoded)).encode()
        print(f'{self.user_type} sending -{len(encoded)}- length of data', '\r\n')

        # send length of data first, so micro knows what to expect
        self.tcp_socket.send(encoded_len)
        time.sleep(3)

        # then send actual data
        self.tcp_socket.sendall(encoded)
        time.sleep(1)

        response = self.tcp_socket.recv(1024).decode()
        return response

    def end_send(self):
        close_string = 'close'
        close_encoded = close_string.encode()
        close_len = str(len(close_encoded)).encode()

        self.tcp_socket.send(close_len)
        time.sleep(1)
        self.tcp_socket.send(close_encoded)

    def send_mod_data(self):
        self.modified_data = [self.total_recipes, self.just_ingredients]
        for i in range(2):
            reply = self.send_data(self.modified_data[i])
            time.sleep(2)
            print(f'Received reply from user: {reply}')

# -----------------------------------------------------------------------------------------------------------------
    # RECEIVE DATA FUNCTION

    # General receive data function
    def recv_data(self, exp_len):
        data = b''
        while len(data) < exp_len:
            more = self.tcp_socket.recv(exp_len - len(data))
            if not more:
                raise Exception("Short socket read")
            data += more
        actual_len = len(data)

        # if processing the close message, do not need to send receipt message back to main
        if data.decode() == 'close':
            return data
        else:
            self.tcp_socket.send(f'"{self.user_type} received -{actual_len}- length of data"'.encode())
            return data

    # User specific get modified data function
    def get_mod_data(self):
        self.modified_data = [self.total_recipes, self.just_ingredients]
        for i in range(2):
            time.sleep(1)
            cur_len = int(self.tcp_socket.recv(1024).decode())
            time.sleep(1)

            cur_data = self.recv_data(cur_len).decode()
            cur_json_objects = json.loads(cur_data)
            self.modified_data[i] = cur_json_objects

        return self.modified_data

    # Microservice specific get raw data function
    def get_raw_data(self):
        listening = True
        while listening:
            # first receive data length to expect
            cur_len = int(self.tcp_socket.recv(1024).decode())
            time.sleep(1)

            # next receive actual data
            cur_data = self.recv_data(cur_len).decode()

            if cur_data == 'close':
                listening = False
            else:
                # convert decoded json string back into json
                cur_json_objects = json.loads(cur_data)

                # add to list
                # we don't want the "hits" part, so just add the value from that key
                for i in range(len(cur_json_objects["hits"])):
                    self.data_to_process.append(cur_json_objects["hits"][i])

# -----------------------------------------------------------------------------------------------------------------
    # MICROSERVICE PROCESS DATA FUNCTION

    def organize_data(self):
        for i in range(len(self.data_to_process)):
            # rename the recipe so they go in ascending order
            new_name = 'recipe ' + str(i + 1)

            # create the new recipe dictionary
            new_recipe = {new_name: self.data_to_process[i]}

            # add new recipe to list
            self.total_recipes.append(new_recipe)

            # isolate the ingredients list from the recipe
            new_ingredients = {new_name + ' ingredients': self.data_to_process[i]['recipe']['ingredientLines']}

            # add isolated ingredients to list of ingredients
            self.just_ingredients.append(new_ingredients)
