
$(function(){
    window.setInterval(function(){
        // auto save
        $('.editor-form').each(function(){
            let content = $(this).find('.ace-content textarea').first().val();
            let versions_btn = $(this).find('.control-btn.save-version').first();
            if(content != '' && versions_btn != undefined){
                ace_ajax.fast_save($(this), 'Автосохранение');
            }
        });
    }, 30000);

    $('.editor-form').each(function(){
        // disable control empty forms
        var form = $(this);
        form.find('.ace-content textarea').first().on('keyup', function(){
            if( $(this).val().trim().length == 0){
                ace_ajax.disableBtns(form)
            } else {
                ace_ajax.enableBtns(form)
            }
        })
    });

})
