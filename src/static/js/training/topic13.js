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
                    switch(form.querySelector(".js__lang").value){
                        case 'python':
                            editor.getSession().setMode("ace/mode/python"); break
                        case 'cpp':
                            editor.getSession().setMode("ace/mode/c_cpp"); break
                        case 'csharp':
                            editor.getSession().setMode("ace/mode/csharp"); break
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
            showMsg(response){
                formControl.hideMsg()
                switch(response.status){
                    case 200:
                        form.querySelector('.js__msg-success').innerHTML = response.msg
                        form.querySelector('.js__msg-success').style.display = 'block'
                        break
                    case 201:
                        form.querySelector('.js__msg-warning').innerHTML = response.msg
                        form.querySelector('.js__msg-warning').style.display = 'block'
                        break
                    case 202:
                    case 203:
                    case 204:
                        form.querySelector('.js__msg-error').innerHTML = response.msg
                        form.querySelector('.js__msg-error').style.display = 'block'
                        break
                }
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
                formControl.showLoader('Отладка')
                formControl.disableBtns()
                $.post(form.getAttribute('action'), formControl.serializeForm(operation='debug'), function(response){
                    formControl.showMsg(response);
                    if(response.output){
                        form.querySelector('.js__output .js__editor-content').innerHTML = response.output
                        form.querySelector('.js__output').style.display = 'block'
                    } else {
                        form.querySelector('.js__output').style.display = 'none'
                    }
                    if(response.error){
                        form.querySelector('.js__error .js__editor-content').innerHTML = response.error
                        form.querySelector('.js__error').style.display = 'block'
                    } else {
                        form.querySelector('.js__error').style.display = 'none'
                    }
                    formControl.aceInit();
                    formControl.enableBtns()
                })
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