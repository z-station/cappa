## Получить статистику решений по курсу для текущего пользователя

### Права доступа
- Аутентифицированный пользователь.
- Пользователь имеет доступ к учебному курсу.

### Формат запроса:
**HTTP-метод:** GET   
**URL:** ```/api/training/courses/<course_id:int>/statistics/```  

**Параметры запроса:**
- course_id - id учебного курса

### Формат ответа:

**HTTP-статус ответа:** 200   
**Состояние:** Запрос завершен успешно.  
**Тело ответа:**
```
{
    taskitem_id_1: {
        id: int,
        created: str,
        translator: str,
        score_method: str,
        max_score: str,
        review_score: int|null,
        review_status: str|null,
        testing_score: str|null,
        due_date: str|null
    },
    taskitem_id_2: {...},
    taskitem_id_N: {...}
  }
}
```
- taskitem_id - id задачи учебного курса
- id - id последнего решения пользователя по задаче по задаче курса  
- created - utc дата создания решения  
- translator - id транслятора языка программирования  
- score_method - код [оценочного метода](../constants.md)
- max_score - максимальный балл за решение задачи
- review_score - оценка преподавателя 
- review_status - статус проверки решения преподавателем (для ручного метода проверки)
- testing_score - оценка на основании тестов
- due_date - дата сдачи решения

**Пример ответа:**
```
{
    "130": {
        "id": 24337,
        "created": "2019-11-23T22:21:02.273068+00:00",
        "due_date": null,
        "max_score": 5,
        "translator": "GCC7.4",
        "review_score": null,
        "score_method": "tests",
        "review_status": null,
        "testing_score": 0
    }
}
```

**HTTP-статус ответа:** 400    
**Состояние:** Ошибка валидации. Тело запроса не соответствует спецификации.  
