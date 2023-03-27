import time
import random
import string
import matplotlib.pyplot as plt

players = 50
servers = 3
slots = 32

server_stats = {f"Server{i}": 0 for i in range(1, servers+1)}
queue = []

def empty_server_method(server_stats):
    return min(server_stats, key=server_stats.get)

def full_server(server_name, slots):
    return server_stats[server_name] >= slots

def server_update():
    print ("Server stats:")
    for server, players in server_stats.items():
        if players>=15:
            print(f"Hostname: {server} | Players: {players}/{slots} | Ping {random.randint(1, 50)} ms")
        else:
            print(f"Hostname: {server} | Players: {players}/{slots} | Ping: {random.randint(20, 50)} ms")
    print ("-------------------------------------------------------------------------------")


graph_data = {f"Server{i}": [0] for i in range(1, servers+1)}
graph_x = [0]

def update_graphs():
    graph_x.append(len(graph_x))
    for server, players in server_stats.items():
        graph_data[server].append(players)
    plt.clf()
    plt.subplots_adjust(wspace=0.3, hspace=0.5)
    for i, (server, data) in enumerate(graph_data.items()):
        plt.subplot(1, 3, i+1)
        plt.plot(graph_x, data)
        plt.title(f"{server}")
        plt.xlabel("Time")
        plt.ylabel("Number of players")
    plt.suptitle("Server stats over time")
    plt.show()

def simulate():
    for i in range(players):
        queue.append(f"Player{i+1}")
        ip = ".".join(map(str, (random.randint(0, 255) for IPs in range(4))))
        names = string.ascii_uppercase
        name = ''.join(random.choice(names) for name in range(10))
        print(f"OK-> {name}(#{i+1}) has connected. IP:{ip} | Ping: {random.randint(1, 50)} ")
        time.sleep(random.randint(1, 3))

        empty_server = empty_server_method(server_stats)
        while full_server(empty_server, slots):
            empty_server=empty_server_method(server_stats)
        server_stats[empty_server] +=1

        print (f"{name} (#{i+1}) has been redirected to server {empty_server}.")
        server_update()
        timeout = random.randint(1, 10)
        if timeout == 8:
            player = queue.pop(0)
            print(f"TIMEOUT-> Player(#{i+2}) has timed out and has been removed from the queue.")
            server_update()
        if timeout == 7:
            server_stats[empty_server] -= 1
            print(f"KICK -> A player has been removed from the server {empty_server}.")
            server_update()

simulate()
update_graphs()