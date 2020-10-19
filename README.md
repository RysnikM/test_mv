Сверстайте страницу по следующему шаблону:
https://www.figma.com/file/vX45ly0T2aeZQOdPU4yo34/OEE_details?node-id=1%3A9
Сверстать нужно на Vue.js. 

Запросы на REST для главного графика: 
http://185.6.25.155/api/basic_data/0/start_time/end_time
start_time, end_time в формате unitime
в параметры OEE, A, P, Q выводить последние полученные данные из предыдущего запроса.

реализовать возможность вывода 4 графиков с возможностью отключения любого из, выводом алерта, если график окажется пустым.
тип графика должен быть либо:
	* 
https://www.highcharts.com/demo/stock/step-line
	* 
https://www.highcharts.com/demo/stock/areaspline
	* 
https://www.highcharts.com/demo/box-plot
	* 
https://www.highcharts.com/demo/stock/line-markers




после этого сделайте pullrequest папки со своим ФИО в которую положите CV и код.


## ВНИМАНИЕ !!!!!
данное задание является тестовым и не рассматривается как ТЗ.
В случае, если вам недостаточно данных можете игнорировать их получение и подставлять статические.

---
Доступные запросы:

    'api/error_net/', данные по сети
    'api/current_messages/',  сообщения

    'api/top_stop_line/<int:id>/<int:start>/<int:end>/<int:smena>', ТОП 5 причин останоыки линии
    'api/time_status/<int:id>/<int:start>/<int:end>/<int:smena>',  времееные данные
    'api/basic_data/<int:id>/<int:start>/<int:end>/<int:smena>', данные по праметра OEE
    'api/data_a/<int:id>/<int:start>/<int:end>/<int:smena>', данные по праметра A
    'api/data_p/<int:id>/<int:start>/<int:end>/<int:smena>', данные по праметра P
    'api/data_q/<int:id>/<int:start>/<int:end>/<int:smena>', данные по праметра Q
    'api/table_oee/<int:id>/<int:start>/<int:end>/<int:smena>' - таблица данных ОЕЕ (A, P,Q,OEE)

ГДЕ
id - идентификатор линии (любое инт чисило)
start - начало периода UNIX
end - конец перилода UNIX
smena - 1 или 0 (если 1 выводи данные по текущей смене игнорируя временные интервалы, если 0 то выводит данные по временным интервалам)

addres: http://185.6.25.155/
