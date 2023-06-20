
    /* widget example:

        <a href='...' class="js__solutions-link hidden">Список решений</a>

        <form
          class="js__editor-form"
          id="js__editor-form-1"
          data-translator="Python3.8"
          data-readonly="false"
          data-taskitemid="1" // только для полной версии
        >

            <div class="js__editor js__input">
                <label>Консольный ввод</label>
                <div class="js__editor-ace"></div>
                <textarea class="js__editor-content" name="input">...</textarea>
            </div>

            <div class="js__editor js__content">
                <label>Консольный ввод</label>
                <div class="js__editor-ace"></div>
                <textarea class="js__editor-content" name="content">...</textarea>
            </div>

            <div>
                <div class="js__editor-btn js__editor-btn-debug" title="Отладка"></div>
            </div>

            <div>
                <span class="js__msg js__msg-loader-text"></span>
                <span class="js__msg js__msg-loader">
                    <span class="pulse"><span>{</span><span>}</span></span>
                </span>
                <span class="js__msg js__msg-success"></span>
            </div>
        </form>
    */
/*
    POST /api/translators/python38/debug/
    POST /api/tasks/:id/draft/
    POST /api/training/taskitem/python38/:id/testing/
    POST /api/training/taskitem/python38/:id/create-solution/
*/

var editorInitField = (editor, field) => {

    /* Инициализация виджета ace-редактора для поля редактора */
    
    var textarea = field.querySelector('.js__editor-content'),
    aceWidget = ace.edit(field.querySelector('.js__editor-ace'));
    aceWidget.setOption("showPrintMargin", false)     // убрать верт черту
    aceWidget.setOption("maxLines", "Infinity")       // авто-высота
    aceWidget.setHighlightActiveLine(false);          // убрать строку вделения
    let fieldReadonly = textarea.getAttribute('readonly') == 'true'
    aceWidget.setReadOnly(editor.readonly || fieldReadonly)  // для чтения
    aceWidget.getSession().setMode(editor.colorScheme)       // цветовая схема редактора
    aceWidget.setValue(textarea.textContent, - 1)     // вписать код из textarea в ace-aceWidget
    aceWidget.addEventListener('change', function(e){ // при изменении кода в ace-editor скопировать его в textarea
        textarea.innerHTML = aceWidget.getValue()
        if(field.classList.contains('js__content')){// если поле контента пустое то заблокировать панель редактора
            if(aceWidget.getValue() == ''){
                editorDisableButtons(editor)
            } else {
                editorEnableButtons(editor)
            }
        }
    })
    // если в редкаторе пусто то заблокировать панель редактора
    if(field.classList.contains('js__content') && textarea.innerHTML == ''){
        editorDisableButtons(editor)
    }
}

var editorDisableButtons = (editor) => {
    editor.form.querySelectorAll('.js__editor-btn').forEach(function(btn){
        btn.classList.add('disabled')
    })
}

var editorEnableButtons = (editor) => {
    editor.form.querySelectorAll('.js__editor-btn').forEach(function(btn){
        btn.classList.remove('disabled')
    })
}

var editorShowMessage = (editor, msg, level='error') => {
    editorHideMessage(editor);
    var elem = editor.form.querySelector(`.js__msg-${level}`);
    if (elem){
        elem.innerHTML = msg;
        elem.style.display = 'block';
        setTimeout(() => { editorHideMessage(editor)}, 10000);
    }
}

var editorHideMessage = (editor) => {
    editor.form.querySelectorAll('.js__msg').forEach(function(elem){
        elem.style.display = 'none'
    })
}

var editorShowSolutionsLink = () => {
    let solutionsLink = document.querySelector('.js__solutions-link')
    solutionsLink && solutionsLink.classList.remove('hidden')
}

var editorShowLoader = (editor, msg) => {
    editorHideMessage(editor);
    editor.form.querySelector('.js__msg-loader').style.display = 'block'
    editor.form.querySelector('.js__msg-loader-text').innerHTML = msg
    editor.form.querySelector('.js__msg-loader-text').style.display = 'block'
}

