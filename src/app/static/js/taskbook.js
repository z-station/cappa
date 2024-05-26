
var initTaskBookFilter = function(){
    /* Раскрыть и отметить зеленым выбранные фильтры */
    document.querySelectorAll('.js__choices').forEach(
        function(elem){
            var activeCheckbox = elem.querySelectorAll(`input[type=checkbox]:checked`).length,
                buttonId = `#js__${elem.dataset.name}_btn`;
            if (activeCheckbox == 0){
                document.querySelector(buttonId).classList.remove("btn-success")
            } else {
                var btn = document.querySelector(buttonId);
                btn.classList.add("btn-success");
                $(elem).collapse('show');
            }
        }
    )


    /* Отмечать зеленым фильтр после того как он выбран */
    document.querySelectorAll('.js__checkbox-container input').forEach(
        function(elem){
            elem.addEventListener('click', function(e){
                var inputName = e.target.getAttribute('name'),
                    buttonId = `#js__${inputName}_btn`,
                    activeCheckbox = document.querySelectorAll(`#js__${inputName}_choices input[type=checkbox]:checked`).length;
                if (activeCheckbox == 0){
                    document.querySelector(buttonId).classList.remove("btn-success")
                } else {
                    document.querySelector(buttonId).classList.add("btn-success")
                }
            })
        }
    )
}

var taskBookPage = function(){
    window.dispatchEvent(new Event('initTablesorter'));
        $(".js-range-slider").ionRangeSlider({
            onFinish: function (data) {
                document.querySelector('#id_rating_0').value = data.from;
                document.querySelector('#id_rating_1').value = data.to;
            },
        });

    initTaskBookFilter()
}


window.addEventListener('taskBookPageLoaded', taskBookPage)
