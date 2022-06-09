var PYTHON38 = 'Python3.8',
    GCC74 = 'GCC7.4',
    PROLOG_D = 'Prolog-D'

var solutionPage = function(e){
 // инициализировать ace-editor
    document.querySelectorAll('.js__editor').forEach(function(elem, index){
        var editor = ace.edit(elem.querySelector('.js__editor-ace'))
        editor.setOption("showPrintMargin", false)     // убрать верт черту
        editor.setOption("maxLines", "Infinity")       // авто-высота
        editor.setHighlightActiveLine(false);          // убрать строку вделения
        editor.setReadOnly(true)                       // для чтения
        switch(elem.getAttribute('data-translator')){
            case PYTHON38:
                editor.getSession().setMode("ace/mode/python"); break
            case GCC74:
                editor.getSession().setMode("ace/mode/c_cpp"); break
        }
    })
}

window.addEventListener('solutionPageLoaded', solutionPage)
