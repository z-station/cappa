var reviewStatuses = {
    ready: 'ready',
    review: 'review',
    checked: 'checked',
    awaitingCheck: ['ready', 'review']
}
var checkMethods = {
    tests: 'tests',
    review: 'review',
    testsAndReview: 'tests_and_review',
    testsMethods: ['tests', 'tests_and_review'],
    reviewMethods: ['review', 'tests_and_review']
}

var setStatus = function(elem, data){
    if (data.due_date){
        overdue = new Date(data.created) > new Date(data.due_date)
    } else {
        var overdue = false
    }
    
    if(overdue){
        elem.classList.add('s-grey');
    } else {
        if(checkMethods.reviewMethods.indexOf(data.score_method) != -1){
            if (data.review_status == reviewStatuses.checked){
                if (data.review_score == data.max_score){
                    elem.classList.add('s-green')
                } else if (data.review_score == 0){
                    elem.classList.add('s-red')
                } else if (data.review_score != null){
                    elem.classList.add('s-yellow')
                }
            } else if(reviewStatuses.awaitingCheck.indexOf(data.review_status) != -1){
                elem.classList.add('s-cyan')
            }
        } else if (data.score_method == checkMethods.tests){
            if (data.testing_score == data.max_score){
                elem.classList.add('s-green')
            } else if (data.testing_score == 0){
                elem.classList.add('s-red')
            } else if (data.testing_score != null){
                elem.classList.add('s-yellow')
            }
        }
    }
}

var getUserSolutions = function(e){

    // запрос списка решений задач курса и их отображение

    $.ajax({
        url: window.courseStatisticsUrl,
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        headers: {
            'Authorization': `Token ${window.authToken}`
        },
        statusCode:{
            200: function(response){
                for (const [taskitemId, data] of Object.entries(response)) {
                    var elem = document.querySelector('#js__taskitem__' + taskitemId)
                    if(elem){
                        setStatus(elem, data)
                    }
                }
                document.querySelectorAll('.js__topic-item').forEach(function(elem){
                    var taskitems = elem.querySelectorAll('.js__taskitem-item')
                    var taskitems_success = elem.querySelectorAll('.js__taskitem-item.s-green:not(.overdue)')
                    if(taskitems.length != 0 && taskitems.length == taskitems_success.length){
                        elem.classList.add('s-green')
                    }
                })
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('Запрос статистики завершился с ошибкой');
        }
    })
}

var toggleSidebar = function(){
    // выделение текущей страницы курса в сайдбаре
    document.querySelectorAll('.js__topic-item').forEach(function(elem){
        var currentElem = elem.querySelector('.js__current')
        if(currentElem){
            var toggler = elem.querySelector('.topic__item-toggler')
            toggler && toggler.classList.remove('collapsed')
            var ul = elem.querySelector('ul')
            ul && ul.classList.add('show')
        }
    })
}

window.addEventListener('getUserSolutions', getUserSolutions)
window.addEventListener('toggleSidebar', toggleSidebar)