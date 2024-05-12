import logging
import uuid

import socketio

import constants
from ..job.dosirak_job import task_check_next_order_post_exist
from ..tools import get_next_workday
from ..vo import FlowUser


class SocketIO:
    user: FlowUser = None
    token = None
    identifier = None
    sio = socketio.AsyncClient(logger=False, engineio_logger=False)

    def __init__(self, user: FlowUser):
        token = None
        cookies = user.get_session().cookie_jar.filter_cookies('https://flow.team')
        for key, cookie in cookies.items():
            if key == "JSESSIONID":
                token = cookie.value
        if token is None:
            logging.error("SocketIO init: JSESSIONID를 User 세션에서 찾을 수 없습니다.")
            return
        SocketIO.token = token
        SocketIO.user = user
        SocketIO.identifier = f"{user.user_id}_{user.duid}_{str(uuid.uuid4())}"

    @staticmethod
    @sio.event
    async def connect():
        logging.debug(f'connection established. sio={SocketIO.sio.sid} transport={SocketIO.sio.transport()}')
        await SocketIO.sio.emit('requestRandomChat', {'ROOM_SRNO': SocketIO.user.user_id})
        await SocketIO.sio.emit('requestRandomChat', {'ROOM_SRNO': SocketIO.identifier})

    @staticmethod
    @sio.on('receiveMessage')
    async def receive_message(data):
        logging.debug(f'message received with data={data}')
        if data["CHAT_CODE"] == "USER0000" and data["COLABO_SRNO"] == constants.DOSIRAK_COLABO_SRNO\
                and data["COLABO_COMMT_SRNO"] != '-1':
            print("도시락 프로젝트에 알림이 왔습니다. 읽지 않은 알림 수: {}".format(data["FLOW_CNT"]))
            task_check_next_order_post_exist(SocketIO.user, get_next_workday())

    @staticmethod
    @sio.on('*')
    async def any_event(event, sid, data):
        logging.debug("event={} sid={} data={}".format(event, sid, data))

    async def ignite(self):
        await self.sio.connect("https://chat.flow.team:7820?token={}".format(SocketIO.token))
        await self.sio.wait()
