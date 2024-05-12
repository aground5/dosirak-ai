import datetime
from datetime import date, timedelta

korean_weekday = ['월', '화', '수', '목', '금', '토', '일']


def get_next_workday():
    today = date.today()
    weekday = today.weekday()

    # If today is Friday (weekday == 4), add 3 days to get to Monday
    if weekday == 4:
        return today + timedelta(days=3)
    # If today is Saturday (weekday == 5), add 2 days
    elif weekday == 5:
        return today + timedelta(days=2)
    # Otherwise, add 1 day to get to the next weekday
    else:
        return today + timedelta(days=1)


def get_recent_workday():
    today = date.today()
    weekday = today.weekday()

    # If today is Sunday (weekday == 6), subtract 2 days to get to Friday
    if weekday == 6:
        return today - timedelta(days=2)
    # If today is Saturday (weekday == 5), subtract 1 day
    elif weekday == 5:
        return today - timedelta(days=1)
    # Otherwise, today is the most recent workday
    else:
        return today


def format_date(dt: datetime.datetime):
    return f"{dt.strftime('%-m/%d')}({korean_weekday[dt.weekday()]})"


def parse_date_from_title(post_title):
    current_year = datetime.datetime.now().year
    end = post_title.find("(")
    post_text_date = post_title[:end]
    post_date = datetime.datetime.strptime(f"{post_text_date}/{current_year}", "%m/%d/%Y").date()
    return post_date


if __name__ == "__main__":
    next_workday = get_next_workday()
    print(next_workday.month)
    print(next_workday.weekday())
    print(next_workday.strftime("%Y-%-m-%d %A"))
    recent_workday = get_recent_workday()
    print(recent_workday.month)
    print(recent_workday.weekday())
    print(recent_workday.strftime("%Y-%m-%d %A"))
