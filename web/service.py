from flow.service import dosirak_service
from flow.tools import get_next_workday

dosirak_type_dict = {
    "heat": "발열",
    "warm": "보온",
    "salad": "샐러드"
}


async def apply_update(prev_data, data, user):
    post = await dosirak_service.get_post_by_order_date(user, get_next_workday())
    if prev_data['name'] == data['name'] and prev_data['sid'] == data['sid']:
        prev_dosirak = prev_data['type']
        dosirak = data['type']
        if prev_dosirak in ['unclassified', 'trash'] and dosirak in ['heat', 'warm', 'salad']:
            name = data['name'].split(' ')
            people = [{"FLNM": name[0], "JBCL_NM": name[1]}]
            orders = [(dosirak_type_dict[dosirak], 1)]
            await dosirak_service.create_dosirak_order(user, post, people, orders)
        elif prev_dosirak in ['heat', 'warm', 'salad'] and dosirak in ['heat', 'warm', 'salad']:
            name = data['name'].split(' ')
            people = [{"FLNM": name[0], "JBCL_NM": name[1]}]
            orders = [dosirak_type_dict[prev_dosirak]]
            await dosirak_service.delete_dosirak_order(user, post, people, orders)
            orders = [(dosirak_type_dict[dosirak], 1)]
            await dosirak_service.create_dosirak_order(user, post, people, orders)
        elif prev_dosirak in ['heat', 'warm', 'salad'] and dosirak in ['unclassified', 'trash']:
            name = data['name'].split(' ')
            people = [{"FLNM": name[0], "JBCL_NM": name[1]}]
            orders = [dosirak_type_dict[prev_dosirak]]
            await dosirak_service.delete_dosirak_order(user, post, people, orders)
    else:
        print(f"오류: prev_data={prev_data}, data={data}")
