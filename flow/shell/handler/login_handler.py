from getpass import getpass

from ...service.login_service import login


async def login_handler(input_array: list):
    if len(input_array) == 1:
        id = input("로그인 아이디를 입력하세요: ")
        pw = getpass("로그인 비밀번호를 입력하세요: ")
        return await login(id, pw)
    elif input_array[1] == "prompt":
        id = input("로그인 아이디를 입력하세요: ")
        pw = getpass("로그인 비밀번호를 입력하세요: ")
        return await login(id, pw)