/***
    Скрипт для асинхронной отправки блоков кода на сервер и возврата результата исполнения кода
 ***/
;
var ace_ajax = {
    submit : function(form){
        var data = {},
            url = form.attr('action'),
            form_array = $(form).serializeArray();

        for (i=0; i<form_array.length; i++){
            var value = form_array[i].value;
            if(value){
                data[form_array[i].name] = value;
            }
        }
        if("content" in data){
            data["code_id"] = form.data("code_id");
            data["code_num"] = form.data("code_num");
            $.post(url, data, function(data, textStatus){
                $(form).replaceWith(data).show();
            });
        }
        return false;
    },
    check_tests : function(form){
        var data = {},
            url = form.data('tests-action'),
            form_array = $(form).serializeArray();

        for (i=0; i<form_array.length; i++) {
            var value = form_array[i].value;
            if (value) {
                data[form_array[i].name] = value;
            }
        }
        if("content" in data) {

            data["code_id"] = form.data("code_id");
            data["code_num"] = form.data("code_num");

            $.post(url, data, function (data, textStatus) {
                $(form).replaceWith(data).show();
            });
        }
        return false;
    }
};