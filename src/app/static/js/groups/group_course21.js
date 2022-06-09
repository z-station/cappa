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

var groupCoursePage = function(e){

    $.ajax({
        url: window.groupCourseSolutionsUrl,
        type: 'GET',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        headers: {
            'Authorization': `Token ${window.authToken}`
        },
        statusCode:{
            200: function(response){
               for(const [user_id, user_data] of Object.entries(response)){
                    var total_solved_tasks = 0,
                        total_score = 0,
                        tr = document.querySelector('#js__member-' + user_id)
                    var userName = tr.querySelector('td.js__username').innerText

                    for(const [taskitem, data] of Object.entries(user_data)){
                        var td = tr.querySelector('.js__taskitem__' + taskitem)
                        if(td){
                            if (data.due_date){
                                overdue = new Date(data.created) > new Date(data.due_date)
                            } else {
                                overdue = false
                            }
                            var localCreatedTime = new Date(data.created); // время с указанием часового пояса автоматически преобразуется ко времени в часовом поясе клиента
                            var createdLocalFormattedDate = getFormatedDateTime(localCreatedTime),
                                th = document.querySelector(td.getAttribute('data-th')),
                                topicTitle = th.getAttribute('data-topic-title'),
                                taskitemTitle = th.getAttribute('data-taskitem-title'),
                                title = `${userName}\n${createdLocalFormattedDate}\n${taskitemTitle}\nТема: ${topicTitle}`;
                            if(overdue){
                                title = title + '\nРешение отправлено позже даты сдачи'
                            }
                            td.setAttribute('title', title)
                            // set td link
                            if(window.userIsTeacher){
                                var tdContent = document.createElement('a')
                                tdContent.setAttribute('href', `/solutions/${data.id}/`)
                                tdContent.setAttribute('target', '_blank')
                            } else {
                                var tdContent = document.createElement('div')
                            }
                            // set td content and color
                            if(overdue){
                                td.classList.add('s-grey')
                            }
                            if(checkMethods.reviewMethods.indexOf(data.score_method) != -1){
                                if (data.review_status == reviewStatuses.checked){
                                    if (data.review_score == null){ // оценка скрыта
                                        tdContent.innerHTML = '✔'
                                        if (!overdue){
                                            td.classList.add('s-green')
                                            total_solved_tasks += 1
                                        }
                                    } else if (data.review_score == data.max_score){
                                        tdContent.innerHTML = '+'
                                        if (!overdue){
                                            td.classList.add('s-green')
                                            total_solved_tasks += 1
                                            total_score += data.review_score
                                        }
                                    } else if (data.review_score == 0){
                                        tdContent.innerHTML = '-'
                                        if (!overdue){
                                            td.classList.add('s-red')
                                        }
                                    } else if (data.review_score != null){
                                        tdContent.innerHTML = data.review_score
                                        if (!overdue){
                                            td.classList.add('s-yellow')
                                            total_solved_tasks += 1
                                            total_score += data.review_score
                                        }
                                    }
                                } else if(reviewStatuses.awaitingCheck.indexOf(data.review_status) != -1){
                                    td.classList.add('awaiting-check')
                                    if (!overdue){
                                        td.classList.add('s-cyan')
                                    }
                                }
                            } else if (data.score_method == checkMethods.tests){
                                if (data.testing_score == data.max_score){
                                    tdContent.innerHTML = '+'
                                    if (!overdue){
                                        td.classList.add('s-green')
                                        total_solved_tasks += 1
                                        total_score += data.testing_score
                                    }
                                } else if (data.testing_score == 0){
                                    if (!overdue){td.classList.add('s-red')}
                                    tdContent.innerHTML = '-'
                                } else if (data.testing_score != null){
                                    tdContent.innerHTML = data.review_score
                                    if (!overdue){
                                        td.classList.add('s-yellow')
                                        total_solved_tasks += 1
                                        total_score += data.testing_score
                                    }
                                }
                            }
                            td.append(tdContent)
                        }
                    }
                    tr.querySelector('.js__total_solved_tasks').innerHTML = total_solved_tasks;
                    tr.querySelector('.js__total_score').innerHTML = total_score.toFixed(1);
                }
                $(".js__tablesorter").tablesorter()
                document.querySelector('.js__loader').style.display = 'none';

            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            document.querySelector('.js__loader').style.display = 'none';
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

}

window.addEventListener('groupCoursePageLoaded', groupCoursePage)