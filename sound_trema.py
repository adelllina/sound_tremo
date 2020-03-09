const uint8_t  pinSensor   = A0;                      // Номер вывода к которому подключён датчик звука (можно изменить на любой другой аналоговый вывод).
const uint16_t varVolume   = 10;                     // Минимальный уровень громкости (значение от 0 до 1023). Чем ниже значение, тем чувствительнее устройство.
const uint16_t varDuration = 2000;                    // Время, которое отводится на хлопки (в миллисекундах), за это время Вы должны успеть совершить максимальное количество хлопков.
const uint8_t  pinLED[3]  = {9, 6, 3};                // Номера выводов к которым подключены светодиоды (первый светодиод подключен к 9 выводу, второй к 6 и третий к 3). Можно указывать любые выводы.
const uint8_t  varLED[3]  = {2, 3, 4};                // Количество хлопков для реакции светодиодов (первый светодиод реагирует на 2 хлопка, второй на 3 и третий на 4). Можно указывать любое количество хлопков.
bool           flgLED[3]  = {0, 0, 0};                // Флаги состояния светодиодов (1-вкл / 0-выкл). Установленные в данной строке значения применяются при старте.
uint8_t        varSum;                                // Переменная для подсчёта количества хлопков за время varDuration.
uint32_t       varTimeOut;                            // Переменная для хранения времени завершения сессии хлопков.

void setup() {
  for (uint8_t i = 0; i < sizeof(pinLED); i++) {      // Проходим по всем выводам к которым подключены светодиоды ...
    pinMode      (pinLED[i], OUTPUT);                 // Конфигурируем вывод очередного светодиода как выход (OUTPUT).
    digitalWrite (pinLED[i], flgLED[i]);              // Устанавливаем на этом выводе состояние flgLED.
  }
}
void loop() {
  //Если зафиксирован хлопок:
  if (analogRead(pinSensor) > varVolume) {            // Если зафиксирован уровень звука выше значения varVolume, то ...
    //Считаем количество хлопков за время varDuration:
    varSum = 0;                                       // Сбрасываем счетчик количества хлопков.
    varTimeOut = millis() + varDuration;              // Определяем время завершения текущей сессии хлопков (текущее время + varDuration).
    while (varTimeOut > millis()) {                   // Уходим в цикл пока не наступит время завершения текущей сессии хлопков ...
      if (analogRead(pinSensor) > varVolume) {        // Если зафиксирован уровень звука выше значения varVolume, то ...
        while (analogRead(pinSensor) > varVolume) {   // Уходим в цикл ожидания завершения текущего хлопка.
          delay(50);                                  // Задержка delay(50) подавляет дребезг начала хлопка.
        }
        varSum++;                                     // Учитываем этот хлопок увеличивая значение varSum.
        delay(50);                                    // Задержка delay(50) подавляет дребезг окончания хлопка.
      }
    }
    // Время varDuration вышло, количество хлопков подсчитано и хранится в varSum, выполняем действия:
    for (uint8_t i = 0; i < sizeof(varLED); i++) {    // Проходим по всем лампам ...
      if (varSum == varLED[i]) {                      // Если количество хлопков varSum совпало со значением varLED одного из светодиодов, то ...
        flgLED[i] = ! flgLED[i];                      // Меняем состояние флага flgLED для этого светодиода.
        digitalWrite(pinLED[i], flgLED[i]);           // Устанавливаем логический уровень на выводе pinLED в соответствии со значением флага flgLED.
      }
    }
  }
  //  В этом месте можно написать свой код ...        // Этот код будет выполняться в то время, пока не фиксируются хлопки.
}