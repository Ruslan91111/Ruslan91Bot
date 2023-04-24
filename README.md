Телеграм бот, написанный на языке Python при помощи библиотеки aiogram. Начало работы с ботом - команда "/start". После старта выводится меню из трех пунктов: 1) '/Узнать_погоду'); 2) '/Конвертировать_валюту'); 3) '/Показать_милого_котенка').

При нажатии '/Узнать_погоду' предлагается ввести название города. После ввода и подтверждения города, выводится текущая погода в указанном населенном пункте. После введения наименования города – данное наименование передается в функцию, которая обращается по API-ключу к приложению: «OpenWeatherMap», из результата формируется строка ответа, которая выводится в чате бота.

При нажатии '/Конвертировать_валюту' предлагается ввести наименование первой валюты, затем ввести наименование второй валюты, затем сумму, которую необходимо конвертировать. Указанные значения сохраняются в словарь, который передается в функцию, которая обращается по API-ключу к приложению: «Excangerate», где получает существующий курс и производит необходимые расчеты,  результат формируется в виде строки ответа, которая выводится в чате бота.

«/Узнать_погоду» и «/Конвертировать_валюту» реализованы через машину состояний.

При выборе '/Показать_милого_котенка' осуществляется запрос к API «https://api.thecatapi.com/v1/images/search», который предоставляет случайную картинку котика, которая и передается в чат.

Команда «/Создать_опрос» предназначена только для админа бота, то есть меня, при создании опроса проверяется ID, мой ID сохранен в отдельном файле «config.py». При нажатии команды  «/Создать_опрос» в машину состояний сохраняется вопрос и четыре варианта ответа, по заполнении которых, опрос и варианты ответа, передаются в группу, в которой бот указан в качестве администратора.

bot_telegram.py — содержит основной код, в том числе создание бота, диспетчера и работу с пользователем через состояния.

get_by_api.py — содержит три функции, посредством, которых происходит обращение к сторонним приложениям по API.

Keyboard.py — cодержит клавиши и клавиатуру.