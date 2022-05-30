import asyncio
import requests
from isdayoff import DateType, ProdCalendar
from datetime import date, timedelta


class Bitrix24:

    def __init__(self, url, data):
        self.url = url
        self.data = data
        self.calendar = ProdCalendar(locale='ru')
        self.loop = None
        self.date_today = date.today()
        self.old_day = None

    def run(self):
        while True:
            self.date_today = date.today()
            if self.old_day != self.date_today:
                self.loop = asyncio.get_event_loop()
                self.loop.create_task(self.check_days())
                self.loop.run_forever()

    def add_task(self):
        request = requests.post(self.url + 'tasks.task.add', json=self.data)
        return request.json()

    async def check_days(self):
        self.old_day = self.date_today
        if await self.calendar.date(self.date_today + timedelta(3)) == DateType.NOT_WORKING:
            print(self.add_task())
            self.loop.stop()
        else:
            self.loop.stop()


data_for = {'fields': {'TITLE': 'Новая задача',
                       'RESPONSIBLE_ID': 1,
                       'DESCRIPTION': 'Описание новой задачи'}}
bitrix = Bitrix24(url='https://b24-ogfxda.bitrix24.ru/rest/1/m2jcj9ckcsdjjcy9/', data=data_for)
bitrix.run()

