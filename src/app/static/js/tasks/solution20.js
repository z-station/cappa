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

var solutionPage = function(e){
 // инициализировать ace-editor
    document.querySelectorAll('.js__editor').forEach(function(elem, index){
        var translator = elem.getAttribute('data-translator'),
            colorScheme = this.colorSchemes[translator],
            editor = ace.edit(elem.querySelector('.js__editor-ace'));

        editor.getSession().setMode(colorScheme)
        editor.setOption("showPrintMargin", false)     // убрать верт черту
        editor.setOption("maxLines", "Infinity")       // авто-высота
        editor.setHighlightActiveLine(false);          // убрать строку вделения
        editor.setReadOnly(true)                       // для чтения
    })
}

window.addEventListener('solutionPageLoaded', solutionPage)
