import asyncio

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

import drag_status
from flow.service import dosirak_service
from flow.service.login_service import login
from flow.tools import get_next_workday, format_date

app = Flask(__name__)
socketio = SocketIO(app)

id = "{id}"
pw = "{pw}"

loop = asyncio.get_event_loop()
user = loop.run_until_complete(login(id, pw))


async def get_order_info_loop():
    post = await dosirak_service.get_post_by_order_date(user, get_next_workday())
    if post is None:
        return {}
    order_info = await dosirak_service.get_order_info_by_post_no(user, post["COLABO_COMMT_SRNO"])
    return post, order_info


@app.route('/api/status')
def get_order_info():
    post, order_info = loop.run_until_complete(get_order_info_loop())
    return {"data": order_info, "post": post["COMMT_TTL"]}


@app.route('/')
def khanban():
    date_str = format_date(get_next_workday())
    return render_template('khanban_board.html', date_str=date_str)


@socketio.on('drag')
def handle_drag_event(json):
    json["sid"] = request.sid
    emit('drag', json, broadcast=True)
    drag_status.drag(json['sid'], json)
    print('received: ' + str(json))


@socketio.on('shadow')
def handle_shadow_event(json):
    json["sid"] = request.sid
    emit('shadow', json, broadcast=True)
    print('received: ' + str(json))


@socketio.on('dragend')
def handle_dragend_event(json):
    json["sid"] = request.sid
    emit('dragend', json, broadcast=True)
    loop.run_until_complete(drag_status.dragend(json['sid'], json, user))
    print('received: ' + str(json))


@socketio.on('syncreq')
def handle_syncreq_event():
    json = {"sid": request.sid}
    emit('syncreq', json, broadcast=True)


@socketio.on('sync')
def handle_sync_event(json):
    json["sid"] = request.sid
    emit('sync', json, broadcast=True)
    print('received: ' + str(json))

@socketio.on('disconnect')
def handle_disconnect_event():
    try :
        drag_status.destroy(request.sid)
    except KeyError:
        pass

if __name__ == '__main__':
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True, port=5002, host="0.0.0.0")
