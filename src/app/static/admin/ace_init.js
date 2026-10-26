var colorSchemes = {
    'GCC7.4': 'ace/mode/c_cpp',
    'Prolog-D': 'ace/mode/prolog',
    'PostgreSQL': 'ace/mode/pgsql',
    'Pascal': 'ace/mode/pascal',
    'Php': 'ace/mode/php',
    'CSharp': 'ace/mode/csharp',
    'Java': 'ace/mode/java',
    'Rust186': 'ace/mode/rust',
    'Go123': 'ace/mode/golang',
    'Node20': 'ace/mode/javascript',
    'Java17': 'ace/mode/java',
    'Kotlin23': 'ace/mode/kotlin',
    'Ruby4': 'ace/mode/ruby',
    'Python314': 'ace/mode/python',
}

var aceInit = function(readonly = false, root = document){

    root.querySelectorAll('.js__editor').forEach(function(elem, index){
        var aceElem = elem.querySelector('.js__editor-ace')
        // шаблон пустой формы inline клонируется Django без экземпляра редактора,
        // поэтому ace в нём не создаётся
        if (aceElem.env || elem.closest('.empty-form')) {
            return
        }
        var textarea = elem.querySelector('.js__editor-content'),
            editor = ace.edit(aceElem),
            aceConfig = document.querySelector('.ace-config')
        aceConfig = aceConfig ? JSON.parse(aceConfig.innerHTML) : {}

        var colorScheme = this.colorSchemes[aceConfig.translator];

        editor.setOption("showPrintMargin", false)     // убрать верт черту
        editor.setOption("maxLines", "Infinity")       // авто-высота
        editor.setHighlightActiveLine(false);          // убрать строку вделения
        editor.setReadOnly(textarea.getAttribute('readonly') || readonly)  // для чтения
        editor.getSession().setMode(colorScheme);

        // вписать код из textarea в ace editor
        editor.setValue(textarea.textContent, - 1)

        // после записи кода в ace editor скопировать его в textarea
        editor.addEventListener('change', function(e){
            textarea.innerHTML = editor.getValue()
        })
    })
}