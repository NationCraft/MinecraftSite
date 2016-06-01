from app import app
from app.controllers import minecraftstats as mc
from app.controllers import player_log
from flask import render_template


@app.route('/')
def main():

    beta_status, beta_player_list, beta_server_online = mc.get_all_mc_info('beta.nationmc.net', 25565)
    play_status, play_player_list, play_server_online = mc.get_all_mc_info('play.nationmc.net', 25565)
    dev_status, dev_player_list, dev_server_online = mc.get_all_mc_info('dev.nationmc.net', 25565)

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
    player_list = []
    server_list = []
    player_data = None
    player_list, server_list = player_log.get_player_server_list()
    if playername is not None and servername is not None:
        print("running player log")
        player_data = player_log.get_player_log(timezone, playername, servername)

    return render_template('player_log.html',
                           player_list=player_list,
                           server_list=server_list,
                           player_selected=playername,
                           server_selected=servername,
                           player_data=player_data,
                           timezone_selected=timezone)