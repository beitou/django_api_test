import time
import threading
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from api_test.common.auto_test import automation_task

job_defaults = {
    'coalesce': False,
    'max_instances': 5,
    'misfire_grace_time': 60
}
scheduler = BackgroundScheduler(job_defaults=job_defaults)

def func(project,schedule_id,task_name):
    automation_task(project,schedule_id)
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func  time :',ts)



def do_with_timing(project,schedule_id,start_date,task_name):
    scheduler.add_job(func,args=(project,schedule_id,task_name), trigger='date', run_date=start_date,id=task_name)

def do_with_loop(project,schedule_id,start_date,end_date,unit,frequency,task_name):
    if unit=='m':
        scheduler.add_job(func,args=(project,schedule_id,task_name),trigger = 'interval', minutes=frequency,start_date=start_date,
                          end_date=end_date,id=task_name)
    elif unit=='h':
        scheduler.add_job(func, args=(project, schedule_id,task_name), trigger='interval', hours=frequency,
                          start_date=start_date,
                          end_date=end_date,id=task_name)
    elif unit == 'd':
        scheduler.add_job(func, args=(project, schedule_id,task_name), trigger='interval', days=frequency,
                          start_date=start_date,
                          end_date=end_date,id=task_name)
    elif unit == 'w':
        scheduler.add_job(func, args=(project, schedule_id,task_name), trigger='interval', weeks=frequency,
                          start_date=start_date,
                          end_date=end_date,id=task_name)
    else:
        return "错误的时间单位"
    #
    # scheduler.add_job(func, 'interval', minutes=1, start_date='2020-05-13 23:15:00',
    #                   end_date='2020-05-13 23:17:00')
    #
    # scheduler.add_job(func, 'interval', hours=1, start_date='2020-05-13 22:42:00',
    #                   end_date='2020-05-13 22:43:00')
    #
    # scheduler.add_job(func, 'cron', day='*', hour=23, minute=19, start_date='2020-05-13 23:18:00',
    #                   end_date='2020-05-13 23:43:00')   ##每2天执行
    #
    # scheduler.add_job(func, 'cron', week='*',  hour=23, minute=22,start_date='2020-05-13 23:20:00',
    #                   end_date='2020-06-13 23:43:00')  ##每周执行


def add_jobs(loop_timing,project,schedule_id,start_date,task_name,end_date=None,unit='d',frequency=1):
    if not scheduler.running:
        scheduler.start()
    # 如果任务存在，那么把任务移除，重新添加
    if scheduler.get_job(task_name)!= None:
        scheduler.remove_job(task_name)
    if loop_timing=='circulation':
        do_with_loop(project,schedule_id,start_date,end_date,unit,frequency,task_name)
    elif loop_timing=='timing':
        do_with_timing(project,schedule_id,start_date,task_name)
    else:
        return "不期望的执行方式，仅支持循环执行或定时执行"

    print(scheduler.get_jobs())
    # while (True):
    #     print('main 1s')
    #     time.sleep(1)
    #     if len(scheduler.get_jobs()) == 0:
    #         break