var editorShowRequestError = (editor, request) => {
    editorEnableButtons(editor);
    if (request.status == 0 || !request.status){ // запрос не достиг сервера
        editorShowMessage(editor, editor.errorMessages[0])
    } else {
        switch (request.status){
            case 400: editorShowMessage(editor, request.responseJSON.message); break
            default: editorShowMessage(editor, editor.errorMessages[request.code])
        }
    }
}

var editorAutoSaveHandler = (editor) => {

    // Автосохранение раз в 3 мин. при условии что решение изменялось

    window.setInterval(() => {
        currentDraft = editor.form.querySelector('.js__content .js__editor-content').innerHTML
        if(currentDraft != editor.draft){
            editor.saveDraft()
            editor.draft = currentDraft
        }
    }, 180000)
}

class Editor {

    colorSchemes = {
        'Python3.8': 'ace/mode/python',
        'GCC7.4': 'ace/mode/c_cpp',
        'Prolog-D': 'ace/mode/prolog',
        'PostgreSQL': 'ace/mode/pgsql',
        'Pascal': 'ace/mode/pascal',
        'Php': 'ace/mode/php',
        'CSharp': 'ace/mode/csharp',
        'Java': 'ace/mode/java',
    }
    urlNames = {
        'Python3.8': 'python38',
        'GCC7.4': 'gcc74',
        'Prolog-D': 'prolog-d',
        'PostgreSQL': 'postgresql',
        'Pascal': 'pascal',
        'Php': 'php',
        'CSharp': 'csharp',
        'Java': 'java',
    }
    errorMessages = {
        0: 'Сайт недоступен',
        403: 'Запрос отклонен',
        404: 'Сервис не найден',
        500: 'Внутренняя ошибка',
        502: 'Сервис недоступен',
    }

    constructor(form){
        this.form = form;
        this.translator = form.dataset.translator;
        this.translatorId = this.urlNames[this.translator]
        this.readonly = form.dataset.readonly == 'true';
        this.autoSave = form.dataset.autosave == 'true';
        this.colorScheme = this.colorSchemes[this.translator];
        this.taskId = form.dataset.taskId;
        this.taskitemId = form.dataset.taskitemId;
        this.draft = form.querySelector('.js__content .js__editor-content').innerHTML

        if (this.autoSave && this.taskitemId){
            editorAutoSaveHandler(this)
        }

        // инициализировать все ace-поля редактора
        form.querySelectorAll('.js__editor').forEach((field, index) => {
            editorInitField(this, field)
        })

        var debugBtn = this.form.querySelector('.js__editor-btn-debug')
        debugBtn && debugBtn.addEventListener('click', (e) => {this.debug()}, false)

        var testsBtn = this.form.querySelector('.js__editor-btn-tests')
        testsBtn && testsBtn.addEventListener('click', (e) => {this.testing()}, false)

        var saveDraftBtn = form.querySelector('.js__editor-btn-save')
        saveDraftBtn && saveDraftBtn.addEventListener('click', (e) => {this.saveDraft()}, false)

        var createSolutionBtn = form.querySelector('.js__editor-btn-ready')
        createSolutionBtn && createSolutionBtn.addEventListener('click', (e) => {this.createSolution()}, false)
    }

