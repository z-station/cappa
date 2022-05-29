var aceInit = function(readonly = false){
    var PYTHON38 = 'Python3.8',
        GCC74 = 'GCC7.4',
        PROLOG_D = 'Prolog-D'

    document.querySelectorAll('.js__editor').forEach(function(elem, index){
        var textarea = elem.querySelector('.js__editor-content'),
            editor = ace.edit(elem.querySelector('.js__editor-ace')),
            aceConfig = document.querySelector('.ace-config')
        aceConfig = aceConfig ? JSON.parse(aceConfig.innerHTML) : {}

        editor.setOption("showPrintMargin", false)     // убрать верт черту
        editor.setOption("maxLines", "Infinity")       // авто-высота
        editor.setHighlightActiveLine(false);          // убрать строку вделения
        editor.setReadOnly(textarea.getAttribute('readonly') || readonly)  // для чтения
        switch(aceConfig.translator || PYTHON38){
            case PYTHON38:
                editor.getSession().setMode("ace/mode/python"); break
            case GCC74:
                editor.getSession().setMode("ace/mode/c_cpp"); break
        }

        // вписать код из textarea в ace editor
        editor.setValue(textarea.textContent, - 1)

        // после записи кода в ace editor скопировать его в textarea
        editor.addEventListener('change', function(e){
            textarea.innerHTML = editor.getValue()
        })
    })
}