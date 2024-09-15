@echo off
REM Активируем виртуальное окружение
call venv\Scripts\activate

REM Запускаем приложение
python app.py

REM Программа завершена. Закрытие окна по завершению работы
pause
