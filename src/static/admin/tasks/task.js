var django = django || {
    "jQuery": jQuery.noConflict(true)
};

var jsonInit = function(){

    var json_field = document.querySelector('#js__tests-container div');
    if (json_field){
        var textarea_selector = '#js__tests-container #id_tests';
        var options = {
            schema: {
              "type": "array",
              "format": "table",
              "title": "Tests",
              "uniqueItems": true,
              "items": {
                "type": "object",
                "title": "Test",
                "properties": {
                  "input": {"type": "string", "format": "textarea"},
                  "output": { "type": "string", "format": "textarea"}
                }
              }
            }
        };
        var editor = new JSONEditor(json_field, options);
        editor.on('ready',function() {
            var jsonContent = JSON.parse(document.querySelector(textarea_selector).textContent)
            editor.setValue(jsonContent);
        });
        editor.on('change',function() {
            var textContent = JSON.stringify(editor.getValue());
            document.querySelector(textarea_selector).value = textContent;
        });
    }
}


var aceInit = function(){
    document.querySelectorAll('.js__editor').forEach(function(elem, index){
        var textarea = elem.querySelector('.js__editor-content')
        var editor = ace.edit(elem.querySelector('.js__editor-ace'))
        editor.setOption("showPrintMargin", false)     // убрать верт черту
        editor.setOption("maxLines", "Infinity")       // авто-высота
        editor.setHighlightActiveLine(false);          // убрать строку вделения
        editor.setReadOnly(textarea.getAttribute('readonly'))  // для чтения
        editor.getSession().setMode("ace/mode/python");

        // вписать код из textarea в ace editor
        editor.setValue(textarea.textContent, - 1)

        // после записи кода в ace editor скопировать его в textarea
        editor.addEventListener('change', function(e){
            textarea.innerHTML = editor.getValue()
        })
    })
}

$(document).ready(function(){
    jsonInit();
    aceInit();

    /* инициализировать ace для нового блока кода */
    $('#solution_examples-group .add-row a').on('click', function(e){
         aceInit()
    })

})
