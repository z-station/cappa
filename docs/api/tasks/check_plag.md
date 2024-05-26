 ## Проверить решение на плагиат
 
### Права доступа
- Аутентифицированный пользователь.
- Пользователь преподаватель

### Формат запроса:
**HTTP-метод:** POST  
**URL:** ```/api/tasks/taskitem/<taskitem_id:int>/check-plag/```  
**Тело запроса:**
```
{
   reference_user_id: int,
   candidates: [int]
}
```
**Параметры запроса:**
- reference_user_id - id пользователя, чье решение проверяется
- candidates - список id пользователей, с решениями которых нужно сравнить искомое на плагиат. Для сравнения берется последнее решение по задаче

### Формат ответа:

**HTTP-статус ответа:** 200  
**Состояние:** Запрос завершен успешно.  
**Тело ответа:**
```
{
    "percent": float,
    "datetime": str,
    "reference": {
        "id": int,
        "solution_type": str,
        "solution_id": int
    },
    "candidate": ?{
        "id": int,
        "solution_type": str,
        "solution_id": int
    }
}
```
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
    "percent": 0.92,
    "datetime": "2023-07-31T09:57:11.843925Z",
    "reference": {
        "id": 872,
        "solution_type": "course",
        "solution_id": 85487
    },
    "candidate": {
        "id": "884",
        "solution_type": "external",
        "solution_id": "83266"
    }
}
```

**HTTP-статус ответа:** 204    
**Состояние:** Искомое решение не найдено или пустое.

**HTTP-статус ответа:** 400    
**Состояние:** Ошибка валидации. Тело запроса не соответствует спецификации.  

**HTTP-статус ответа:** 500    
**Состояние:** Решение не может быть проверено на плагиат, например сервис недоступен или не поддерживается язык (Доступные python, java, c++).  
