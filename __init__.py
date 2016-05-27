from flask import Flask, render_template, request
import minecraftstats as mc
from pymongo import MongoClient
import timeconverter

app = Flask(__name__)


@app.route('/')
def main():
    try:
        beta_status = mc.get_status('beta.nationmc.net', 25565).players.online
        beta_player_list = mc.get_player_list('beta.nationmc.net', 25565)
        beta_server_online = True
    except Exception:
        beta_status = 0
        beta_player_list = []
        beta_server_online = False

    try:
        play_status = mc.get_status('play.nationmc.net', 25565).players.online
        play_player_list = mc.get_player_list('play.nationmc.net', 25565)
        play_server_online = True
    except Exception:
        play_status = 0
        play_player_list = []
        play_server_online = False
    try:
        dev_status = mc.get_status('dev.nationmc.net', 25565).players.online
        dev_player_list = mc.get_player_list('dev.nationmc.net', 25565)
        dev_server_online = True
    except Exception:
        dev_status = 0
        dev_player_list = []
        dev_server_online = False

    return render_template('main.html',
                           beta_users_connected=beta_status,
                           beta_player_list=beta_player_list,
                           beta_server_online=beta_server_online,
                           play_users_connected=play_status,
                           play_player_list=play_player_list,
                           play_server_online=play_server_online,
                           dev_users_connected=dev_status,
                           dev_player_list=dev_player_list,
                           dev_server_online=dev_server_online)


@app.route('/player_log/')
@app.route('/player_log/<timezone>')
@app.route('/player_log/<timezone>/<playername>')
@app.route('/player_log/<timezone>/<playername>/<servername>')
def player_log(timezone=None, playername=None, servername=None):
    player_list, server_list = get_player_server_list(get_mongo_collection(get_mongo_client()))
    player_data = None
    if playername is not None and servername is not None:
        print("running player log")
        player_data = get_player_log(timezone, playername, servername)

    return render_template('player_log.html',
                           player_list=player_list,
                           server_list=server_list,
                           player_selected=playername,
                           server_selected=servername,
                           player_data=player_data,
                           timezone_selected=timezone)


# get_player_log functions *******************************************************
def get_mongo_client():
    client = MongoClient('localhost', 27017)
    db = client.minecraft_logger
    return db.session_log


# get all data from collection unmodified
def get_mongo_collection(mongo_client):
    data_log = mongo_client.find()
    return data_log


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


# returns player_list and server_list
def get_player_server_list(col_data):
    player_list = []
    server_list = []
    # multi_list = []
    for i in col_data:
        if not i['username'] in player_list:
            player_list.append(i['username'])
        if not i['server'] in server_list:
            server_list.append(i['server'])
    return player_list, server_list


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


if __name__ == '__main__':
    app.run()
