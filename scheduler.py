import json
import os
import config


class Scheduler:

    def __init__(self):
        self.schedule = self.get_schedule_file()

    def get_schedule_file(self):
        self.make_schedule_file()
        with open(config.SCHEDULE, 'r') as f:
            schedule = json.load(f)

        return schedule

    def make_schedule_file(self):
        if not os.path.exists(config.SCHEDULE):
            print('Creating new schedule file...')
            with open(config.SCHEDULE, 'w') as f:
                json.dump([], f)

    def get_schedule_for_post(self, image_name):
        schedules = self.get_schedule_file()
        for schedule in schedules:
            if schedule['photo'].split('/')[-1] == image_name:
                return schedule

    def remove_schedule_for_post(self, image_name):
        schedules = self.get_schedule_file()
        new_schedule = [schedule for schedule in schedules if schedule['photo'].split('\\')[-1] != image_name]
        self.write_schedule(new_schedule)


    def write_schedule_for_post(self, image_name, description):
        schedules = self.get_schedule_file()
        schedules.append(self.make_schedule(image_name, description))
        self.write_schedule(schedules)

    def write_schedule(self, schedule):
        print(f'Upserting schedule with: {schedule}')
        with open(config.SCHEDULE, 'w') as schedule_file:
            json.dump(schedule, schedule_file)

    def make_schedule(self, image_name, description):
        return {
            'photo': os.path.normpath(config.POSTS_DIR + '/' + image_name),
            'description': description
        }
