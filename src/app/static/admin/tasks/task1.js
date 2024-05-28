
var jsonInit = function(){

    var json_field = document.querySelector('#js__tests-container div');
    if (json_field){
        var textarea_selector = '#js__tests-container #id_tests';
        var options = {
            schema: {
              "type": "array",
              "format": "table",
              "title": " ",
              "uniqueItems": true,
              "items": {
                "type": "object",
                "title": "Test",
                "properties": {
                  "data_in": {
                    "type": "string",
                    "format": "textarea",
                    "title": "Консольный ввод"
                  },
                  "data_out": {
                    "type": "string",
                    "format": "textarea",
                    "title": "Правильный ответ"
                  },
                  "visible": {
                    "type": "boolean",
                    "format": "checkbox",
                    "title": "Показывать",
                    "default": true
                  },
                  "enabled": {
                    "type": "boolean",
                    "format": "checkbox",
                    "title": "Проверять",
                    "default": true
                  }
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

window.addEventListener("load", function() {

    jsonInit();
    aceInit();

    /* инициализировать ace для нового блока кода */
    document.querySelector('#solution_examples-group .add-row a').addEventListener('click', function(e){
        aceInit()
    })
})
