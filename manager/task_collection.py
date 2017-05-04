import threading
from global_setting.sqs import get_sqs_queue


class TaskCollection(object):
    # class represents all the task obj
    # this call is thread safe
    # only one thread can enter each fun
    tasks_obj_dic = {}

    def __init__(self):
        self.montiner = threading.Lock()

    def all_task_are_done(self):
        """
        check if all tasks are done
        :return: bool -> if all task are done 
        """
        with self.montiner:
            if len(self.tasks_obj_dic) == 0:
                return True
            else:
                return False

    def check_if_task_done(self):
        """
        check if there is a task done
        and there is send a done message
        and delete the task obj
        :return: None
        """
        with self.montiner:
            for pdf_task in self.tasks_obj_dic.values():
                if pdf_task.all_task_done():
                    queue = get_sqs_queue(pdf_task.job_id)
                    queue.send_message(MessageBody=pdf_task.get_summary_report())
                    # remove the done task from the task dic
                    self.tasks_obj_dic.pop(pdf_task.get_job_id())

    def add_new_task(self, task_id, new_task_obj):
        """
        add a new task obj to the collection
        :param task_id: string -> the task id
        :param new_task_obj: task_obj -> new task obj
        :return: None
        """
        with self.montiner:
            self.tasks_obj_dic[task_id] = new_task_obj

    def add_new_pdf_task_done(self, task_group_id, new_pdf_done_task):
        """
        add a new pdf done task to the task obj
        :param task_group_id: string -> task group id
        :param new_pdf_done_task: list -> list of the new pdf done
        :return: None
        """
        with self.montiner:
            self.tasks_obj_dic[task_group_id].add_new_done_message(new_pdf_done_task)