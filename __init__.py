from flask import Flask, render_template, request
import minecraftstats as mc
from pymongo import MongoClient
from datetime import datetime, timedelta, tzinfo
import timeconverter

app = Flask(__name__)


@app.route('/')
def main():
    try:
        beta_status = mc.get_status('connect.bonecrack.com', 25565)
        beta_player_list = mc.get_player_list('connect.bonecrack.com', 25565)
        beta_server_online = True
    except Exception:
        beta_server_online = False

    return render_template('main.html',
                           beta_users_connected=beta_status.players.online,
                           beta_player_list=beta_player_list,
                           beta_server_online=beta_server_online)


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


def get_mongo_collection(mongo_client):
    data_log = mongo_client.find()
    return data_log


def get_mongo_all(mongo_client, timezone):
    return_log = []
    print('all')
    for p in mongo_client.find():
        return_log.append(p)
        print(timezone)
        if timezone != 'utc':
            print(timezone)
            pst = timeconverter.PST
            print(type(return_log[len(return_log) - 1]['logout']))
            login = timeconverter.utc_to_local(return_log[len(return_log) - 1]['login'], timezone)
            logout = timeconverter.utc_to_local(return_log[len(return_log) - 1]['logout'], timezone)
            print(_login, _logout)
            return_log[len(return_log - 1)]['login'] = login
            return_log[len(return_log - 1)]['logout'] = logout

        s = str(return_log[len(return_log) - 1]['logout'] - return_log[len(return_log) - 1]['login'])
        return_log[len(return_log) - 1]['session'] = s[:-7]
    return return_log


def get_mongo_all_servers(mongo_client, timezone, player):
    return_log = []
    for p in mongo_client.find({'username': player}):
        return_log.append(p)
        if timezone != 'utc':
            _login = timeconverter.utc_to_local(return_log[len(return_log - 1)]['login'], timezone)
            _logout = timeconverter.utc_to_local(return_log[len(return_log - 1)]['logout'], timezone)
            return_log[len(return_log - 1)]['login'] = _login
            return_log[len(return_log - 1)]['logout'] = _logout

        s = str(return_log[len(return_log) - 1]['logout'] - return_log[len(return_log) - 1]['login'])
        return_log[len(return_log) - 1]['session'] = s[:-7]
    return return_log


def get_mongo_all_players(mongo_client, timezone, server):
    return_log = []
    for p in mongo_client.find({'server': server}):
        return_log.append(p)
        if timezone != 'utc':
            _login = timeconverter.utc_to_local(return_log[len(return_log - 1)]['login'], timezone)
            _logout = timeconverter.utc_to_local(return_log[len(return_log - 1)]['logout'], timezone)
            return_log[len(return_log - 1)]['login'] = _login
            return_log[len(return_log - 1)]['logout'] = _logout

        s = str(return_log[len(return_log) - 1]['logout'] - return_log[len(return_log) - 1]['login'])
        return_log[len(return_log) - 1]['session'] = s[:-7]
    return return_log


def get_mongo_all_args(mongo_client, timezone, player, server):
    return_log = []
    for p in mongo_client.find({'username': player, 'server': server}):
        return_log.append(p)
        if timezone != 'utc':
            _login = timeconverter.utc_to_local(return_log[len(return_log - 1)]['login'], timezone)
            _logout = timeconverter.utc_to_local(return_log[len(return_log - 1)]['logout'], timezone)
            return_log[len(return_log - 1)]['login'] = _login
            return_log[len(return_log - 1)]['logout'] = _logout

        s = str(return_log[len(return_log) - 1]['logout'] - return_log[len(return_log) - 1]['login'])
        return_log[len(return_log) - 1]['session'] = s[:-7]
    return return_log


# returns list[[][]]
def get_player_server_list(col_data):
    # col_data = get_mongo_collection(host='localhost', port=27017, db='minecraft_logger', collection='session_log')
    player_list = []
    server_list = []
    # multi_list = []
    for i in col_data:
        if not i['username'] in player_list:
            player_list.append(i['username'])
        if not i['server'] in server_list:
            server_list.append(i['server'])
    # multi_list.append(player_list)
    # multi_list.append(server_list)
    return player_list, server_list


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
