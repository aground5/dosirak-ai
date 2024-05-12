import datetime

from ...job.dosirak_job import check_next_order_post_exist
from ...tools import get_next_workday, get_recent_workday
from ...vo import FlowUser


async def run_handler(user: FlowUser, input_array: list):
    if len(input_array) == 1:
        await check_next_order_post_exist(user, get_next_workday())
    elif input_array[1] == "next":
        await check_next_order_post_exist(user, get_next_workday())
    elif input_array[1] == "recent":
        await check_next_order_post_exist(user, get_recent_workday())
    else:
        strdate = input_array[1]
        target_date = datetime.datetime.strptime(strdate, "%m/%d")
        await check_next_order_post_exist(user, target_date)
