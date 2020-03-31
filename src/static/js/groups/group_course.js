// solution statuses
var S_NONE = '0',
    S_UNLUCK = '1',
    S_PROGRESS = '2',
    S_SUCCESS = '3';
var S_WITH_SCORE = [S_PROGRESS, S_SUCCESS]

// manual statuses
var MS__NOT_CHECKED = '0',
    MS__READY_TO_CHECK = '1',
    MS__CHECK_IN_PROGRESS = '2',
    MS__CHECKED = '3';
var MS__AWAITING_CHECK = [MS__READY_TO_CHECK, MS__CHECK_IN_PROGRESS];

var getFormatedDateTime = function(strDate) {
    var d = new Date(strDate)
    var year = d.getFullYear()
    var month = d.getMonth().toString().length < 2 ? "0"+d.getMonth().toString() :d.getMonth()
    var date = d.getDate().toString().length < 2 ? "0"+d.getDate().toString() :d.getDate()
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
                    var datetime = getFormatedDateTime(data.datetime)
                    var th = document.querySelector(td.getAttribute('data-th'))
                    var topicTitle = th.getAttribute('data-topic-title')
                    var taskitemTitle = th.getAttribute('data-taskitem-title')
                    var statusClass = 'status__' + data.status;
                    th.setAttribute('title', `Тема: ${topicTitle}\nЗадача: ${taskitemTitle}`)
                    td.classList.add(statusClass)
                    td.setAttribute('title', `Тема: ${topicTitle}\nЗадача: ${taskitemTitle}\n${userName}\n${datetime}\n`)
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
                    if(data.manual_check){
                        if(data.manual_check.status == MS__NOT_CHECKED){
                            td.classList.add('not-checked');
                        }
                        else if(MS__AWAITING_CHECK.indexOf(data.manual_check.status) != -1){
                            td.classList.add('awaiting-check');
                        }
                    }
                    td.append(content)
                    if(data.status == S_SUCCESS) total_solved_tasks+=1;
                    if(S_WITH_SCORE.indexOf(data.status) != -1) total_score += data.score;
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
        console.log('fake');
        $(".js__course__table-container").scrollLeft($(".js__course__fake-table-container").scrollLeft());
    });
    $(".js__course__table-container").scroll(function(){
        console.log('scroll');
        $(".js__course__fake-table-container").scrollLeft($(".js__course__table-container").scrollLeft());
    });
}

window.addEventListener('groupCoursePageLoaded', groupCoursePage)