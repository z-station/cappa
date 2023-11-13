
var getFormatedDateTime = function(d){
    var year = d.getFullYear()
    // zero indicates the first month of the year, then month = month + 1
    var month = d.getMonth() + 1;
    var month = month.toString().length < 2 ? "0" + month : month;
    var date = d.getDate().toString().length < 2 ? "0"+d.getDate().toString() :d.getDate()
    var hour = d.getHours().toString().length < 2 ? "0"+d.getHours().toString() :d.getHours()
    var minutes = d.getMinutes().toString().length < 2 ? "0"+d.getMinutes().toString() :d.getMinutes()
    return `${year}.${month}.${date} ${hour}:${minutes}`
}

var getLocalTime = function(strUtcDate) {

    // strUtcDate - строка, время в UTC, без указания часового пояса

    var d = new Date(strUtcDate);
    var msecOffset = d.getTimezoneOffset() * 60000 //  возвращает смещение часового пояса клиента относительно часового пояса UTC в миллисекундах
    d.setTime(d.getTime() - msecOffset) // устанавливает значение даты в часовом поясе клиента
    return d
}

/* Перевод серверного времени UTC в локальное время */
document.querySelectorAll('.js__utc-time').forEach(function(elem){
    var strUtcDate = elem.dataset.utcTime
    if (strUtcDate){
        d = getLocalTime(strUtcDate)
        elem.innerHTML = getFormatedDateTime(d);
    }
})
