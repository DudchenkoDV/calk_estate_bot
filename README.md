# calk_estate_bot
Здесь представлен бот оценки стоимости недвижимости. 
-----------------
Для запуска бота локально необходимо:
- скопировать репозиторий
- установить зависимости
- запустить API модели машшинного обучения командой:uvicorn main:model_application --reload
- запустить чат-бота: py bot.py

----------------
В качестве модели машинного обучения применена технология 
CatBoost - градиентный бустинг на основе деревьев решений.