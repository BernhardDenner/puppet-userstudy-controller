#!/usr/bin/env python2.7


class Experiment(object):

    def __init__(self, group_name, user_name, tasks):
        self.group_name = group_name
        self.user_name = user_name
        self.tasks = tasks

        self.cnt_id = None
        self.current_task = None
        self.current_task_index = None

    def get_task_ids(self):
        ids = []
        for i in self.tasks:
            ids.append(i.id)
        return ids

    def get_current_task(self):
        return self.current_task

    def get_current_task_index(self):
        return self.current_task_index

    def get_number_of_tasks(self):
        return len(self.tasks)

    def get_expected_remaining_time(self):
        t = 0
        for i in range(self.current_task_index, len(self.tasks)):
            if self.tasks[i].duration != None:
                t += self.tasks[i].duration
        return t

    def set_current_task_id(self, task_id):
        i = 0
        new_task = None
        for t in self.tasks:
            if t.id == task_id:
                new_task = t
                break
            i += 1

        if new_task == None:
            raise NameError("task %s not found" % task_id)

        self.current_task = new_task
        self.current_task_index = i


    def next_task(self):
        try:
            if self.current_task == None:
                self.current_task_index = 0
                self.current_task = self.tasks[self.current_task_index]

            else:
                self.current_task_index += 1
                if self.current_task_index >= len(self.tasks):
                    self.current_task_index = None
                    self.current_task = None
                else:
                    self.current_task = self.tasks[self.current_task_index]
        except ValueError:
            self.current_task_index = None
            self.current_task = None

        return self.current_task


