/***
     * Поле виджета состоит из div + textarea
     * div - для создания в нем js редактора Ace (нужен именно div)
     * textarea - это значение из редактора(код) которое запишется в бд
 ***/

function set_editor_field(editor_id){
    /** Инициализировать Ace-редактор в div **/
    var editor_content_container = $("#" + editor_id + "-content"),
        editor_container = $("#" + editor_id),
        readonly = editor_container.data("readonly"),
        editor = ace.edit(editor_id);
    editor.getSession().setMode("ace/mode/python");
    editor.setOption("showPrintMargin", false)   // убрать верт черту
    editor.setOption("maxLines", "Infinity");    // авто-высота
    editor.setHighlightActiveLine(false);        // убрать строку вделения
    editor.renderer.setShowGutter(false);        // отключить вывод номеров строк
    if(readonly){
        editor.setReadOnly(true);  // для чтения
    }
        //editor.renderer.$cursorLayer.element.style.display = "none" // скрыть позиицию курсора
        //editor_container.css("fontSize", '14px');
        //editor_container.css("background-color", '#f5f2f0');
        //editor_container.css("pointerEvents", 'none');

    /** при рендеринге страницы вписать код из textarea в Ace редактор **/
    var editor_content = editor_content_container.text() ? editor_content_container.text() : "";
    editor.setValue(editor_content, -   1);

    /** После записи кода в Ace скопировать его в textarea **/
    editor_container.on("focusout", function(){
        editor_content_container.val(editor.getValue());
    });
};

function update_editor_fields(){
    /** Для каждого div с класом инициализировать Ace-редактор **/
    $('.ace-editor').each(function(){
        set_editor_field($(this).attr("id"));
    });
};

function update_code_blocks_titles(){
    /** Удалить ненужный фрагмент из заголовков блоков кода **/
    $(document).find(".dynamic-executors-code-content_type-object_id h3").each(function(){
        $(this).find("b:first").remove();
    });
}

function change_new_code_block_title() {
    var new_code_block_title = $(document).find(".dynamic-executors-code-content_type-object_id h3").last();
    new_code_block_title.find("b:first").remove();
    new_code_block_title.find(".inline_label:first").html("Новый блок кода");
}

$(function(){

    /** При первоначальном рендеринге страницы **/
    update_editor_fields();
    update_code_blocks_titles();

    /** При добавлении элемента кода **/
    $('.add-row').on("click", function(){
        console.log("add");
        update_editor_fields();
        change_new_code_block_title();
    });
});