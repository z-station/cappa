var getTaskitemTitle = (data) => {
    if(data.percent == 0){
        var title = ''
    } else {
        var localCreatedTime = new Date(data.datetime), // время с указанием часового пояса автоматически преобразуется ко времени в часовом поясе клиента
            createdLocalFormattedDate = getFormatedDateTime(localCreatedTime),
            candidateName = window.candidates[data.candidate.id],
            referenceName = window.candidates[data.reference.id];
        var title = `Пользователь: ${referenceName}\nКандидат: ${candidateName}\nСовпадение: ${getFormattedNumber(data.percent * 100, 0)}%\nДата проверки: ${createdLocalFormattedDate}`
    }
    return title
}

var clearTaskitemContent = () => {
    taskitem.innerHTML = ''
    taskitem.classList.remove('s-black', 's-green', 's-yellow', 's-red')
}

var getPlagByTaskItem = async (taskitem) => {
    return new Promise(function(resolve, reject) {
        var candidateIds = window.candidateIds,
            tr = taskitem.parentElement,
            referenceUserId = Number(tr.dataset.userId),
            taskitemId = taskitem.dataset.taskitemId,
            requestData = {
                reference_user_id: referenceUserId,
                candidates: candidateIds
            }
        fetch(
            `/api/tasks/taskitem/${taskitemId}/check-plag/`,
            {
                method: 'POST',
                body:  JSON.stringify(requestData),
                headers: {
                    'Authorization': `Token ${window.authToken}`,
                    'Content-Type': 'application/json;charset=utf-8'
                }
            }
        ).then(
            (response) => {
                if (response.status == 204){
                   return {}
                } else if (response.status == 200){
                   return response.json()
                } else if (response.status == 500){
                    return response.json()
                }
            }, // await response body
            (error) => {
                reject(error)
            }
        ).then(
            (data) => resolve(data)
        ).catch((error) => {reject(error)})
    })
}

var showPlagByTaskItem = (taskitem, data) => {
    var percent = getFormattedNumber(data.percent * 100, 0)
    if (percent == 0){
        var tdContent = document.createElement('div')
        tdContent.innerHTML = '+'
        taskitem.classList.add('s-green')
    } else if(percent > 0) {
        var tdContent = document.createElement('a')
        tdContent.setAttribute('href', `/solutions/${data.reference.solution_id}/diff/${data.candidate.solution_id}`)
        tdContent.setAttribute('target', '_blank')
        tdContent.innerHTML = percent
        if(percent <= 25) {
            taskitem.classList.add('s-green')
        } else if(percent > 25 && percent <= 50) {
            taskitem.classList.add('s-yellow')
        } else {
            taskitem.classList.add('s-red')
        }
        taskitem.setAttribute('title', getTaskitemTitle(data))
    }
    taskitem.append(tdContent)
}

var showTaskItemError = (taskitem, data) => {
    taskitem.classList.add('s-grey')
    var tdContent = document.createElement('div')
    tdContent.innerHTML = 'x'
    taskitem.append(tdContent)
    taskitem.setAttribute('title', data.message)

}

var refreshUserListener = async (tr) => {
        showLoader()
        var taskitems = tr.querySelectorAll('.js__taskitem');
        for (taskitem of taskitems) {
            clearTaskitemContent()
            await getPlagByTaskItem(taskitem).then(
                (data) => {
                    // 204 статус ответа и пустое тело если нет решения по задаче
                    if (Object.keys(data).length){
                        if(data.percent){
                            showPlagByTaskItem(taskitem, data)
                        } else if (data.message) {
                            showTaskItemError(taskitem, data)
                        }
                    }
                },
                (error) => console.log(error)
            )
        }
        hideLoader()
}


//var refreshAllUsersListener = async () => {
//    return new Promise(function(resolve, reject) {
//        var users = document.querySelectorAll('.js__member')
//        for (user of users) {
//            var result = async refreshUserListener(users)
//        })
//        return resolve()
//    })
//}

var loadGroupStatistics = async () => {
    var response = await fetch(
         window.groupCoursePlagStatisticsUrl,
         {
            method: 'GET',
            headers: {
                'Authorization': `Token ${window.authToken}`,
                'Content-Type': 'application/json;charset=utf-8'
            }
         }
    )
    if (response.ok){
        var data = await response.json()
        for(const [userId, userData] of Object.entries(data)){
            var tr = document.querySelector(`.js__member-${userId}`)
            for(const [taskitemId, plagData] of Object.entries(userData)){
                var taskitem = tr.querySelector(`.js__taskitem__${taskitemId}`)
                showPlagByTaskItem(taskitem, plagData)
            }
        }
        hideLoader()
    }
}

var groupCoursePlagPage = (e) => {

    loadGroupStatistics()

    $(".js__course__fake-table").width($(".js__course__table").width() + 20);

    $(".js__course__fake-table-container").scroll(function(){
        $(".js__course__table-container").scrollLeft($(".js__course__fake-table-container").scrollLeft());
    });

    $(".js__course__table-container").scroll(function(){
        $(".js__course__fake-table-container").scrollLeft($(".js__course__table-container").scrollLeft());
    });

    var searchForm = document.getElementById('js__search-form')
    searchForm && searchForm.addEventListener('submit', (event) => tableFilter.search(event))

    document.querySelectorAll('.js__refresh-user').forEach((elem) => {
        elem.addEventListener('click', (event) => {
            let tr = event.target.parentElement
            refreshUserListener(tr)
        })
    })

//    document.querySelector('.js__refresh-all').addEventListener('click', (event) => {
//        showLoader()
//        refreshAllUsersListener()
//        hideLoader()
//    })

}

window.addEventListener('groupCoursePlagPageLoaded', groupCoursePlagPage)