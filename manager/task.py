import json


class Task(object):

    def __init__(self, task_list, job_id):
        self.task_list = task_list
        self.job_id = job_id
        self.message_done = []

    def add_new_done_message(self, new_message):
        self.message_done.append(new_message)

    def all_task_done(self):
        if len(self.task_list) == len(self.message_done):
            return True
        else:
            return False

    def get_summary_report(self):
        return json.dumps(self.message_done)

    def get_job_id(self):
            return self.job_id

    def update_task_list(self, task_list):
        self.task_list = task_list

