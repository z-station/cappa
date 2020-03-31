
var getUserSolutions = function(e){
    // запрос списка решений задач курса и их отображение
    $.get(e.target.userSolutionUrl, function(response){
        for (const [key, val] of Object.entries(response)) {
            var elem = document.querySelector('#js__' + key)
            if(elem){
                elem.classList.add('status__' + val.status);
                if(val.awaiting_check){
                    elem.classList.add('awaiting-check');
                }
            }
        }
        document.querySelectorAll('.js__topic-item').forEach(function(elem){
            var taskitems = elem.querySelectorAll('.js__taskitem-item')
            var taskitems_success = elem.querySelectorAll('.js__taskitem-item.status__3')
            if(taskitems.length != 0 && taskitems.length == taskitems_success.length){
                elem.classList.add('status__3')
            }
        })
    })
}

var toggleSidebar = function(){
    // выделение текущей страницы курса в сайдбаре
    document.querySelectorAll('.js__topic-item').forEach(function(elem){
        var currentElem = elem.querySelector('.js__current')
        if(currentElem){
            elem.querySelector('.topic__item-toggler').classList.remove('collapsed')
            elem.querySelector('ul').classList.add('show')
        }
    })
}

window.addEventListener('getUserSolutions', getUserSolutions)
window.addEventListener('toggleSidebar', toggleSidebar)