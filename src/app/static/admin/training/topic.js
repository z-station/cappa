var django = django || {
    "jQuery": jQuery.noConflict(true)
};

var initTinyMCE = function($e) {
    if ($e.parents('.empty-form').length == 0) {  // Don't do empty inlines
      var mce_conf = $.parseJSON($e.attr('data-mce-conf'));

      // There is no way to pass a JavaScript function as an option
      // because all options are serialized as JSON.
      var fns = [
        'color_picker_callback',
        'file_browser_callback',
        'file_picker_callback',
        'images_dataimg_filter',
        'images_upload_handler',
        'paste_postprocess',
        'paste_preprocess',
        'setup',
        'urlconverter_callback',
      ];
      $.each(fns, function(i, fn_name) {
        if (typeof mce_conf[fn_name] != 'undefined') {
          if (mce_conf[fn_name].indexOf('(') != -1) {
            mce_conf[fn_name] = eval('(' + mce_conf[fn_name] + ')');
          }
          else {
            mce_conf[fn_name] = window[mce_conf[fn_name]];
          }
        }
      });

      var id = $e.attr('id');
      if ('elements' in mce_conf && mce_conf['mode'] == 'exact') {
        mce_conf['elements'] = id;
      }
      if ($e.attr('data-mce-gz-conf')) {
        tinyMCE_GZ.init($.parseJSON($e.attr('data-mce-gz-conf')));
      }
      if (!tinyMCE.editors[id]) {
        tinyMCE.init(mce_conf);
      }
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
        var lang = JSON.parse(document.querySelector('.ace-config').innerHTML).lang
        switch(lang){
            case 'python':
                editor.getSession().setMode("ace/mode/python"); break
            case 'cpp':
                editor.getSession().setMode("ace/mode/c_cpp"); break
            case 'csharp':
                editor.getSession().setMode("ace/mode/csharp"); break
        }

        // вписать код из textarea в ace editor
        editor.setValue(textarea.textContent, - 1)

        // после записи кода в ace editor скопировать его в textarea
        editor.addEventListener('change', function(e){
            textarea.innerHTML = editor.getValue()
        })
    })
}

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
        $('.tinymce').each(function () {
            try {
                var editor = tinymce.get($(this).attr('id')).remove()
                initTinyMCE($(this))
            } catch(e) {
                console.log($(this).attr('id'))
            }
        })
    })
})
