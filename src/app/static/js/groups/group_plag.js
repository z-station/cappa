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
        ).then((response) => {return response.json()}
        ).then((data) => {resolve(data)}
        ).catch(error => {reject(error)})
    })
}

var showPlagByTaskItem = (taskitem, data) => {
/**
	Зеленый (0 - 25%)
	Желтый (26 - 50%)
	Красный (51 - 100%)
**/

    console.log('showPlagByTaskItem', data)
    if (data.percent <= 0){
        var tdContent = document.createElement('div')
        if (data.percent < 0){
            tdContent.innerHTML = '❎'
            taskitem.classList.add('s-black')
        } else {
            tdContent.innerHTML = '+'
            taskitem.classList.add('s-green')
        }
    } else if(data.percent > 0) {
        var tdContent = document.createElement('a')
        tdContent.setAttribute('href', `/solutions/${data.reference.solution_id}/diff/${data.candidate.solution_id}`)
        tdContent.setAttribute('target', '_blank')
        tdContent.innerHTML = getFormattedNumber(data.percent)
        if(data.percent <= 0.25) {
            taskitem.classList.add('s-green')
        } else if(data.percent > 0.25 && data.percent <= 0.5) {
            taskitem.classList.add('s-yellow')
        } else {
            taskitem.classList.add('s-red')
        }
    }
    taskitem.append(tdContent)

}
var showTaskItemError = (taskitem, error) => {
    console.log('showTaskItemError', error)
}

var refreshListener = async (event) => {
    var taskitems = event.target.parentElement.querySelectorAll('.js__taskitem');
    for (taskitem of taskitems) {
        await getPlagByTaskItem(taskitem).then(
            (data) => showPlagByTaskItem(taskitem, data),
            (error) => showTaskItemError(taskitem, error),
        )
    }
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
                }
                document.querySelector('.js__loader').style.display = 'none';
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                document.querySelector('.js__loader').style.display = 'none';
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