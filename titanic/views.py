import pandas as pd
from .forms import DataPeopleForm
import joblib
from django.shortcuts import render, redirect


# Загрузка модели из файла
loaded_model = joblib.load('model.joblib')


def titanic_data(request):
    # Создаём экземпляр класса формы.
    form = DataPeopleForm()
    # Добавляем его в словарь контекста под ключом form:
    context = {'form': form}
    # Указываем нужный шаблон и передаём в него словарь контекста.
    return render(request, 't.html', context)


def predict(request):
    if request.method == 'POST':
        # Получение данных из формы
        gender = 1 if request.POST.get('gender') == 'male' else 0
        marital_status = request.POST.get('marital_status')
        age = int(request.POST.get('age'))
        with_parents = 1 if request.POST.get('with_parents') else 0
        with_siblings = 1 if request.POST.get('with_siblings') else 0
        ticket_class = int(request.POST.get('ticket_class'))

        data = pd.DataFrame({
            'Sex': [gender],
            'Age': [age],
            'Pclass_1': [1 if ticket_class == 1 else 0],
            'Pclass_2': [1 if ticket_class == 2 else 0],
            'Pclass_3': [1 if ticket_class == 3 else 0],
            'Gender_Boy': [1 if gender == 1 and age < 18 else 0],
            'Gender_Girl': [1 if gender == 0 and age < 18 else 0],
            'Gender_Man': [1 if gender == 1 and age >= 18 else 0],
            'Gender_Woman': [1 if gender == 0 and age >= 18 else 0],
            'Title_Miss': [1 if gender == 0
                           and marital_status == 'single' else 0],
            'Title_Mr': [1 if gender == 1 else 0],
            'Title_Mrs': [1 if gender == 0
                          and marital_status == 'married' else 0],
            'Title_Other': [0],
            'SibSp_Binary': [1 if with_parents else 0],
            'Parch_Binary': [1 if with_siblings else 0]
        })

        prediction = loaded_model.predict(data)[0]
        return render(request, 'result.html', {'prediction': prediction})
    return redirect('titanic_data')
