"""スケジュールを作成するためのモジュールです。"""
import datetime


class TimeScheduleBS4:
    """タイムスケジュールを作成する(Bootstrap4)."""

    def __init__(
        self, minute_height=1, hours=None, schedule_color='bg-info', step=1
    ):
        """初期化.
        引数:
        minute_height: 1分の高さ(px)。1ならば1時間が60px、全体で1440px
        hours: スケジュールに記載する時間の幅。range(6, 13)だと6〜12時まで
        schedule_color: スケジュールがある場合の背景色
        step: 何分毎にdivタグを入れるか。デフォルトは1分毎に1divタグ
              1に近いほどdivタグが多くなりパフォーマンスが落ちるが、細かい時間
              でも色をつけることができる
        """
        # hoursがNoneなら0から23時で
        if hours is None:
            self.hours = [x for x in range(24)]
        else:
            self.hours = hours
        self.step = step
        self.minute_height = minute_height
        self.hour_height = self.minute_height * 60
        self.max_height = self.hour_height * len(self.hours)
        self.schedule_color = schedule_color

    def convert(self, obj):
        """(開始時間、終了時間、スケジュールテキスト)のタプルを返す.
        format_schedueメソッドに渡した各scheduleオブジェクトを
        (開始時間, 終了時間,テキスト)の形に変換するためのメソッド
        return obj.start, obj.end, obj.text
        return obj['start'], obj['end'], obj['title']+obj['text']
        のようにしてください
        """
        message = '{}〜{}<br>{}'.format(
            obj.start_time, obj.end_time, obj.memo
        )
        return obj.start_time, obj.end_time, message

    def format_hour_name(self, hour):
        """左側の列、時間表示部分の作成."""
        div = '<div style="height:{0}px;" class="hour-name">{1}:00</div>'
        return div.format(self.hour_height, hour)

    def format_minute(self, schedule, now):
        """分部分の作成."""
        start, end, text = self.convert(schedule)
        context = {
            'color': self.schedule_color,
            'height': self.minute_height * self.step,
            'just-hour': '',
            'text': text,
        }
        # 1:00、2:00などの0分に枠線を入れるためのcss
        if now.minute == 0:
            context['just-hour'] = 'just-hour'

        # 現在ループの時間が開始時間〜終了時間内なら、色をつける
        if start <= now < end:

            # 既にtooltipを入れているなら背景色だけ
            if self.already_tooltip:
                base_html = (
                    '<div class="{color} {just-hour}" '
                    'style="height:{height}px;"></div>'
                )

            # 最初の予定なら、tooltipをつけてフラグをTrueに
            else:
                self.already_tooltip = True
                base_html = (
                    '<div class="{color} {just-hour}" '
                    'style="height:{height}px;" '
                    'data-html="true" title="{text}" data-placement="top" '
                    'data-trigger="manual"  data-toggle="tooltip">'
                    '</div>'
                )

        else:
            base_html = (
                '<div class="{just-hour}" style="height:{height}px;"></div>'
            )

        return base_html.format(**context)

    def format_schedule(self, schedules):
        """タイムスケジュールを作成する."""
        v = []
        a = v.append
        a('<div class="row no-gutters">')

        # 左列、時間表示部分の作成
        a('<div class="col" style="height:{0}px;">'.format(self.max_height))
        for hour in self.hours:
            a(self.format_hour_name(hour))
        a('</div>')

        # 右列、スケジュール作成部分
        for schedule in schedules:
            # 予定の最初のdivタグにtooltipを導入するためのフラグ
            self.already_tooltip = False
            a('<div class="col minute-wrapper" style="height:{0}px;">'.format(
                self.max_height
            ))
            for hour in self.hours:
                for minute in range(0, 60, self.step):
                    now = datetime.time(hour=hour, minute=minute)
                    a(self.format_minute(schedule, now))
            a('</div>')

        a('</div>')

        return ''.join(v)
