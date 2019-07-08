from django_cron import CronJobBase, Schedule


class TestCron(CronJobBase):
    RUN_EVERY_MINS = 60
    MIN_NUM_FAILURES = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'test_cron'

    def do(self):
        # do something here
        pass
