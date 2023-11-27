import pygame
import subprocess
import sys
import socket
import pickle
from player import Player

# 서버의 IP 주소와 포트를 수정하세요.
server_ip = "주소"  # 서버가 실행 중인 컴퓨터의 IP 주소
server_port = 포트번호


#통신을 위한 네트워크 클래스
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_ip
        self.port = server_port
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print(e)
            return None

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def get_player_state_from_server(self):
        try:
            data = self.client.recv(2048)
            return pickle.loads(data)
        except socket.error as e:
            print(e)

    def move(self,player):

        if self.p is None:
            self.p = self.connect()

        if self.p is not None:
        # 서버로부터 플레이어의 새로운 상태를 가져오는 코드
            new_player_state = self.get_player_state_from_server()

            if new_player_state is not None:
                print("Received player state from server:", new_player_state)
                if len(new_player_state) >= 2:
                    player1.update_state(new_player_state[0])
                    player2.update_state(new_player_state[1])
                    self.send_player_state(player1)
                    self.send_player_state(player2)
                else:
                    print("Invalid player state received from the server.")
            else:
                print("Failed to receive player state from the server.")
    
    def send_player_state(self, player):
        data = player.get_state()
        return self.send(data)


# 재시작 토큰 파일 위치 설정
def restart_game():
    python = sys.executable
    pygame.quit()
    subprocess.run([python, file_path])
    sys.exit()

file_path = sys.argv[0]
pygame.init()

# 화면 크기
win_width = 500
win_height = 500
win = pygame.display.set_mode((win_width, win_height))

# 화면 창 이름
pygame.display.set_caption("피카츄 사냥")

# BGM
sound = pygame.mixer.Sound("C:/Users/KIMJUNHO/source/repos/comnet2/bgm.wav")
sound.play()

# 시간
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 40)
total_time = 5
start_ticks = pygame.time.get_ticks()

# 배경 이미지
background = pygame.image.load("C:/Users/KIMJUNHO/source/repos/comnet2/background.png")

# 플레이어1 및 플레이어2 생성
player1 = Player()
player1.initialize("C:/Users/KIMJUNHO/source/repos/comnet2/player1.png", 0, 0)

player2 = Player()
player2.initialize("C:/Users/KIMJUNHO/source/repos/comnet2/player2.png", 450, 450)

network=Network()

# 이벤트 루프
running = True
restart_flag = False
while running:
    dt = clock.tick(60)  # 초당 60 프레임
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player1.move(keys)
    player2.move(keys)

    # 서버로부터 플레이어의 새로운 상태를 가져오는 코드
    new_player_state = network.get_player_state_from_server()

    # 플레이어의 상태 업데이트
    if new_player_state is not None:
        player1.update_state(new_player_state[0])
        player2.update_state(new_player_state[1])

    # 서버로 현재 플레이어의 상태를 전송
    network.send_player_state(player1)
    network.send_player_state(player2)


    # 충돌처리
    player1_rect = player1.image.get_rect(topleft=(player1.x_pos, player1.y_pos))
    player2_rect = player2.image.get_rect(topleft=(player2.x_pos, player2.y_pos))

    # 배경, 캐릭터 출력
    win.blit(background, (0, 0))
    player1.draw(win)
    player2.draw(win)

    # 타이머
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255, 0, 0))
    win.blit(timer, (460, 10))

    text3 = game_font.render("PRESS 'R' TO RESTART", 1, (255, 0, 0))
    text4 = game_font.render("PRESS 'Q' TO QUIT", 1, (255, 0, 0))

    # 충돌
    if player1_rect.colliderect(player2_rect):
        text = game_font.render("PLAYER1 WIN!!", 1, (255, 0, 0))
        win.blit(text, (150, win_height / 2))
        win.blit(text3, (100, win_height / 10))
        win.blit(text4, (125, win_height / 5))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False
        restart_flag = True
    elif total_time - elapsed_time <= 0:
        text2 = game_font.render("PLAYER2 WIN!!", 1, (255, 0, 0))
        win.blit(text2, (150, win_height / 2))
        win.blit(text3, (100, win_height / 10))
        win.blit(text4, (125, win_height / 5))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False
        restart_flag = True

    pygame.display.update()

# 게임 종료

# 다시 실행
if restart_flag:
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
