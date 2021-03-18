var PYTHON38 = '1',
    GCC74 = '2';

var topicPage = function(e){

    document.querySelectorAll('.js__editor-form').forEach(function(form, index){

        // скрипт контрольной панели редактора кода
        var formControl = {
            aceInit: function(){
                // инициализировать ace-editor
                form.querySelectorAll('.js__editor').forEach(function(elem, index){
                    var textarea = elem.querySelector('.js__editor-content')
                    var editor = ace.edit(elem.querySelector('.js__editor-ace'))
                    editor.setOption("showPrintMargin", false)     // убрать верт черту
                    editor.setOption("maxLines", "Infinity")       // авто-высота
                    editor.setHighlightActiveLine(false);          // убрать строку вделения
                    editor.setReadOnly(Boolean(form.getAttribute('readonly') == 'True'))  // для чтения
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
            enableBtns: function(){
               form.querySelectorAll('.js__editor-btn').forEach(function(btn){
               btn.classList.remove('disabled')
               })
            },
            showLoader: function(msg){
                formControl.hideMsg();
                form.querySelector('.js__msg-loader').style.display = 'block'
                form.querySelector('.js__msg-loader-text').innerHTML = msg
                form.querySelector('.js__msg-loader-text').style.display = 'block'
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
                        async: false,
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
            }
        }

        formControl.aceInit()

        // Обработчики кнопок
        var debugBtn = form.querySelector('.js__editor-btn-debug')
        debugBtn && debugBtn.addEventListener('click', formControl.debug)

    })
}

window.addEventListener('topicPageLoaded', topicPage)