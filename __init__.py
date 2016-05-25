from flask import Flask, render_template, request
import minecraftstats as mc
from pymongo import MongoClient

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
@app.route('/player_log/<playername>')
@app.route('/player_log/<playername>/<servername>')
def player_log(playername=None, servername=None):
    # col_data = player_log.get_mongo_collection('localhost', 27017, 'minecraft_logger', 'session_log')
    player_list, server_list = get_player_server_list(get_mongo_collection(get_mongo_client()))
    player_selected = playername
    server_selected = servername
    player_data = None

    if playername is not None and servername is not None:
        print("running player log")
        player_data = get_player_log(playername, servername)

    return render_template('player_log.html',
                           player_list=player_list,
                           server_list=server_list,
                           player_selected=player_selected,
                           server_selected=server_selected,
                           player_data=player_data)


# get_player_log functions *******************************************************
def get_mongo_client():
    client = MongoClient('localhost', 27017)
    db = client.minecraft_logger
    return db.session_log


def get_mongo_collection(mongo_client):
    data_log = mongo_client.find()
    return data_log


def get_mongo_all_servers(mongo_client, player):
    print('all servers', player)
    return mongo_client.find({'username': player})


def get_mongo_all_players(mongo_client, server):
    print('all players', server)
    return mongo_client.find({'server': server})


def get_mongo_all_args(mongo_client, player, server):
    print('all args', player, server)
    return mongo_client.find({'username': player, 'server': server})


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


def get_player_log(playername, servername):
    if playername == "AllPlayers":
        if servername == 'AllServers':
            return get_mongo_collection(get_mongo_client())
        else:
            return get_mongo_all_players(get_mongo_client(), servername)
    else:
        if servername == 'AllServers':
            return get_mongo_all_servers(get_mongo_client(), playername)
        else:
            return get_mongo_all_args(get_mongo_client(), playername, servername)


if __name__ == '__main__':
    app.run(debug=True)
