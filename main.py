import os
from dotenv import load_dotenv
import asana
import datetime
import requests

load_dotenv()


key = os.environ["ASANA_AUTH"]
client = asana.Client.access_token(key)
project_id = 1202108478874368


def print_all_tasks():
    print("**All tasks**")
    tasks = client.tasks.find_by_project(project_id)
    for task in tasks:
        print(task)


def tasks_modified_since_yesterday():
    print("**Tasks modified since yesterday**")
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    params = {
        "project": project_id,
        "modified_since": yesterday,
        "opt_expand": ["memberships", "assignee"],
    }
    tasks = client.tasks.get_tasks(params, opt_pretty=True)
    for task in tasks:
        print(task)


def tasks_inprogress_since_yesterday():
    print("**Tasks unchanged since yesterday**")

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    allTasks = client.tasks.get_tasks(
        {"project": project_id, "opt_expand": ["memberships", "assignee"]},
        opt_pretty=True,
    )
    modTasks = client.tasks.get_tasks(
        {
            "project": project_id,
            "modified_since": yesterday,
            "opt_expand": ["memberships", "assignee"],
        },
        opt_pretty=True,
    )

    mod_list = list(modTasks)
    same_list = list(allTasks)
    two_days_ongoing = [];
    for i in range(len(same_list)):
        if same_list[i] not in mod_list:
            # print(same_list[i]['memberships'][0]['section']['name'])
            if same_list[i]['memberships'][0]['section']['name'] == 'In progress':
                two_days_ongoing.append((same_list[i]))

    return two_days_ongoing;






if __name__ == "__main__":
    tasks_inprogress_since_yesterday()
