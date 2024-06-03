# Tower Defense Game

## 프로젝트 설명
간단한 타워 디펜스 게임으로 Pygame을 사용하여 개발되었습니다. 게임은 타워 배치, 적 웨이브, 타워 업그레이드, 적과 플레이어의 기본 체력 시스템을 특징으로 합니다.

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

### Linux (소리x)
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
- `main.py`: 게임의 메인 파일로, 타워 배치, 적 생성, 웨이브 시스템, 타워 업그레이드 등의 기능을 포함하고 있습니다.
- **타워 배치**: 민트색 원을 클릭하여 타워를 배치하고 업그레이드할 수 있습니다.
- **적 웨이브**: 적은 일정 시간 간격으로 생성되며, 웨이브가 진행될수록 강해집니다.
- **사운드**: 로컬 환경에서만 작동하는 사운드 기능을 포함하고 있습니다.

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

## 구동 영상

## References
[1] [pybox2d](https://github.com/pybox2d/pybox2d)  
[2] [pygame](https://github.com/pygame/pygame)
