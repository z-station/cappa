// solution statuses
var S_NONE = '0',
    S_UNLUCK = '1',
    S_PROGRESS = '2',
    S_SUCCESS = '3';
var S_WITH_SCORE = [S_PROGRESS, S_SUCCESS]

// manual statuses
var MS__NONE = '0',
    MS__READY_TO_CHECK = '1',
    MS__CHECK_IN_PROGRESS = '2',
    MS__CHECKED = '3';
var MS__AWAITING_CHECK = [MS__READY_TO_CHECK, MS__CHECK_IN_PROGRESS];


var tableFilter = {
    search: function(event){
        event.preventDefault()
        tableFilter.resetSearch()
        var searchStr = document.getElementById('js__search-input').value
        if(searchStr){
            var searchValues = searchStr.toLowerCase().split(',');
            document.querySelectorAll('.js__username').forEach(function(elem){
                for(let i=0; i < searchValues.length; i++){
                    var showElem = false
                    if(elem.textContent.toLowerCase().indexOf(searchValues[i].trim()) != -1 ){
                        showElem = true
                        break
                    }
                }
                if(!showElem){
                    elem.parentElement.style.display = "none";
                }
            })
        }
    },
    resetSearch: function(){
        document.querySelectorAll('.js__username').forEach(function(elem){
            elem.parentElement.style.display = "table-row";
        })
    }
}

var getLocalTime = function(strUtcDate) {
    var d = new Date(strUtcDate);
    var msecOffset = d.getTimezoneOffset() * -60000
    d.setTime(d.getTime() + msecOffset)
    var year = d.getFullYear()
    // zero indicates the first month of the year, then month = month + 1
    var month = d.getMonth() + 1
    var month = month.toString().length < 2 ? "0" + month : month
    var date = d.getDate().toString().length < 2 ? "0" + d.getDate().toString() :d.getDate()
    var hour = d.getHours().toString().length < 2 ? "0"+d.getHours().toString() :d.getHours()
    var minutes = d.getMinutes().toString().length < 2 ? "0"+d.getMinutes().toString() :d.getMinutes()
    return `${year}.${month}.${date} [${hour}:${minutes}]`
}

var groupCoursePage = function(e){
    var url = e.target.groupCourseSolutionsUrl
    $.get(url, function(response){
        for(const [member, val] of Object.entries(response)){
            var total_solved_tasks = 0;
            var total_score = 0;
            var userName = val.full_name
            var tr = document.querySelector('#js__' + member)
            for(const [taskitem, data] of Object.entries(val.data)){
                var td = tr.querySelector('.js__' + taskitem)
                if(td){
                    var lastModified = getLocalTime(data.last_modified)
                    var th = document.querySelector(td.getAttribute('data-th'))
                    var topicTitle = th.getAttribute('data-topic-title')
                    var taskitemTitle = th.getAttribute('data-taskitem-title')
                    var statusClass = 'status__' + data.status;
                    th.setAttribute('title', `${taskitemTitle}\nТема: ${topicTitle}`)
                    td.classList.add(statusClass)
                    if(data.is_count){
                        var title = `${userName}\n${lastModified}\n${taskitemTitle}\nТема: ${topicTitle}`
                    } else {
                        var title = `${userName}\n${lastModified}\n${taskitemTitle}\nТема: ${topicTitle}\nРешение вне зачета`
                    }
                    td.setAttribute('title', title)
                    if(val.show_link){
                        var content = document.createElement('a')
                        content.setAttribute('href', data.url)
                        content.setAttribute('target', '_blank')
                    } else {
                        var content = document.createElement('div')
                    }
                    switch(data.status){
                        case S_UNLUCK: content.innerHTML = '-'; break;
                        case S_PROGRESS: content.innerHTML = data.score; break;
                        case S_SUCCESS: content.innerHTML = '+'; break;
                    }
                    if(data.manual_check && MS__AWAITING_CHECK.indexOf(data.manual_check.status) != -1){
                        // Если решение на проверке добавить иконку
                        td.classList.add('awaiting-check');
                    } else if(data.status == S_NONE){
                        // Если решение начато - добавить иконку
                        td.classList.add('not-checked');
                    }
                    // если решение идет в зачет
                    if(data.is_count){
                        // если статус "решено"
                        if(data.status == S_SUCCESS) total_solved_tasks+=1;
                        // если статус с баллами (решено или в процессе)
                        if(S_WITH_SCORE.indexOf(data.status) != -1) total_score += data.score;
                    } else {
                        td.classList.add('not-count');
                    }
                    td.append(content)
                }
            }
            tr.querySelector('.js__total_solved_tasks').innerHTML = total_solved_tasks;
            tr.querySelector('.js__total_score').innerHTML = total_score.toFixed(1);
        }
        $(".js__tablesorter").tablesorter()
        document.querySelector('.js__loader').style.display = 'none';

    })

    $(".js__course__fake-table").width($(".js__course__table").width() + 20);

    $(".js__course__fake-table-container").scroll(function(){
        $(".js__course__table-container").scrollLeft($(".js__course__fake-table-container").scrollLeft());
    });
    $(".js__course__table-container").scroll(function(){
        $(".js__course__fake-table-container").scrollLeft($(".js__course__table-container").scrollLeft());
    });

    var searchForm = document.getElementById('js__search-form')
    searchForm && searchForm.addEventListener('submit', (event) => tableFilter.search(event))

}

window.addEventListener('groupCoursePageLoaded', groupCoursePage)