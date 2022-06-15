var colorSchemes = {
    'Python3.8': 'ace/mode/python',
    'GCC7.4': 'ace/mode/c_cpp',
    'Prolog-D': 'ace/mode/prolog',
    'PostgreSQL': 'ace/mode/pgsql',
    'Pascal': 'ace/mode/pascal',
    'Php': 'ace/mode/php',
    'CSharp': 'ace/mode/csharp',
    'Java': 'ace/mode/java',
}

var aceInit = function(readonly = false){

    document.querySelectorAll('.js__editor').forEach(function(elem, index){
        var textarea = elem.querySelector('.js__editor-content'),
            editor = ace.edit(elem.querySelector('.js__editor-ace')),
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