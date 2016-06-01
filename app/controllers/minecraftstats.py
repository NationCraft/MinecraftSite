from mcstatus import MinecraftServer


def get_status(address, port):
    server = MinecraftServer(address, port=25565)
    return server.status()


def get_player_list(address, port):
    server = MinecraftServer(address, port=25565)
    players = server.query()
    return players.players.names


def get_all_mc_info(address, port):
    try:
        status = get_status(address, port).players.online
        player_list = get_player_list(address, port)
        server_online = True
    except Exception:
        status = 0
        player_list = []
        server_online = False

    return status, player_list, server_online