    debug(){
        var content = this.form.querySelector('textarea.js__editor-content[name=content]').value
        if(content){
            var inputTextarea = this.form.querySelector('textarea.js__editor-content[name=input]'),
                that = this;
            if(this.translator == 'PostgreSQL'){
                var dbName = this.form.dataset.dbName
                var requestData = {code: content, name: dbName}
            } else {
                var input = inputTextarea ? inputTextarea.value : null
                var requestData = {code: content, data_in: input}
            }
            editorShowLoader(that, 'Отладка');
            editorDisableButtons(that);
            $.ajax({
                url: `/api/translators/${that.translatorId}/debug/`,
                type: 'POST',
                data: JSON.stringify(requestData),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                headers: {'Authorization': `Token ${window.authToken}`},
                statusCode:{
                    200: function(response){
                        editorShowMessage(that, 'Готово', 'success')
                        // Отображение результата работы программы
                        if(response.result){
                            that.form.querySelector('.js__output .js__editor-content').innerHTML = response.result
                            that.form.querySelector('.js__output').style.display = 'block'
                        } else {
                            that.form.querySelector('.js__output').style.display = 'none'
                        }
                        // Отображение текста ошибки
                        if(response.error){
                            that.form.querySelector('.js__error .js__editor-content').innerHTML = response.error
                            that.form.querySelector('.js__error').style.display = 'block'
                        } else {
                            that.form.querySelector('.js__error').style.display = 'none'
                        }
                        // инициализировать все ace-поля редактора
                        that.form.querySelectorAll('.js__editor').forEach((field, index) => {
                            editorInitField(that, field)
                        })
                        editorEnableButtons(that);
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    editorShowRequestError(that, XMLHttpRequest)
                }
            })
        }
    }

    testing(){
        var content = this.form.querySelector('textarea.js__editor-content[name=content]').value
        if(content){
            var inputTextarea = this.form.querySelector('textarea.js__editor-content[name=input]'),
                input = inputTextarea ? inputTextarea.value : null,
                that = this;

            editorShowLoader(that, 'Тестирование');
            editorDisableButtons(that);
            $.ajax({
                url: `/api/tasks/taskitem/${that.translatorId}/${that.taskitemId}/testing/`,
                type: 'POST',
                data: JSON.stringify({code: content}),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                headers: {'Authorization': `Token ${window.authToken}`},
                statusCode:{
                    200: function(response){
                        if(response.ok){
                            editorShowMessage(that, 'Тесты пройдены', 'success')
                        } else {
                            editorShowMessage(that, 'Тесты не пройдены', 'warning')
                        }
                        var table = document.querySelector('.js__form__tests-table')
                        if (that.translator != 'PostgreSQL'){
                            response.tests.forEach(function(test, index){
                                var tr = table.querySelector('.js__form__test-'+ index)
                                tr.classList.remove('success', 'unluck')
                                if(test.ok){
                                    tr.classList.add('success')
                                } else {
                                    tr.classList.add('unluck')
                                }
                                var testResult = '';
                                if(test.result && test.error){
                                    testResult = `${test.result}\n${test.error}`
                                } else if(test.result){
                                    testResult = test.result
                                } else if(test.error){
                                    testResult = test.error
                                }
                                var column = tr.querySelector('.js__form__test-result pre')
                                column.innerHTML = testResult
                                table.querySelectorAll('.js__form__test-result').forEach((elem) => {
                                    elem.classList.remove('hidden')
                                })
                            })
                        }
                        editorEnableButtons(that)
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    editorShowRequestError(that, XMLHttpRequest)
                }
            })
        }
    }

    createSolution(){
        var content = this.form.querySelector('textarea.js__editor-content[name=content]').value
        if(content){
            if (confirm('Вы уверены что хотите отправить решение задачи?')){
                var that = this;
                editorShowLoader(that, 'Отправляем решение');
                editorDisableButtons(that);
                $.ajax({
                    url: `/api/tasks/taskitem/${that.translatorId}/${that.taskitemId}/create-solution/`,
                    type: 'POST',
                    data: JSON.stringify({code: content}),
                    contentType: 'application/json; charset=utf-8',
                    dataType: 'json',
                    headers: {'Authorization': `Token ${window.authToken}`},
                    statusCode:{
                        200: function(response){
                            editorShowMessage(that, 'Готово', 'success');
                            editorShowSolutionsLink();
                            editorEnableButtons(that);
                        }
                    },
                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                        editorShowRequestError(that, XMLHttpRequest)
                    }
                })
            }
        }
    }

    saveDraft(){
        var content = this.form.querySelector('textarea.js__editor-content[name=content]').value,
            that = this;

        editorShowLoader(that, 'Сохранение');
        editorDisableButtons(that);
        $.ajax({
            url: `/api/tasks/${that.taskId}/draft/`,
            type: 'POST',
            data: JSON.stringify({content: content, translator: that.translator}),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            headers: {'Authorization': `Token ${window.authToken}`},
            statusCode:{
                200: function(response){
                    editorShowMessage(that, 'Готово', 'success')
                    editorEnableButtons(that);
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                editorShowRequestError(that, XMLHttpRequest)
            }
        })
    }
}
