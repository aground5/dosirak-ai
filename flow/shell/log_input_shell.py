import logging

from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout

# 로그 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 로그 메시지를 저장할 버퍼
log_buffer = Buffer()

# 로그 메시지를 업데이트하는 함수
def log_message(message):
    log_buffer.text += message + '\n'

# 로그를 위한 윈도우
log_window = Window(content=BufferControl(buffer=log_buffer), wrap_lines=True)

# 사용자 입력을 위한 버퍼와 윈도우
input_buffer = Buffer()
input_window = Window(content=BufferControl(buffer=input_buffer))

# 레이아웃 구성
root_container = HSplit([
    log_window,  # 로그 윈도우
    input_window  # 입력 윈도우
])
layout = Layout(root_container)

# 키 바인딩 설정
kb = KeyBindings()

@kb.add('enter')
def _(event):
    # 사용자 입력 처리
    user_input = input_buffer.text
    if user_input.strip():
        log_message(f"User input: {user_input}")
    input_buffer.reset()

# 애플리케이션 구성 및 실행
application = Application(layout=layout, key_bindings=kb, full_screen=True)

if __name__ == '__main__':
    application.run()

    # 로깅 테스트
    logger.debug("Debug message")
    logger.info("Info message")
