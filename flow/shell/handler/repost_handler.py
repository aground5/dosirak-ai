from ...job.dosirak_job import regular_order_post_repost
from ...tools import get_next_workday
from ...vo import FlowUser


async def repost_handler(user: FlowUser, input_array: list):
    if input_array[1] == "order":
        pass
    elif input_array[1] == "regular":
        if input_array[2] == "order":
            await regular_order_post_repost(user, get_next_workday().month)
        else:
            print("존재하지 않는 명령어 입니다.")
    else:
        print("존재하지 않는 명령어 입니다.")
