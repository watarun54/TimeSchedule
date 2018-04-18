from django import forms
from .models import Schedule


class ScheduleForm(forms.ModelForm):
    """Bootstrap4に対応するためのModelForm"""

    class Meta:
        # 各ウィジェットのclass名にform-contorlとつける
        model = Schedule
        fields = ('memo', 'start_time', 'end_time')
        widgets = {
            'memo': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'start_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def clean_end_time(self):
        """終了時間が開始時間より前だとエラーにする"""
        start_time = self.cleaned_data['start_time']
        end_time = self.cleaned_data['end_time']
        if end_time <= start_time:
            raise forms.ValidationError(
                '終了時間は、開始時間よりも後にしてください'
            )
        return end_time
