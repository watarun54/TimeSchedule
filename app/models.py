import datetime
from django.db import models


class Schedule(models.Model):
    """スケジュールモデル"""

    memo = models.TextField('メモ')
    start_time = models.TimeField('開始時間', default=datetime.time(0, 0, 0))
    end_time = models.TimeField('終了時間', default=datetime.time(0, 0, 0))

    def __str__(self):
        return self.memo
