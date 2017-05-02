import threading
from global_setting.sqs import get_sqs_queue , done_task
import json

class TaskCollection(object):
    tasks_obj_dic = {}

    def __init__(self):
        self.montiner = threading.Lock()

    def all_task_are_done(self):
        with self.montiner:
            if len(self.tasks_obj_dic) == 0:
                return True
            else:
                return False

    def check_if_task_done(self, taksks):
        with self.montiner:
            for pdf_task in self.tasks_obj_dic.values():
                if pdf_task.all_task_done():
                    queue = get_sqs_queue(pdf_task.job_id)
                    done_string = json.dumps(taksks)
                    queue.send_message(MessageBody=done_string)

                    queue2 = get_sqs_queue("done_task")
                    done_task.send_message(Message_body=taksks )
                    # remove the done task from the task dic
                    self.tasks_obj_dic.pop(pdf_task.get_job_id())

    def add_new_task(self, task_id, new_task_obj):
        with self.montiner:
            self.tasks_obj_dic[task_id] = new_task_obj

    def add_new_pdf_task_done(self, task_group_id, new_pdf_done_task):
        with self.montiner:
            self.tasks_obj_dic[task_group_id].add_new_done_message(new_pdf_done_task)