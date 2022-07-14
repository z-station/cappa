var getTaskitemTitle = (data) => {
    if(data.percent == 0){
        var title = ''
    } else {
        var candidateName = window.candidates[data.candidate.id]
        var referenceName = window.candidates[data.reference.id]
        var title = `Пользователь: ${referenceName}\nКандидат: ${candidateName}\nСовпадение: ${getFormattedNumber(data.percent * 100, 0)}%`
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
            `/api/training/taskitem/${taskitemId}/check-plag/`,
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
        )
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

var refreshListener = async (event) => {
    showLoader()
    var taskitems = event.target.parentElement.querySelectorAll('.js__taskitem');
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

var groupCoursePlagPage = (e) => {

    $.ajax({
        url: window.groupCoursePlagStatisticsUrl,
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        headers: {
            'Authorization': `Token ${window.authToken}`
        },
        statusCode:{
            200: function(response){
                for(const [user_id, user_data] of Object.entries(response)){
                    // pass
                }
                hideLoader()
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                // show error
                hideLoader()
            }
        }
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

    document.querySelectorAll('.js__refresh').forEach((elem) => {
        elem.addEventListener('click', refreshListener)
    })

}

window.addEventListener('groupCoursePlagPageLoaded', groupCoursePlagPage)