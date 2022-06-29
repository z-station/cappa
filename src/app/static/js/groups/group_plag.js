// duplicate
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

async function checkPlagForTaskItem(taskitem){
    var candidateIds = window.candidateIds,
        tr = taskitem.parentElement,
        referenceUserId = Number(tr.dataset.userId),
        taskitemId = taskitem.dataset.taskitemId,
        requestData = {
            reference_user_id: referenceUserId,
            candidates: candidateIds
        };

    return $.ajax({
        url: `/api/training/taskitem/${taskitemId}/check-plag/`,
        type: 'POST',
        data: JSON.stringify(requestData),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        headers: {
            'Authorization': `Token ${window.authToken}`
        },
        statusCode:{
            200: function(response){
                console.log(1)
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log(2)
            }
        }
    })
}


async function refreshListener(event){
    var taskitems = event.target.parentElement.querySelectorAll('.js__taskitem');
    for (taskitem of taskitems) {
        await checkPlagForTaskItem(taskitem)
    }
}

var groupCoursePlagPage = function(e){
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