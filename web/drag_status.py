from service import apply_update

dragging_user = {}


def drag(sid, data):
    dragging_user[sid] = data


async def dragend(sid, data, user):
    if dragging_user.get(sid):
        prev_data = dragging_user[sid]
        await apply_update(prev_data, data, user)

def destroy(sid):
    dragging_user.pop(sid)
