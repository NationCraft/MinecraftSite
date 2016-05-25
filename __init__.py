from flask import Flask, render_template, request
import minecraftstats as mc
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.minecraft_logger
db_log = db.session_log


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
def player_log(playername=None):
    player_list = []
    server_list = []
    player_selected = playername
    server_selected = None
    log_data = db_log.find()
    for i in log_data:
        if not i['username'] in player_list:
            player_list.append(i['username'])
        if not i['server'] in server_list:
            server_list.append(i['server'])
    return render_template('player_log.html',
                           player_list=player_list,
                           server_list=server_list,
                           player_selected=player_selected)

'''
@app.route('/player_log/<playername>')
def player_log(playername):
    render_template('player_log.html')
'''

if __name__ == '__main__':
    app.run(debug=True)
