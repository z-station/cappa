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
                editor.setOption("showPrintMargin", false)     // убрать верт черту
                editor.setOption("maxLines", "Infinity")       // авто-высота
                editor.setHighlightActiveLine(false);          // убрать строку вделения
                editor.setReadOnly(textarea.getAttribute('readonly'))  // для чтения
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
        disableBtn: function(btnName){
           var btn = form.querySelector(`.js__editor-btn.js__editor-btn-${btnName}`);
           btn && btn.classList.add('disabled');
        },
        enableBtns: function(){
           form.querySelectorAll('.js__editor-btn').forEach(function(btn){
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
            var status = response.status;
            if(status >= 200 && status < 300){
                form.querySelector('.js__msg-success').innerHTML = response.msg
                form.querySelector('.js__msg-success').style.display = 'block'
            } else if(status >= 300 && status < 400){
                form.querySelector('.js__msg-warning').innerHTML = response.msg
                form.querySelector('.js__msg-warning').style.display = 'block'
            } else if (status >= 400 && status < 500){
                form.querySelector('.js__msg-error').innerHTML = response.msg
                form.querySelector('.js__msg-error').style.display = 'block'
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
                formControl.aceInit()
                formControl.enableBtns()
            })
            return false
        },
        tests : function(e){
            formControl.showLoader('Тестирование')
            formControl.disableBtns()
            $.post(form.getAttribute('action'), formControl.serializeForm(operation='check_tests'), function(response){
                formControl.showMsg(response)
                table = document.querySelector('.js__form__tests-table')
                if(response.tests_result){
                    table.querySelector('th.js__form__test-result').innerHTML = 'Вывод программы'
                    response.tests_result.data.forEach(function(test, index){
                        var tr = table.querySelector('.js__form__test-'+ index)
                        if(test.success){
                            tr.classList.remove('success', 'unluck')
                            tr.classList.add('success')
                        } else {
                            tr.classList.remove('success', 'unluck')
                            tr.classList.add('unluck')
                        }
                        tr.querySelector('.js__form__test-result pre').innerHTML = test.output + test.error
                    })
                    if(response.tests_result.id){
                        var sidebarItem = document.querySelector('#js__' + response.tests_result.id)
                        sidebarItem && sidebarItem.classList.remove('status__0', 'status__1', 'status__2', 'status__3')
                        sidebarItem && sidebarItem.classList.add('status__'+ response.tests_result.status)
                    }
                }
                formControl.aceInit();

            });
            return false;
        },
        version: function(e){
            formControl.showLoader('Сохранение версии')
            $.post(form.getAttribute('action'), formControl.serializeForm(operation='create_version'), function(response){
                formControl.showMsg(response)
                formControl.enableVersionsBtn()
            })
            return false

        },
        save: function(e){
            formControl.showLoader('Сохранение');
            $.post(form.getAttribute('action'), formControl.serializeForm(operation='save_solution'), function(response){
                formControl.showMsg(response)
                formControl.enableVersionsBtn()
            })
            return false
        },
        autosave: function(e){
            formControl.showLoader('Автосохранение')
            $.post(form.getAttribute('action'), formControl.serializeForm(operation='save_last_changes'), function(response){
                formControl.showMsg(response)
            })
            return false
        },
        ready: function(e){
            var confirmed = true;
            if(e.target.classList.contains('js__confirm')){
                confirmed = confirm('После отправки решения на проверку его будет нельзя изменить. Вы согласны?')
            }
            if(confirmed){
                formControl.showLoader('Отправляем на проверку');
                $.post(form.getAttribute('action'), formControl.serializeForm(operation='ready_solution'), function(response){
                    formControl.showMsg(response)
                    formControl.disableBtn('save');
                    formControl.enableVersionsBtn()
                })
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

    var versionBtn = form.querySelector('.js__editor-btn-version')
    versionBtn && versionBtn.addEventListener('click', formControl.version)

    var saveBtn = form.querySelector('.js__editor-btn-save')
    saveBtn && saveBtn.addEventListener('click', formControl.save)

    var readyBtn = form.querySelector('.js__editor-btn-ready')
    readyBtn && readyBtn.addEventListener('click', formControl.ready)
}

window.addEventListener('taskItemPageLoaded', taskItemPage)