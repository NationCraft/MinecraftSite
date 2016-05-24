from flask import Flask, render_template
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
                           title='NationCraft Server Status',
                           beta_users_connected=beta_status.players.online,
                           beta_player_list=beta_player_list,
                           beta_server_online=beta_server_online)


if __name__ == '__main__':
    app.run(debug=True)
