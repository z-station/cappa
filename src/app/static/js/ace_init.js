var aceInit = function(readonly = false){

    document.querySelectorAll('.js__editor').forEach(function(elem, index){
        var textarea = elem.querySelector('.js__editor-content'),
            editor = ace.edit(elem.querySelector('.js__editor-ace')),
            aceConfig = document.querySelector('.ace-config')
        aceConfig = aceConfig ? JSON.parse(aceConfig.innerHTML) : {}
        editor.setOption("showPrintMargin", false)     // убрать верт черту
        editor.setOption("maxLines", "Infinity")       // авто-высота
        editor.setHighlightActiveLine(false);          // убрать строку вделения
        editor.setReadOnly(true)  // для чтения
        editor.getSession().setMode('ace/mode/python');

        // вписать код из textarea в ace editor
        editor.setValue(textarea.textContent, - 1)

        // после записи кода в ace editor скопировать его в textarea
        editor.addEventListener('change', function(e){
            textarea.innerHTML = editor.getValue()
        })
    })
}