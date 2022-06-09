
var django = django || {
    "jQuery": jQuery.noConflict(true)
};


var toggleWidgetAceInput = function(e){
   if($(this).prop('checked')){
        $(this).parents('fieldset').find('.field-input').show()
   } else {
        $(this).parents('fieldset').find('.field-input').hide()
   }
}

var toggleWidget = function(e){
    var fieldset = $(this).parents('fieldset')
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
    }
}

$(document).ready(function(){
    aceInit()
    $('#_content-group .field-type select').each(toggleWidget)

    /* инициализировать ace для нового блока кода */
    $('#_content-group .add-row a').on('click', function(e){
         aceInit()
         $('#_content-group .field-type select').each(toggleWidget)
    })

    /* Показать/скрыть блок ввода редактора */
    $(document).on('change', '#_content-group .field-box.field-show_input input[type=checkbox]', toggleWidgetAceInput)

    /* Переключть тип виджета */
    $(document).on('change', '#_content-group .field-type select', toggleWidget)

    /* После сортировки обновить нужно виджет tinymce */
    window.addEventListener('sort', function(e){
        initTinyMCE()
    })
})
