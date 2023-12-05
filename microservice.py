from send_and_receive import TcpConnect

# -----------------------------------------------------------------------------------------------------------------
# SERVER/MICRO SOCKET SETUP
# use a random port number > 1023
server_port = 1088
server_name = 'localhost'

my_micro = TcpConnect('Microservice', server_name, server_port)
my_micro.connect()

# -----------------------------------------------------------------------------------------------------------------
# LOOP TO LISTEN AND RECEIVE RAW DATA
my_micro.get_raw_data()

# ----------------------------------------------------------------------------------------------------------------
# DATA PROCESSING AND ORGANIZATION
my_micro.organize_data()

# -----------------------------------------------------------------------------------------------------------------
# SENDING DATA
my_micro.send_mod_data()


# -----------------------------------------------------------------------------------------------------------------
# CLOSE SOCKET AND PRINT OUT RESULTS FOR USER
print('Received: ', '\r\n', my_micro.data_to_process, '\r\n')
print('Sent all recipes: ', '\r\n', my_micro.total_recipes, '\r\n')
print('Sent just the ingredients: ', '\r\n', my_micro.just_ingredients)

my_micro.disconnect()
