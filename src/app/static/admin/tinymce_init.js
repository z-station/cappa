var initTinyMCE = function() {
    $('.tinymce').each(function () {
        var editor = tinymce.get($(this).attr('id'))
        if(editor)(
            editor.remove()
        )
        var $e = $(this);

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
    })
}