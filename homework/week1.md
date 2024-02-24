# Проектирование

В [week0](https://github.com/BrittleFoot/async-architecture/blob/main/homework/week0.md) описал более детально мысленный процесс,
здесь приведу финальные результаты, особенно ES объединенный по поддоменам.

![image](https://github.com/BrittleFoot/async-architecture/assets/14301123/791485d3-1147-4caa-9369-cc973ff84451)


## Буря событий и домены

<img width="1024" alt="es-domain-model" src="https://github.com/BrittleFoot/async-architecture/assets/14301123/25d75436-62b5-46bc-9ac4-7eef4d9e1c33">

## Модель Данных

<img width="1024" alt="data-model" src="https://github.com/BrittleFoot/async-architecture/assets/14301123/8273aa98-6c61-4be4-ad18-c9e15b24748c">

## Разделение на сервисы

<img width="1024" alt="services" src="https://github.com/BrittleFoot/async-architecture/assets/14301123/dbacfaba-7ea2-4264-817b-14d1ed4f97b7">


# События

<img width="400" alt="events" src="https://github.com/BrittleFoot/async-architecture/assets/14301123/61b3af4b-6dd6-41ec-9a0b-f23f84e6ce1f">


У нас есть 3 сервиса которые будут общаться событиями

- auth
- tracker
- billing

Ниже, при описании, буду использовать нотацию `x -> y, z` для обозначения, что `x` отправляет событие, а `y, z` его читают.

## Бизнес события

  - DAY END `billing`
  - REASSIGN `tracker`

<img width="400" alt="business" src="https://github.com/BrittleFoot/async-architecture/assets/14301123/1d786f5f-4f15-43fa-a285-bc618c88ae03">


## CUD события

  - Account `auth -> tracker, billing`
    - Created
    - Updated (info, roles changed)
    - Deleted
    
  - Task `tacker -> billing`
    - Created
    - Performer Assigned
    - Task Done

<img width="400" alt="cud" src="https://github.com/BrittleFoot/async-architecture/assets/14301123/0f4dbfba-bf37-4b66-890b-16e3ae6f715f">

## И на этом мы переходим к неделе №2

![image](https://github.com/BrittleFoot/async-architecture/assets/14301123/498d3188-0945-46de-a01e-1e70a6de1e9d)

