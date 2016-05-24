from mcstatus import MinecraftServer


def get_status(address, port):
    server = MinecraftServer(address, port=25565)
    return server.status()


def get_player_list(address, port):
    server = MinecraftServer(address, port=25565)
    players = server.query()
    return players.players.names
