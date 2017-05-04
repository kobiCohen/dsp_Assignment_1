import json


class Task(object):
    # a class represents a task from the worker

    def __init__(self, task_list, job_id):
        """
        this is init the task file
        :param task_list: list -> list include all the tasks
        :param job_id: string -> the job id
        """
        self.task_list = task_list
        self.job_id = job_id
        self.message_done = []

    def add_new_done_message(self, new_message):
        """
        add new tone task
        :param new_message: list -> the result return from the worker
        :return: None
        """
        self.message_done.append(new_message)

    def all_task_done(self):
        """
        check if all pdf task are done
        :return: bool -> true if all task done or false
        """
        if len(self.task_list) == len(self.message_done):
            return True
        else:
            return False

    def get_summary_report(self):
        """
        create the summery report
        :return: string -> json represents the summary report
        """
        return json.dumps(self.message_done)

    def get_job_id(self):
        """
        get the job id
        :return: int -> job id
        """
        return self.job_id

    def update_task_list(self, task_list):
        self.task_list = task_list

