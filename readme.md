Версия Debian: `11.7`
Версия ядра: `5.10.160-12-rk356x`

> **Для конкретной работы диагностики необходимо подключить к плате sd-карту с образом системы, оба ethernet-кабеля, монитор по HDMI, USB накопители (FAT32), USB mini (с data), замкнуть RS232 (TX/RX), замкнуть обе CAN шины .**
{.is-warning}

![nms-sm-evm-v1_conn_top.jpg](/oiid/nms-sm-evm-v1_conn_top.jpg)

`X8`, `X7` - подключить ethernet
`X11` - подключить 2 флешки в FAT32 формате
`X10`, `X17` - соединить через USB mini
`X18` - замкнуть TX с RX
`X15`, `X16` - замкнуть 2 шины

После старта системы автоматически выполняется диагностика: 
- `network.py` - проверяет сетевые интерфейсы, определяя их IP-адреса и выполняя тестовую отправку ping-запросов для диагностики их доступности.
- `usb.py` - выполняет диагностику USB-устройств, проверяя их доступность, монтирование, а также скорость чтения и записи тестовых файлов на указанные точки монтирования.
- `can.py` - настраивает два CAN-интерфейса на 500Кбит/c, отправляет тестовые пакеты по одному каналу и принимает их на другом.
- `i2c.py` - проверяет доступные девайсы на шине с помощью утилиты `i2cdetect`
  Должны быть инициализированы следующее устройства: 
  ```
  root@nms-sm-rk3568:/opt/rk3568_test/src# i2cdetect -l
  i2c-3   i2c             rk3x-i2c                                I2C adapter
  i2c-6   i2c             DP-AUX                                  I2C adapter
  i2c-4   i2c             rk3x-i2c                                I2C adapter
  i2c-0   i2c             rk3x-i2c                                I2C adapter
  i2c-7   i2c             DesignWare HDMI                         I2C adapter
  i2c-5   i2c             rk3x-i2c                                I2C adapter
  ```
  
  - `rtc.py` - Скрипт читает с устройства `/dev/rtc1`  таймштамп с помощью команды

  ```
  hwclock --show --rtc /dev/rtc1
  ```

  Если вывод пустой - тест не пройден. 

  - `rs232.py` - RX и TX на порту должны быть замкнуты, скрипт отправляет и читает тестовые данные на порт.

	- `console.py` - Проверка работы USB консоли
  
  - `gpio.py` - Проверка работы GPIO с 20 по 63 порт (Экспорт, запись в высокий/низкий уровень, чтение, перевод в спящий режим)

  - `watchdog_test()` - Функция предназначена для проверки функциональности /dev/watchdog. В ходе тестирования главный класс `main` фиксирует результаты в файл `result.log`. При активации функции `watchdog_test` активирует сторожевой таймер через `cat /dev/watchdog`. После перезагрузки main() сначала проверяет доступность `result.log`. Если он существует - выводит содержимое result.log, после удаляет.
  
Полный цикл тестирования состоит из двух этапов: 
1) Модульное тестирование, перезагрузка через триггер вачдога (до 3 минут)
2) Вывод результатов (до 2 минут)
  
### Пример успешного выполнения диагностики:

```
2024-12-17 13:24:20,007 - INFO - Network    [OK]
2024-12-17 13:24:20,008 - INFO - USB        [OK]
2024-12-17 13:24:20,008 - INFO - CAN        [OK]
2024-12-17 13:24:20,009 - INFO - I2C        [OK]
2024-12-17 13:24:20,010 - INFO - RTC        [OK]
2024-12-17 13:24:20,010 - INFO - GPIO       [OK]
2024-12-17 13:24:20,010 - INFO - RS232      [OK]
2024-12-17 13:24:20,010 - INFO - Console    [OK]
2024-12-17 13:24:20,011 - INFO - Watchdog   [OK]
```
При обнаружении ошибки возможен следующий результат:
```
2024-12-14 15:15:32.546 - ERROR - Error getting IP for eth: list of index out of range
...
2024-12-14 15:15:56.331 - ERROR - Network tests failed.
```
Вывод: 
Не все ethernet кабели подключены к плате или инициализированы при старте

> Записать новую sd карту можно с помощью BalenaEtcher(Linux) или Rufus(Windows) на SD карту, объемом не менее 16ГБ
{.is-info}

Выключение платы следует делать после полного отключения системы с помощью кнопки `PWR BTN`

![nms.png](/oiid/nms.png)
