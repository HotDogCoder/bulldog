from django import forms
from .models import Report, ReportType, ReportScreenshot

class ReportForm(forms.ModelForm):

    report_type = forms.ModelChoiceField(
        queryset=ReportType.custom_objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='id',
        label='Report Type',
        help_text='Select report type',
        error_messages={
            'required': 'Please select a report type',
        },
    )

    class Meta:
        model = Report
        exclude = ('created_at',)


class ReportTypeForm(forms.ModelForm):

    class Meta:
        model = ReportType
        exclude = ('created_at',)


class ReportScreenshotForm(forms.ModelForm):

    report_type = forms.ModelChoiceField(
        queryset=ReportType.custom_objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='id',
        label='Report Type',
        help_text='Select report type',
        error_messages={
            'required': 'Please select a report type',
        },
    )

    report = forms.ModelChoiceField(
        queryset=Report.custom_objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='id',
        label='Report',
        help_text='Select report',
        error_messages={
            'required': 'Please select a report',
        },
    )

    class Meta:
        model = ReportScreenshot
        exclude = ('created_at',)
