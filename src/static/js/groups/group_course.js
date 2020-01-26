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
            var score = 0
            var userName = val.full_name
            var tr = document.querySelector('#js__' + member)
            for(const [taskitem, data] of Object.entries(val.data)){
                var td = tr.querySelector('.js__' + taskitem)
                if(td){
                    var datetime = getFormatedDateTime(data.datetime)
                    var th = document.querySelector(td.getAttribute('data-th'))
                    var title = th.getAttribute('title')
                    var statusClass = 'status__' + data.status;
                    td.classList.add(statusClass)
                    td.setAttribute('title', `${userName}\n${datetime}\n${title}`)
                    if(data.status == 3) score+=1
                    if(val.show_link){
                        var content = document.createElement('a')
                        content.setAttribute('href', data.url)
                        content.setAttribute('target', '_blank')
                    } else {
                        var content = document.createElement('div')
                    }
                    if(data.status == 3){
                        content.innerHTML = '+'
                    } else if(data.status == 2){
                        content.innerHTML = data.progress + '%'
                    } else if(data.status == 1){
                        content.innerHTML = '-'
                    }
                    td.append(content)
                }
            }
            tr.querySelector('.js__score').innerHTML = score
        }
        $(".js__tablesorter").tablesorter()
        document.querySelector('.js__loader').style.display = 'none';

    })

}

window.addEventListener('groupCoursePageLoaded', groupCoursePage)