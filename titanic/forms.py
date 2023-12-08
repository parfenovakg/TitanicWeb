from django import forms


class DataPeopleForm(forms.Form):
    GENDER_CHOICES = [('male', 'Мужской'), ('female', 'Женский')]
    MARITAL_STATUS_CHOICES = [('single', 'Холост(а)'),
                              ('married', 'В браке')]

    gender = forms.ChoiceField(label='Ваш пол', choices=GENDER_CHOICES,
                               widget=forms.RadioSelect)
    marital_status = forms.ChoiceField(label='Ваше семейное положение',
                                       choices=MARITAL_STATUS_CHOICES,
                                       widget=forms.RadioSelect)
    age = forms.IntegerField(label='Возраст', min_value=1, max_value=100)
    with_parents = forms.BooleanField(label='Обычно вы путешествуете'
                                      ' с родителями/детьми?', required=False)
    with_siblings = forms.BooleanField(label='Обычно вы путешествуете с'
                                       ' партнером/братьями/сестрами?',
                                       required=False)
    ticket_class = forms.ChoiceField(label='Билеты какого класса '
                                     'Вы обычно берете в путешествия?',
                                     choices=[(1, 'Премиум'), (2, 'Средний'),
                                              (3, 'Эконом')])

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 1 or age > 100:
            raise forms.ValidationError('Введите корректный возраст'
                                        '(от 1 до 100 лет).')
        return age
