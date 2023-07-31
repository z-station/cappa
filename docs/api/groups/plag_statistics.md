## Получить статистику плагиата по курсу для учебной группы


### Права доступа
- Аутентифицированный пользователь.
- Пользователь является преподавателем учебной группы.

### Формат запроса:
**HTTP-метод:** GET   
**URL:** ```/api/groups/<group_id:int>/plag-statistics?course_id=<course_id:int>```  

**Параметры запроса:**
- group_id - id учебной группы
- course_id - id учебного курса


### Формат ответа:

**HTTP-статус ответа:** 200   
**Состояние:** Запрос завершен успешно.  
**Тело ответа:**
```
{
    user_id_1: {
        taskitem_id_1: {
           percent: float,
           datetime: str,
           reference: ?{
               id: int,
               solution_type: str,
               solution_id: int
           },
           candidate: ?{
               id: int,
               solution_type: str,
               solution_id: int
           }
        },
        taskitem_id_2: {...},
        taskitem_id_N: {...}
    },
    user_id_2: {...},
    user_id_N: {...}
}
```
- user_id - id пользователя группы
- taskitem_id - id задачи курса, по которой представлена статистика
- percent - значение плагиата от 0 до 100. Если percent = 0 то candidate = None
- datetime - дата проверки на плагиат
- reference - данные искомого проверяемого решения
- reference.id - id пользователя
- reference.solution_type - [тип решения](../constants.md)
- reference.solution_id - id искомого решения
- candidate - данные решения с наибольшим плагиатом
- reference.id - id пользователя с наибольшим плагиатом
- reference.solution_type - [тип решения](../constants.md)
- reference.solution_id - id плагиатного решения

- **Пример ответа:**
```
{
    "872": {
        "134": {
            "percent": 0.93,
            "datetime": "2023-07-31T09:57:13.246057Z",
            "candidate": {
                "id": 864,
                "solution_id": 80624,
                "solution_type": "course"
            },
            "reference": {
                "id": 872,
                "solution_id": 85424,
                "solution_type": "course"
            }
        }
    }
}
```

**HTTP-статус ответа:** 404
**Состояние:** Курс не найден.