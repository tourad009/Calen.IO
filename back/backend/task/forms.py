from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'end_date', 'completed', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le titre de la tâche',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez une description (facultatif)',
                'rows': 4,
                'required': False,
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Date et heure de début',
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'placeholder': 'Date et heure de fin',
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez une priorité',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get('due_date')
        end_date = cleaned_data.get('end_date')

        if due_date and end_date and due_date > end_date:
            raise forms.ValidationError(
                "La date de début doit être antérieure à la date de fin."
            )
        return cleaned_data
