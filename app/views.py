from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic
from .forms import ScheduleForm
from .lib import TimeScheduleBS4
from .models import Schedule


class TimeSchedule(generic.CreateView):
    model = Schedule
    form_class = ScheduleForm
    success_url = reverse_lazy('app:index')
    template_name = 'app/index.html'

    def get_context_data(self, *args, **kwargs):
        schedules = Schedule.objects.order_by('start_time')
        time_schedule = TimeScheduleBS4(step=10, minute_height=0.5)
        context = super().get_context_data(*args, **kwargs)
        # テンプレートにhtmlを含んだ文字列を渡すときは、mark_safeをしておけばよい
        context['time_schedule'] = mark_safe(
            time_schedule.format_schedule(schedules)
        )
        return context
