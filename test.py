import webbrowser

while True:
    answer = input('Слушаю...\n').lower()
    if answer in ('привет','здравствуй', 'hello', ' hi'):
        print('Приветствую')

    elif answer in ('пока','bye', 'stop'):
        print('Всего хорошего')

    elif answer in ('как дела','как сам','как ты'):
        print('Хорошо, насколько это возможно для бота')
        break
    elif answer in ('открой браузер','ютуб','давай посмотрим что нибудь','мне скучно'):
        print('Выполняю...')
        webbrowser.open_new_tab('https://www.youtube.com/')
    else:
        print('Я ничего не понял я просто глупый')