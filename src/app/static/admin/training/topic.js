
var django = django || {
    "jQuery": jQuery.noConflict(true)
};


var toggleWidgetAceInput = function(e){
   var fieldset = $(this).closest('.inline-related')
   var isAce = fieldset.find('.field-type select').val() == 'ace'
   if(isAce && $(this).prop('checked')){
        fieldset.find('.field-input').show()
        resizeAce(fieldset)
   } else {
        fieldset.find('.field-input').hide()
   }
}

var toggleWidget = function(e){
    var fieldset = $(this).closest('.inline-related')
    if($(this).val() == 'text'){
        fieldset.find('.field-show_input').hide()
        fieldset.find('.field-show_debug').hide()
        fieldset.find('.field-readonly').hide()
        fieldset.find('.field-input').hide()
        fieldset.find('.field-content').hide()
        fieldset.find('.field-text').show()
    } else if($(this).val() == 'ace'){
        if(fieldset.find('.field-show_input input[type=checkbox]').prop('checked')){
            fieldset.find('.field-input').show()
        } else {
            fieldset.find('.field-input').hide()
        }
        fieldset.find('.field-show_debug').show()
        fieldset.find('.field-readonly').show()
        fieldset.find('.field-show_input').show()
        fieldset.find('.field-content').show()
        fieldset.find('.field-text').hide()
        resizeAce(fieldset)
    }
}

/* ace, созданный в скрытом блоке, имеет нулевой размер до вызова resize */
var resizeAce = function(fieldset){
    fieldset.find('.js__editor-ace').each(function(){
        if(this.env){
            this.env.editor.resize(true)
        }
    })
}

$(document).ready(function(){
    aceInit()
    $('#_content-group .field-type select').each(toggleWidget)

    /* инициализировать ace для нового блока кода */
    django.jQuery(document).on('formset:added', function(e, row, prefix){
        if(prefix !== '_content'){
            return
        }
        aceInit(false, row[0])
        $(row[0]).find('.field-type select').each(toggleWidget)
    })

    /* Показать/скрыть блок ввода редактора */
    $(document).on('change', '#_content-group .field-show_input input[type=checkbox]', toggleWidgetAceInput)

    /* Переключть тип виджета */
    $(document).on('change', '#_content-group .field-type select', toggleWidget)

    /* После сортировки обновить нужно виджет tinymce */
    window.addEventListener('sort', function(e){
        initTinyMCE()
    })
})
