import asyncio

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from .handler import login_handler, repost_handler, run_handler, export_handler
from ..http import async_ajax_impl
from ..realtime import SocketIO
from ..vo import FlowUser


class FlowShell:
    user: FlowUser = None
    shell_completer = WordCompleter(
        [
            'login',
            'repost',
            'regular',
            'order',
            'logout',
            'exit',
            'realtime',
            'run',
            'export'
        ], ignore_case=True)

    def __init__(self):
        self.loop = None

    def ignite_task_socket_io(self, socket_io: SocketIO):
        self.loop.create_task(socket_io.ignite())

    async def handle_command(self, user_input):
        input_array = user_input.split(' ')
        if input_array[0] == 'login':
            self.user = await login_handler(input_array)
        elif input_array[0] == 'exit':
            if self.user is not None:
                await async_ajax_impl.logout(self.user)
            return True  # 종료 신호
        elif self.user is None:
            print("로그인이 필요합니다. 명령어 login 을 사용하여 로그인 하세요.")
        elif input_array[0] == 'logout':
            await async_ajax_impl.logout(self.user)
            self.user = None
        elif input_array[0] == 'run':
            await run_handler(self.user, input_array)
        elif input_array[0] == 'repost':
            await repost_handler(self.user, input_array)
        elif input_array[0] == 'export':
            await export_handler(self.user, input_array)
        elif input_array[0] == 'realtime':
            socket_io = SocketIO(self.user)
            self.ignite_task_socket_io(socket_io)
        else:
            print("알 수 없는 명령어입니다.")

    async def ignite(self):
        session = PromptSession(completer=FlowShell.shell_completer)

        while True:
            try:
                message = "도시락> "
                if self.user is not None and self.user.get_name() != '':
                    message = "{}@도시락> ".format(self.user.get_name())
                    if SocketIO.sio.sid is not None and SocketIO.sio.sid != '':
                        message = "{}@도시락/{}> ".format(self.user.get_name(), SocketIO.sio.sid)
                user_input = await session.prompt_async(message, completer=FlowShell.shell_completer)
                if await self.handle_command(user_input):
                    break
            # except IndexError:
            #     print("명령어가 완료되지 않았습니다.")
            #     continue
            except KeyboardInterrupt:
                continue  # Ctrl+C를 눌러도 쉘 종료되지 않음
            except EOFError:
                break  # Ctrl+D를 누르면 쉘 종료

        print("쉘을 종료합니다.")

    def run(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.ignite())


if __name__ == '__main__':
    asyncio.run(main())
