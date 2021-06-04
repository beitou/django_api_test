FROM harbor.xiaobangtouzi.com/base/python3-django:202105200926

WORKDIR /data

ADD . /data
#ADD api_automation_test /data/api_automation_test/
#ADD api_test /data/api_test/
#ADD frontend /data/
#ADD img	/data/
#ADD manage.py /data/
#ADD script_code_dir /data/

RUN pip3 install APScheduler xlwt
RUN cd /data/frontend &&  npm install && npm install node-sass && npm run build
EXPOSE 8000
CMD ["/data/manage.py" "runserver" "0.0.0.0:8000"]
