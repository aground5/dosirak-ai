import logging

from flow.shell import FlowShell

logging.basicConfig(
    filename='debug.log',  # 로그를 기록할 파일
    filemode='a',  # 파일 모드 ('a'는 추가, 'w'는 덮어쓰기)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 로그 형식
    level=logging.DEBUG
)


shell = FlowShell()
shell.run()
