# QR-Access
Приложение полностью разработано в рамках хакатона от Ростелеком - SuperHack.
Демонстрация работы: https://www.youtube.com/watch?v=eiPoCFeEga8
## Прототип сделан без сохранения сессий, доступные страницы:
**lab:**
- */doctor*   <-- для сессии лаборанта
- */admin*  <-- для сессии начальства лаборатории
- */superadmin*  <-- для сессии тех. специалистов лаборатории

**qr-platform:**
- */check*
- */admin*  <-- для сессии тех. специалистов платформы
## Запуск
Для корректной работы в lab/config_lab.py нужно изменить URL платформы
## Используемые технологии и фреймворки
 - *Flask* + *SQLAlchemy*
 - *Bootstrap 4*
 - *EdDSA* для подписи всех сообщений, отправляемых на платформу
##  Пример работы алгоритма подписи
![Диаграмма](https://i.imgur.com/q7UkBSh.png)
