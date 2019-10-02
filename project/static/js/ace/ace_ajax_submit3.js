/***
    Скрипт для асинхронной отправки блоков кода на сервер и возврата результата исполнения кода
 ***/
;
var ace_ajax = {
    hideMsg: function(form){
        $(form).find('.msg').addClass('hide');
    },
    disableBtns: function(form){
        $(form).find('.control-btn').addClass('disabled');
    },
    enableBtns: function(form){
        $(form).find('.control-btn').removeClass('disabled');
    },
    enableVersionsBtn: function(form){
        $(form).find('.control-btn.versions').removeClass('not-versions');
    },
    showLoader: function(form, msg){
        this.hideMsg(form);
        $(form).find('.loader').first().removeClass('hide');
        $(form).find('.msg-loader').first().html(msg).removeClass('hide');
    },
    showMsg(form, msg, status){
        this.hideMsg(form)
        switch(status){
            case 'success':
                $(form).find('.msg-success').first().html(msg).removeClass('hide');
                break
            case 'warning':
                $(form).find('.msg-warning').first().html(msg).removeClass('hide');
                break
            case 'error':
                $(form).find('.msg-error').first().html(msg).removeClass('hide');
                break
        }
        setTimeout(function(){ ace_ajax.hideMsg(form) }, 10000);
    },
    serializeForm(form){
        var data = {},
            form_array = form.serializeArray();

        for (i=0; i<form_array.length; i++){
            var value = form_array[i].value;
            if(value){
                data[form_array[i].name] = value;
            }
        }
        data["code_id"] = form.data("code_id");
        data["code_num"] = form.data("code_num");
        return data
    },
    execute : function(form){
        this.disableBtns(form);
        this.showLoader(form, 'Отладка');
        $.post(form.attr('action'), this.serializeForm(form), function(response, textStatus){
            ace_ajax.showMsg(form, response.msg, response.status);
            form.find('.ace-input div').first().replaceWith(response.input).show();
            form.find('.ace-content div').first().replaceWith(response.content).show();
            form.find('.ace-output div').first().replaceWith(response.output).show();
            form.find('.ace-error div').first().replaceWith(response.error).show();
            update_editor_fields();
            ace_ajax.enableBtns(form);
        });
        return false;
    },
    check_tests : function(form, testsContainer){
        this.disableBtns(form);
        this.showLoader(form, 'Тестирование');
        $.post(form.data('tests-action'), this.serializeForm(form), function(response, textStatus){
            ace_ajax.showMsg(form, response.msg, response.status);
            form.find('.ace-input div').first().replaceWith(response.input).show();
            form.find('.ace-content div').first().replaceWith(response.content).show();
            form.find('.ace-output div').first().replaceWith(response.output).show();
            form.find('.ace-error div').first().replaceWith(response.error).show();
            testsContainer.find('table').first().replaceWith(response.tests).show();
            update_editor_fields();
            ace_ajax.enableBtns(form);
            ace_ajax.enableVersionsBtn(form);
            if(response.success){
                $('h1 .success').show()
            }
        });
        return false;
    },
    save_version: function(form){
        this.disableBtns(form);
        this.showLoader(form, 'Сохранение')
        $.post(form.data('save-version-action'), this.serializeForm(form), function(response, textStatus){
            ace_ajax.showMsg(form, response.msg, response.status);
            ace_ajax.enableBtns(form);
            ace_ajax.enableVersionsBtn(form);
        });
        return false;

    },
    fast_save: function(form, msg='Сохранение'){
        this.disableBtns(form);
        this.showLoader(form, msg);
        $.post(form.data('save-version-action'), this.serializeForm(form), function(response, textStatus){
            ace_ajax.showMsg(form, 'Изменения сохранены', response.status);
            ace_ajax.enableBtns(form);
            ace_ajax.enableVersionsBtn(form);
        });
        return false;
    }
};
