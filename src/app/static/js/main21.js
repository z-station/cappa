// sidebar
var initSidebar = function(){
    var sidebarBtns = document.querySelectorAll('.js__sidebar-btn')
    sidebarBtns && sidebarBtns.forEach(function(elem){
        elem.addEventListener('click', function(e){
            e.target.classList.toggle("active")
            document.querySelector('.js__sidebar').classList.toggle("active")
        })
    })

    document.addEventListener('click', function(e) {
        var sidebar = document.querySelector('.js__sidebar')
        if(sidebar && !sidebar.contains(e.target)){
            sidebar.classList.remove("active")
            document.querySelectorAll('.js__sidebar-btn').forEach(function(e){
                e.classList.remove('active')
            })
        }
    })
}

var initTablesorter = function(){
    document.querySelectorAll(".js__tablesorter").forEach(function(table){
        $(table).tablesorter()
            .bind(
                'sortEnd filterEnd',
                function(e) {
                    /* Колонка с номерами строк не сортруется */
                    let i = 1;
                    $(".js__tablesorter").find("tr:gt(0)").each(function(){
                        $(this).find("td.js__tablesorter-number").text(i);
                        i++;
                    });
                }
            )
    })
}

var getFormatedDateTime = function(d){
    var year = d.getFullYear()
    var month = d.getMonth().toString().length < 2 ? "0"+ (d.getMonth() + 1) :d.getMonth() + 1
    var date = d.getDate().toString().length < 2 ? "0"+d.getDate().toString() :d.getDate()
    var hour = d.getHours().toString().length < 2 ? "0"+d.getHours().toString() :d.getHours()
    var minutes = d.getMinutes().toString().length < 2 ? "0"+d.getMinutes().toString() :d.getMinutes()
    return `${year}.${month}.${date} ${hour}:${minutes}`
}

document.querySelectorAll('.js__utc-timestamp').forEach(function(elem){
    var ts = elem.dataset.utcTimestamp;
    if (ts){
        ts = parseFloat(ts.replace(',', '.')) * 1000;
        d = new Date(ts)
        elem.innerHTML = getFormatedDateTime(d);
    }
})

/* Перевод серверного времени UTC в локальное время */
document.querySelectorAll('.js__utc-time').forEach(function(elem){
    var strUtcDate = elem.dataset.utcTime
    if (strUtcDate){
        d = new Date(strUtcDate);
        var msecOffset = d.getTimezoneOffset() * -60000;
        d.setTime(d.getTime() + msecOffset);
        elem.innerHTML = getFormatedDateTime(d);
    }
})

window.addEventListener('initSidebar', initSidebar)
window.addEventListener('initTablesorter', initTablesorter)