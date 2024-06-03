# Tower Defense Game

## 게임 설명
Tower Defense Game은 플레이어가 타워를 배치하여 적의 경로를 방어하는 전략 게임입니다. 플레이어는 타워를 업그레이드하고, 적을 물리치며, 웨이브를 견뎌내야 합니다. 각 타워는 다양한 공격 범위와 속도를 가지며, 적들은 웨이브가 진행될수록 더 강력해집니다. 플레이어는 적을 처치하면 코인을 얻고, 이를 통해 타워를 업그레이드하거나 새로운 타워를 배치할 수 있습니다. 적이 경로의 끝에 도달하면 플레이어의 목숨이 줄어들며, 목숨이 모두 소진되면 게임이 종료됩니다.

## 설치 방법
### Windows
1. [Python3.12](https://www.python.org/downloads/) 설치
2. PowerShell에서 필요한 라이브러리 설치:
    ```bash
    pip3 install pygame
    pip3 install box2d box2d-kengz
    ```
3. 재부팅 후 게임 실행:
    ```bash
    python3 main.py
    ```

### Linux <sub><sup>(소리x)</sup></sub>
1. Docker 설치
2. Docker 이미지 빌드:
    ```bash
    docker build -t tower-defense-game .
    ```
3. Docker 컨테이너 실행:
    ```bash
    xhost +
    docker run -it \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    tower-defense-game
    ```

### MacOS
1. Python3 및 필요한 라이브러리 설치
2. 게임 실행:
    ```bash
    python3 main.py
    ```

## 실행 방법
게임을 실행하려면 `main.py`를 실행하세요. Docker를 사용하는 경우 위의 Linux 설치 방법을 참조하세요.

## 지원 Operating Systems
| OS       | 지원 여부 |
|----------|------------|
| Windows  | ⭕         |
| Linux    | ⭕         |
| MacOS    | ⭕         |

## 코드 설명
### 주요 클래스 및 함수
- **`class Tower`**:
  - 설명: 타워를 나타내는 클래스입니다.
  - `__init__(self, x, y)`: 타워의 초기 설정을 담당하며, 타워의 위치, 모양, 범위, 공격 속도를 초기화합니다.
  - `create_shape(self, shape)`: 주어진 모양에 따라 타워의 이미지를 생성합니다.
  - `upgrade(self)`: 타워를 업그레이드하여 모양을 변경하고, 범위 및 공격 속도를 개선합니다.
  - `attack(self, enemies, projectiles)`: 타워가 적을 공격하도록 합니다.
  
- **`class Enemy`**:
  - 설명: 적을 나타내는 클래스입니다.
  - `__init__(self, path)`: 적의 초기 설정을 담당하며, 경로, 속도, 체력을 초기화합니다.
  - `update(self)`: 적의 위치를 업데이트하고, 경로를 따라 이동합니다.
  - `take_damage(self, damage)`: 적이 피해를 입었을 때 체력을 감소시키고, 체력이 0 이하일 경우 적을 제거합니다.
  - `draw_health_bar(self, surface)`: 적의 체력 바를 그립니다.
  
- **`class Projectile`**:
  - 설명: 투사체를 나타내는 클래스입니다.
  - `__init__(self, pos, target)`: 투사체의 초기 설정을 담당하며, 위치와 목표를 초기화합니다.
  - `update(self)`: 투사체의 위치를 업데이트하고, 목표에 도달했을 때 피해를 입힙니다.
  
- **`def draw_intro_screen`**:
  - 설명: 게임의 시작 화면을 그립니다.
  - 세부사항: 타이틀, 시작 안내 문구, 게임 설명을 화면에 표시합니다.

- **`def draw_menu_button`**:
  - 설명: 메뉴 버튼을 화면에 그립니다.
  - 세부사항: 메뉴 버튼을 생성하고 화면의 우측 하단에 표시합니다.

- **`def draw_menu_screen`**:
  - 설명: 메뉴 화면을 그립니다.
  - 세부사항: 메뉴, 재개, 소리 켜기, 소리 끄기, 종료 버튼을 화면에 표시합니다.

- **`def handle_menu_screen_click(pos)`**:
  - 설명: 메뉴 화면의 버튼 클릭을 처리합니다.
  - 세부사항: 클릭한 위치에 따라 게임 상태를 변경합니다 (재개, 소리 켜기/끄기, 종료).

- **`def draw_game_over_screen`**:
  - 설명: 게임 오버 화면을 그립니다.
  - 세부사항: "GAME OVER" 텍스트와 재시작, 종료 버튼을 화면에 표시합니다.

- **`def handle_game_over_click(pos)`**:
  - 설명: 게임 오버 화면의 버튼 클릭을 처리합니다.
  - 세부사항: 클릭한 위치에 따라 게임을 재시작하거나 종료합니다.

- **`def main_game`**:
  - 설명: 게임의 메인 루프를 실행합니다.
  - 세부사항: 타워 배치, 적 생성, 웨이브 관리, 타워 공격, 화면 업데이트 등의 기능을 포함합니다.

- **`def place_tower(x, y)`**:
  - 설명: 주어진 위치에 타워를 배치하거나 업그레이드합니다.
  - 세부사항: 타워가 이미 존재하면 업그레이드하고, 그렇지 않으면 새로운 타워를 배치합니다.
  
- **`def spawn_enemy`**:
  - 설명: 새로운 적을 생성하여 경로를 따라 이동시킵니다.
  
- **`def is_docker`**:
  - 설명: 현재 환경이 Docker 컨테이너인지 확인합니다.
  - 세부사항: Docker 환경에서는 오디오를 비활성화합니다.

## 실행 예시

### 초기 화면
- 게임이 시작될 때 표시되는 초기 화면입니다.
- 게임 설명과 규칙이 화면에 표시됩니다.
![intro](https://github.com/JunWooP0/oss_personal_project/assets/163957128/420b48b6-19ec-42b2-81a1-0edf75596202)

### 게임 중간 단계
- 게임 플레이 중 타워를 배치하고 적을 물리치는 과정입니다.
https://github.com/JunWooP0/oss_personal_project/assets/163957128/99070d33-8839-4465-94da-15d3ecc70367
- 웨이브 진행 상황과 현재 자원 상태를 확인할 수 있습니다.
- Menu를 눌러 다양한 기능들을 수행할 수 있습니다.
![menu](https://github.com/JunWooP0/oss_personal_project/assets/163957128/4d0ffe0a-2678-41ca-a02b-952f2793abf4)
https://github.com/JunWooP0/oss_personal_project/assets/163957128/2f999406-1305-4254-93e8-8df0a1def59b


### 게임 오버 화면
- 플레이어의 라이프가 0이 되었을 때 표시되는 화면입니다.
https://github.com/JunWooP0/oss_personal_project/assets/163957128/bd1c811d-edd9-41c8-8ca8-b7c9a002fd56
- "Restart" 버튼을 누르면 게임이 처음부터 다시 시작됩니다.
https://github.com/JunWooP0/oss_personal_project/assets/163957128/0dcf9b79-d7e1-4015-85c0-91a68ed56723
- "Exit" 버튼을 클릭하면 게임이 종료됩니다.


## References
[1] [pybox2d](https://github.com/pybox2d/pybox2d)  
[2] [pygame](https://github.com/pygame/pygame)
