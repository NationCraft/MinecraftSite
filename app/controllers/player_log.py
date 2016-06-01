from pymongo import MongoClient
from app.controllers import timeconverter


def get_mongo_client():
    client = MongoClient('localhost', 27017)
    db = client.minecraft_logger
    return db.session_log


# get all data from collection unmodified
def get_mongo_collection(mongo_client):
    data_log = mongo_client.find()
    return data_log


# returns player_list and server_list
def get_player_server_list():
    mongo_client = MongoClient('localhost', 27017)
    col_data = mongo_client.find()
    player_list = []
    server_list = []
    # multi_list = []
    for i in col_data:
        if not i['username'] in player_list:
            player_list.append(i['username'])
        if not i['server'] in server_list:
            server_list.append(i['server'])
    return player_list, server_list


# get all data modified timezone and added session length
def get_mongo_all(mongo_client, timezone):
    return_log = []
    for p in mongo_client.find():
        return_log.append(p)
        if timezone != 'UTC':
            return_log[len(return_log) - 1]['login'] = timeconverter.utc_to_local(
                return_log[len(return_log) - 1]['login'], timezone)
            return_log[len(return_log) - 1]['logout'] = timeconverter.utc_to_local(
                return_log[len(return_log) - 1]['logout'], timezone)

        s = str(return_log[len(return_log) - 1]['logout'] - return_log[len(return_log) - 1]['login'])
        return_log[len(return_log) - 1]['session'] = s[:-7]
    return return_log


# get all servers modified timezone and added session length
def get_mongo_all_servers(mongo_client, timezone, player):
    return_log = []
    for p in mongo_client.find({'username': player}):
        return_log.append(p)
        if timezone != 'UTC':
            return_log[len(return_log) - 1]['login'] = timeconverter.utc_to_local(
                return_log[len(return_log) - 1]['login'], timezone)
            return_log[len(return_log) - 1]['logout'] = timeconverter.utc_to_local(
                return_log[len(return_log) - 1]['logout'], timezone)

        s = str(return_log[len(return_log) - 1]['logout'] - return_log[len(return_log) - 1]['login'])
        return_log[len(return_log) - 1]['session'] = s[:-7]
    return return_log


# get all players with server var modified timezone and added session length
def get_mongo_all_players(mongo_client, timezone, server):
    return_log = []
    for p in mongo_client.find({'server': server}):
        return_log.append(p)
        if timezone != 'UTC':
            return_log[len(return_log) - 1]['login'] = timeconverter.utc_to_local(
                return_log[len(return_log) - 1]['login'], timezone)
            return_log[len(return_log) - 1]['logout'] = timeconverter.utc_to_local(
                return_log[len(return_log) - 1]['logout'], timezone)

        s = str(return_log[len(return_log) - 1]['logout'] - return_log[len(return_log) - 1]['login'])
        return_log[len(return_log) - 1]['session'] = s[:-7]
    return return_log


# get player var and server var modified timezone and added session length
def get_mongo_all_args(mongo_client, timezone, player, server):
    return_log = []
    for p in mongo_client.find({'username': player, 'server': server}):
        return_log.append(p)
        if timezone != 'UTC':
            return_log[len(return_log) - 1]['login'] = timeconverter.utc_to_local(
                return_log[len(return_log) - 1]['login'], timezone)
            return_log[len(return_log) - 1]['logout'] = timeconverter.utc_to_local(
                return_log[len(return_log) - 1]['logout'], timezone)

        s = str(return_log[len(return_log) - 1]['logout'] - return_log[len(return_log) - 1]['login'])
        return_log[len(return_log) - 1]['session'] = s[:-7]
    return return_log


# runs correct functions to get log from db
def get_player_log(timezone, playername, servername):
    if playername == "AllPlayers":
        if servername == 'AllServers':
            return get_mongo_all(get_mongo_client(), timezone)
        else:
            return get_mongo_all_players(get_mongo_client(), timezone, servername)
    else:
        if servername == 'AllServers':
            return get_mongo_all_servers(get_mongo_client(), timezone, playername)
        else:
            return get_mongo_all_args(get_mongo_client(), timezone, playername, servername)