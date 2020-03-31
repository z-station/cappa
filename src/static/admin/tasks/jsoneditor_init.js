
$(document).ready(function(){
    var editor_selector = '#js__tests-container div';
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

    var editor = new JSONEditor(document.querySelector(editor_selector), options);
    editor.on('ready',function() {
        var jsonContent = JSON.parse(document.querySelector(textarea_selector).textContent)
        editor.setValue(jsonContent);
    });
    editor.on('change',function() {
        var textContent = JSON.stringify(editor.getValue());
        document.querySelector(textarea_selector).value = textContent;
    });
})
