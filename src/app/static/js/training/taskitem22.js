var PYTHON38 = '1',
    GCC74 = '2';

var taskItemPage = function(e){

    var lastChanges = ''
    var form = document.querySelector('.js__editor-form')
    // скрипт контрольной панели редактора кода
    var formControl = {
        aceInit: function(){
            // инициализировать ace-editor
            form.querySelectorAll('.js__editor').forEach(function(elem, index){
                var textarea = elem.querySelector('.js__editor-content')
                var editor = ace.edit(elem.querySelector('.js__editor-ace'))
                editor.setOption("wrap", true)                 // добавляет перенос строк
                editor.setOption("showPrintMargin", false)     // убрать верт черту
                editor.setOption("maxLines", "Infinity")       // авто-высота
                editor.setHighlightActiveLine(false);          // убрать строку вделения
                editor.setReadOnly(textarea.getAttribute('readonly'))  // для чтения
                switch(form.querySelector(".js__translator").value){
                    case PYTHON38:
                        editor.getSession().setMode("ace/mode/python"); break
                    case GCC74:
                        editor.getSession().setMode("ace/mode/c_cpp"); break
                }

                // вписать код из textarea в ace-editor
                editor.setValue(textarea.textContent, - 1)

                // после записи кода в ace-editor скопировать его в textarea
                editor.addEventListener('change', function(e){
                    textarea.innerHTML = editor.getValue()
                    // если поле контента пустое то заблокировать панель редактора
                    if(elem.classList.contains('js__content')){
                        if(editor.getValue() == ''){
                            formControl.disableBtns()
                        } else {
                            formControl.enableBtns()
                        }
                    }
                })

                // если в редкаторе пусто то заблокировать панель редактора
                if(elem.classList.contains('js__content') && textarea.innerHTML == ''){
                    formControl.disableBtns()
                }
            })
        },
        hideMsg: function(){
            form.querySelectorAll('.js__msg').forEach(function(msg){
                msg.style.display = 'none'
            })
        },
        disableBtns: function(){
           form.querySelectorAll('.js__editor-btn').forEach(function(btn){
               btn.classList.add('disabled')
           })
        },
        disableBtn: function(btnName){
           var btn = form.querySelector(`.js__editor-btn.js__editor-btn-${btnName}:not(.js__permanent-disabled)`);
           btn && btn.classList.add('disabled');
        },
        permanentDisableBtn: function(btnName){
           var btn = form.querySelector(`.js__editor-btn.js__editor-btn-${btnName}`);
           btn && btn.classList.add('js__permanent-disabled');
        },
        enableBtns: function(){
           form.querySelectorAll('.js__editor-btn:not(.js__permanent-disabled)').forEach(function(btn){
           btn.classList.remove('disabled')
           })
        },
        enableVersionsBtn: function(){
            var versionsBtn = form.querySelector('.js__editor-btn-versions')
            versionsBtn && versionsBtn.classList.remove('not-versions')
        },
        showLoader: function(msg){
            formControl.hideMsg();
            form.querySelector('.js__msg-loader').style.display = 'block'
            form.querySelector('.js__msg-loader-text').innerHTML = msg
            form.querySelector('.js__msg-loader-text').style.display = 'block'
        },
        showMsg(response){
            formControl.hideMsg();
            if(response.status == 'ok'){
                form.querySelector('.js__msg-success').innerHTML = response.msg
                form.querySelector('.js__msg-success').style.display = 'block'
            } else if(response.status == 'warning'){
                form.querySelector('.js__msg-warning').innerHTML = response.msg
                form.querySelector('.js__msg-warning').style.display = 'block'
            } else {
                form.querySelector('.js__msg-error').innerHTML = response.msg
                form.querySelector('.js__msg-error').style.display = 'block'
            }
            setTimeout(function(){ formControl.hideMsg() }, 10000);
        },
        showErrorMsg(msg){
            formControl.hideMsg();
            form.querySelector('.js__msg-error').innerHTML = msg
            form.querySelector('.js__msg-error').style.display = 'block'
            formControl.aceInit();
            formControl.enableBtns();
            setTimeout(function(){ formControl.hideMsg() }, 10000);
        },
        serializeForm(operation){
            // вернуть данные формы + submitType
            var data = {},
                formArray = $(form).serializeArray();

            for (i=0; i<formArray.length; i++){
                var value = formArray[i].value;
                if(value){
                    data[formArray[i].name] = value;
                }
            }
            data['operation'] = operation
            return data
        },
        getConfirmation: function(e, msg){
            if(e.target.classList.contains('js__one_try')){
                confirmed = confirm(msg)
            } else {
                confirmed = true
            }
            return confirmed
        },
        debug : function(e){
            // запрос на отладку кода из редактора
            var formData = formControl.serializeForm(operation='debug');
            if(formData.content){
                formControl.showLoader('Отладка');
                formControl.disableBtns();
                var url = window.translators_urls[formData.translator],
                    data = {'code': formData.content};
                if(formData.input){
                    data['translator_console_input'] = formData.input;
                }
                $.ajax({
                    url: `${url}/debug/`,
                    type: 'POST',
                    data: JSON.stringify(data),
                    contentType: 'application/json; charset=utf-8',
                    dataType: 'json',
                    statusCode:{
                        200: function(response){
                            // Отображение сообщения
                            formControl.hideMsg();
                            if(response.translator_error_msg){
                                form.querySelector('.js__msg-warning').innerHTML = 'Ошибка'
                                form.querySelector('.js__msg-warning').style.display = 'block'
                            } else {
                                form.querySelector('.js__msg-success').innerHTML = 'Готово'
                                form.querySelector('.js__msg-success').style.display = 'block'
                            }
                            // Отображение результата работы программы
                            if(response.translator_console_output){
                                form.querySelector('.js__output .js__editor-content').innerHTML = response.translator_console_output
                                form.querySelector('.js__output').style.display = 'block'
                            } else {
                                form.querySelector('.js__output').style.display = 'none'
                            }
                            // Отображение текста ошибки
                            if(response.translator_error_msg){
                                form.querySelector('.js__error .js__editor-content').innerHTML = response.translator_error_msg
                                form.querySelector('.js__error').style.display = 'block'
                            } else {
                                form.querySelector('.js__error').style.display = 'none'
                            }
                            formControl.aceInit();
                            formControl.enableBtns();
                        },
                        400: function(response){
                            formControl.showErrorMsg('Ошибка запроса (400)');
                        },
                        403: function(response){
                            formControl.showErrorMsg('Запрос отклонен (403)');
                        },
                        404: function(response){
                            formControl.showErrorMsg('Сервис недоступен (404)');
                        },
                        500: function(){
                            formControl.showErrorMsg('Серверная ошибка (500)');
                        },
                        502: function(response){
                            formControl.showErrorMsg('Сервис недоступен (502)');
                        }
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        formControl.showErrorMsg('Запрос не выполнен');
                    }
                })
            }
            return false
        },
        tests : function(e){
            var formData = formControl.serializeForm(operation='check_tests')
            if(formData.content){
                formControl.showLoader('Тестирование')
                formControl.disableBtns();
                $.ajax({
                    url: form.getAttribute('action'),
                    type: 'POST',
                    data: formData,
                    headers: {
                        'X-CSRF-Token': formData.csrfmiddlewaretoken
                    },
                    statusCode:{
                        200: function(response){
                            formControl.showMsg(response)
                            table = document.querySelector('.js__form__tests-table')
                            if(response.sandbox_data && response.sandbox_data.ok){
                                table.querySelector('th.js__form__test-result').innerHTML = 'Вывод программы'
                                response.sandbox_data.data.tests_data.forEach(function(test, index){
                                    var tr = table.querySelector('.js__form__test-'+ index)
                                    if(test.ok){
                                        tr.classList.remove('success', 'unluck')
                                        tr.classList.add('success')
                                    } else {
                                        tr.classList.remove('success', 'unluck')
                                        tr.classList.add('unluck')
                                    }
                                    var testResult = '';
                                    if(test.translator_console_output && test.translator_error_msg){
                                        testResult = `${test.translator_console_output}\n\n${test.translator_error_msg}`
                                    } else if(test.translator_console_output){
                                        testResult = test.translator_console_output
                                    } else if(test.translator_error_msg){
                                        testResult = test.translator_error_msg
                                    }
                                    tr.querySelector('.js__form__test-result pre').innerHTML = testResult
                                })
                                // if(response.tests_result.id){
                                //     var sidebarItem = document.querySelector('#js__' + response.tests_result.id)
                                //     sidebarItem && sidebarItem.classList.remove('status__0', 'status__1', 'status__2', 'status__3')
                                //     sidebarItem && sidebarItem.classList.add('status__'+ response.tests_result.status)
                                // }
                            }
                            formControl.aceInit();
                        },
                        400: function(response){
                            formControl.showErrorMsg('Ошибка запроса (400)');
                        },
                        403: function(response){
                            formControl.showErrorMsg('Запрос отклонен (403)');
                        },
                        404: function(response){
                            formControl.showErrorMsg('Сервис недоступен (404)');
                        },
                        500: function(){
                            formControl.showErrorMsg('Серверная ошибка (500)');
                        },
                        502: function(response){
                            formControl.showErrorMsg('Сервис недоступен (502)');
                        }
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        formControl.showErrorMsg('Запрос не выполнен');
                    }
                })
            }
            return false;
        },
        save: function(e){
            var formData = formControl.serializeForm(operation='save_solution')
            if(formData.content){
                formControl.showLoader('Сохранение');
                $.ajax({
                    url: form.getAttribute('action'),
                    type: 'POST',
                    data: formData,
                    headers: {
                        'X-CSRF-Token': formData.csrfmiddlewaretoken
                    },
                    statusCode:{
                        200: function(response){
                            formControl.showMsg(response)
                        },
                        400: function(response){
                            formControl.showErrorMsg('Ошибка запроса (400)');
                        },
                        403: function(response){
                            formControl.showErrorMsg('Запрос отклонен (403)');
                        },
                        404: function(response){
                            formControl.showErrorMsg('Сервис недоступен (404)');
                        },
                        500: function(){
                            formControl.showErrorMsg('Серверная ошибка (500)');
                        },
                        502: function(response){
                            formControl.showErrorMsg('Сервис недоступен (502)');
                        }
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        formControl.showErrorMsg('Запрос не выполнен');
                    }
                })
                formControl.aceInit();
            }
            return false
        },
        autosave: function(e){
            var formData = formControl.serializeForm(operation='save_last_changes')
            if(formData.content){
                formControl.showLoader('Автосохранение')
                $.ajax({
                    url: form.getAttribute('action'),
                    type: 'POST',
                    data: formData,
                    headers: {
                        'X-CSRF-Token': formData.csrfmiddlewaretoken
                    },
                    statusCode:{
                        200: function(response){
                            formControl.showMsg(response)
                        },
                        400: function(response){
                            formControl.showErrorMsg('Ошибка запроса (400)');
                        },
                        403: function(response){
                            formControl.showErrorMsg('Запрос отклонен (403)');
                        },
                        404: function(response){
                            formControl.showErrorMsg('Сервис недоступен (404)');
                        },
                        500: function(){
                            formControl.showErrorMsg('Серверная ошибка (500)');
                        },
                        502: function(response){
                            formControl.showErrorMsg('Сервис недоступен (502)');
                        }
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        formControl.showErrorMsg('Запрос не выполнен');
                    }
                })
                return false
            }
        },
        ready: function(e){
            var formData = formControl.serializeForm(operation='ready_solution')
            if(formData.content){
                var confirmed = formControl.getConfirmation(e, 'После отправки решения на проверку его будет нельзя изменить. Вы согласны?');
                if(confirmed){
                    formControl.showLoader('Отправляем на проверку');
                    formControl.disableBtns();
                    $.ajax({
                        url: form.getAttribute('action'),
                        type: 'POST',
                        data: formData,
                        headers: {
                            'X-CSRF-Token': formData.csrfmiddlewaretoken
                        },
                        statusCode:{
                            200: function(response){
                                formControl.showMsg(response);
                                if(e.target.classList.contains('js__one_try')){
                                    formControl.permanentDisableBtn('save');
                                    formControl.permanentDisableBtn('ready');
                                }
                                formControl.enableVersionsBtn();
                            },
                            400: function(response){
                                formControl.showErrorMsg('Ошибка запроса (400)');
                            },
                            403: function(response){
                                formControl.showErrorMsg('Запрос отклонен (403)');
                            },
                            404: function(response){
                                formControl.showErrorMsg('Сервис недоступен (404)');
                            },
                            500: function(){
                                formControl.showErrorMsg('Серверная ошибка (500)');
                            },
                            502: function(response){
                                formControl.showErrorMsg('Сервис недоступен (502)');
                            }
                        },
                        error: function (XMLHttpRequest, textStatus, errorThrown) {
                            formControl.showErrorMsg('Запрос не выполнен');
                        }
                    })
                    formControl.enableBtns();
                }
            }
        }
    }

    formControl.aceInit()
    // Автосохранение раз в 3 мин. при условии что решение изменялось
    window.setInterval(function(){
        newChanges = form.querySelector('.js__content .js__editor-content').innerHTML
        var versionsBtn = form.querySelector('.js__editor-btn-versions')
        if(versionsBtn && newChanges != lastChanges){
            formControl.autosave();
            lastChanges = newChanges
        }
    }, 180000)

    // Обработчики кнопок
    var debugBtn = form.querySelector('.js__editor-btn-debug')
    debugBtn && debugBtn.addEventListener('click', formControl.debug)

    var testsBtn = form.querySelector('.js__editor-btn-tests')
    testsBtn && testsBtn.addEventListener('click', formControl.tests)

    var saveBtn = form.querySelector('.js__editor-btn-save')
    saveBtn && saveBtn.addEventListener('click', formControl.save)

    var readyBtn = form.querySelector('.js__editor-btn-ready')
    readyBtn && readyBtn.addEventListener('click', formControl.ready)
}

window.addEventListener('taskItemPageLoaded', taskItemPage)