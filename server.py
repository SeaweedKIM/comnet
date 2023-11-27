
import socket
from _thread import *
from player import Player
import pickle

server = "주소"
port = 포트번호
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

# 초기에는 두 플레이어를 생성하지 않고 빈 리스트로 시작
players = []
connected_players = 0
max_players = 2

def threaded_client(conn, player):
    print("Thread started")
    global connected_players

    # 새로운 플레이어가 접속할 때마다 players 리스트에 추가
    players.append(Player())
    players[player].initialize(f"image address", 0, 0)

    conn.send(pickle.dumps(players[player].get_state()))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player].update_state(data)

            if not data:
                print("Disconnected")
                break
            else:
                # 플레이어 상태 업데이트
                other_player_id = 1 if player == 0 else 0
                reply = [players[other_player_id].get_state(), players[player].get_state()]
                # if player == 1:
                #     reply = players[0].get_state()
                # else:
                #     reply = players[1].get_state()

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except Exception as ex:
            print("Exception in threaded_client:", ex)
            break

    print("Lost connection")
    conn.close()
    connected_players -= 1

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    if connected_players < max_players:
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
        connected_players += 1
        print("Thread started for player", currentPlayer)

        if connected_players == max_players:
            print("Maximum players reached. Server will now exit when both players disconnect.")
    else:
        print("Maximum players reached. Connection refused.")
        conn.close()

    if currentPlayer > max_players:
        break  # exit the loop after the second player connects
