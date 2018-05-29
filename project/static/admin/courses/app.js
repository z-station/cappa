'use strict';


var templateHelper = function(templateName, data){
    return _.template($('#'+templateName).html(), data)
}

var csrftoken = $.cookie('csrftoken');

function addMessage(type, text) {
    var message = $('<li class="' + type + '">' + text + '</li>').hide();
    $(".messagelist").append(message);
    message.slideDown(500);

    setTimeout(function() {
        message.slideUp(500, function() {
            message.remove();
        });
    }, 5000);
}

var delete_tree_item = function(node, tree){
    var item_id = node.id
    $.ajax({
        url: 'delete/',
        method: "POST",
        data: {'item_id': item_id},
        beforeSend: function(xhr) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function(data) {
            if (data.status === 'OK') {
                tree.delete_node(node);
            }
            addMessage(data.type_message, data.message);
        }
    });
}

var move_tree_item = function(item_id, target_id, position){
    var moving = false;
    $.ajax({
        url: 'move/',
        method: "POST",
        data: {'item_id': item_id, 'position': position, 'target_id': target_id},
        async: false,
        beforeSend: function(xhr) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function(data){
            if (data.status === 'OK') {
                moving = true;
                addMessage(data.type_message, data.message);
            }
            else {
                moving = false;
                addMessage(data.type_message, data.message);
            }
        }
    });
    return moving;
}


var CatalogApp = {};

CatalogApp.ItemModel = Backbone.Model.extend({
    sync: function(method, model, options) {
        if (method === "update") {
            options.url = "edit/";
            options.beforeSend = function(xhr){
                if (!this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            };
            return Backbone.sync(method, model, options);
        }
    },
    parse : function(response, xhr) {
        //в админке открываем элементы курса
        if (response.status) {
            this.response = response;
            addMessage(response.type_message, response.message);
            return {};
        }
        else {
            return response;
        }
    },
    destroy: function() {
        this.trigger('destroy', this);
    }
});

CatalogApp.EditView = Backbone.View.extend({
    tagName: 'td',
    className: 'editable',
    template: 'field_tpl',
    edit_template: 'edit_tpl',
    events: {
        'click': 'activeEdit',
        'click .accept': 'acceptEdit',
        'click .cancel': 'cancelEdit',
        'click input, select': function(event){ event.stopPropagation(); }
    },
    initialize: function(options) {
        if(options.field_name){
            this.field_name = options.field_name;
        }
    },
    render: function() {
        this.$el.html(
            templateHelper(
                this.template,
                {field: this.model.get(this.field_name)}
            )
        );
        return this;
    },
    renderEdit: function() {
        this.$el.html(
            templateHelper(
                this.edit_template,
                {type: this.model.get(this.field_name).type,
                 value: this.model.get(this.field_name).value,
                 correct_values: this.model.get(this.field_name).correct_values}
            )
        );
        this.$el.removeClass('accept_value');
        this.$el.find('input').focus().val(this.model.get(this.field_name).value);
        return this;
    },
    close: function() {
        this.remove();
        this.unbind();
        this.undelegateEvents();
    },
    showError: function() {
        this.$el.addClass("error");
        this.renderEdit();
    },
    activeEdit: function(event){
        if (event.which == 1) {
            event.stopPropagation();
            this.renderEdit();
        }
    },
    cancelEdit: function(event){
        event.stopPropagation();
        this.render();
    },
    acceptEdit: function(event){
        event.stopPropagation();
        var new_value;
        if (this.model.get(this.field_name).type == 'checkbox') {
            if (this.$el.find('input').prop("checked")) new_value = 't';
            else new_value = 'f';
        } else if (this.model.get(this.field_name).type == 'select'){
            new_value = this.$el.find('select option:selected').val();
        } else {
            new_value = this.$el.find('input').val();
        }
        if (this.model.get(this.field_name).value != new_value) {
            this.model.set(this.field_name, {'editable': true, 'type': this.model.get(this.field_name).type, 'value': new_value, 'correct_values': this.model.get(this.field_name).correct_values});
            this.$el.addClass('accept_value');
        }
        this.render();
    }
});

CatalogApp.ItemView = Backbone.View.extend({
    tagName: 'tr',
    template: 'item_tpl',
    actionTemplate: 'action_tpl',
    events: {
        'click button.save': 'save',
        'mousedown button.change': 'change',
    },
    initialize: function(options){
        if(options.fields && options.tableEl){
            this.fields = options.fields;
            this.tableEl = options.tableEl;
        }
        this.edit = false;
        this.child_views = [];
        this.listenTo(this.model, 'change', this.allowSave);

    },
    render: function () {
        this.$el.empty();
        var self = this;
        _.each(this.fields, function(field){
            self.renderField(field[0]);
        });
        this.$el.append(templateHelper(this.actionTemplate, {'edit': this.edit}));
        return this;
    },
    renderField: function(field_name) {
        var field = this.model.get(field_name)
        if (field.editable) {
            this.edit = true;
            var editview = new CatalogApp.EditView({
                model: this.model,
                field_name: field_name
            });
            this.$el.append(editview.render().el);
            this.child_views.push(editview);
        }
        else {
            this.$el.append(
                templateHelper(
                    this.template,
                    {field: field}
                )
            );
        }
    },
    close: function() {
        this.removeChilds();
        this.remove();
        this.unbind();
        this.undelegateEvents();
    },
    removeChilds: function() {
        _.each(this.child_views, function(child_view){
            if (child_view.close){
                child_view.close();
            }
        });
        this.child_views = [];
    },
    allowSave: function() {
        this.$el.find("button.save").prop("disabled", false);
    },
    change: function(event) {
        if (event.which == 2) {
            window.open(this.model.get('link'), '_blank', "");
        }
        else {
            var win = window.open(this.model.get('link') + '?_popup=1', '', '');
            win.focus();
        }
    },
    save: function(event) {
        var self = this;
        this.model.save({},
            {
                success: function(model, response, options){
                    if (model.response.status === 'OK') {
                        self.removeChilds();
                        self.render();
                        self.tableEl.trigger('update');
                    }
                    else {
                        _.each(self.child_views, function(child_view){
                            if (child_view.field_name in model.response.errors){
                                child_view.showError();

                            }
                        });
                    }
                    model.response = {};
                }
            }

        );
    }
});

CatalogApp.ItemCollection = Backbone.Collection.extend({

    model: CatalogApp.ItemModel,
    initialize: function(options){
        if(options.parent_id){
            this.parent_id = options.parent_id;
        } else {
            this.parent_id = '';
        }
        this.fetch({reset: true});
    },
    url: function(){
        return 'list_children/' + this.parent_id
    },
    parse: function(response, xhr){
        this.fields = response.fields;
        return response.nodes
    },
    changeParentId: function(parent_id){
        this.parent_id = parent_id;
        this.fetch({reset: true});
    }
});

CatalogApp.ListItemsView = Backbone.View.extend({
    el: '#list_items_container',
    tableEl: '#list_table',
    tbodyEl: '#list_table tbody',
    template: 'table_items_tpl',
    initialize: function(options){
        var self = this;
        if(options.parent_id){
            this.parent_id = options.parent_id;
        } else {
            this.parent_id = '';
        }

        this.collection = new CatalogApp.ItemCollection({
            parent_id: this.parent_id
        });
        this.child_views = [];
        this.listenTo(this.collection, 'reset', this.render);
        this.listenTo(this, 'afterRender', this.initSorter);
    },
    render: function(){
        if (this.collection.fields) {
            this.$el.html(
                templateHelper(
                    this.template,
                    {fields: this.collection.fields}
                )
            );
            this.collection.each(function( item ){
                this.renderItem( item );
            }, this);
            this.trigger('afterRender');
        }
        return this
    },
    renderItem: function(item) {
        var itemview = new CatalogApp.ItemView({
            model: item,
            tableEl: $(this.tableEl),
            fields: this.collection.fields
        });
        $(this.tbodyEl).append(itemview.render().el);
        this.child_views.push(itemview);
    },
    reRender: function(options){
        this.destroy();
        this.collection.changeParentId(options.parent_id);
        return this
    },
    destroy: function() {
        $(this.tableEl).trigger("destroy");
        this.$el.empty();
        this.removeChilds();
    },
    removeChilds: function() {
        var item;
        while (item = this.collection.first()) {
          item.destroy();
        }
        _.each(this.child_views, function(child_view){
            if (child_view.close) child_view.close();
        });
        this.child_views = [];
    },
    initSorter: function(){
        self = this;
        $(document).ready(function(){
            $(self.tableEl).tablesorter({
                theme: 'ice',
                textExtraction:function(s){
                    if($(s).find('img').length == 0) return $(s).text();
                    return $(s).find('img').attr('alt');
                }
            });
        });
    }
});



 CatalogApp.TreeView = Backbone.View.extend({
    el: '#tree_container',
    rootEl: '#catalog-root-btn',
    searchId: '#tree_search',
    template: 'tree_tpl',
    initialize: function(options){
        var self = this;
        this.render();

        if(Modernizr.localstorage){

            this.resizeColumns($('#left-col'), localStorage['resize_width']);
        }

        $(this.rootEl).click(function(event){
            self.selectRoot();
        });

        $(window).resize(function(event){
            self.resizeColumns($("#left-col"));
        });

        $("#left-col").resizable({
            handles: 'e',
            resize: function(e, ui){
                self.resizeColumns(this);
            },
            stop: function(e, ui){
                if(Modernizr.localstorage){
                    localStorage['resize_width'] = $(this).width().toString();
                }
            }
        });
    },
    render: function(){
        this.initJsTree();
        return this;
    },
    resizeColumns: function(el, width){
        var parent_width = $(el).parent().outerWidth();
        var scroll = 16;
        if(width){
            var width = parseInt(width)
            $(el).width(width);
            $('#right-col').width(parent_width - parseInt(width)-scroll);
        } else {
            var left_width = $(el).outerWidth();
            $('#right-col').width(parent_width - left_width-scroll);
        }
    },
    initJsTree: function(){
        var self = this;
        this.$el.jstree({
            'core' : {
                'check_callback' : self.checkTreeCallbacks,
                'animation': 0,
                'data': {
                    'url': 'tree/',
                }

            },
            'types': {
                'leaf': {
                    'max_depth': '0',
                    'icon': 'jstree-file',
                },
            },
            'search': {
                'show_only_matches': true,
                'show_only_matches_children': true
            },
            'contextmenu': {
                'items': function(node){
                    var tree = self.$el.jstree(true);
                    var submenu = {};
                    _.each(node.data.add_links, function(link) {
                        var menu_item = {};
                        menu_item.label = link.label;
                        menu_item.action = function () {
                            self.addTreeItem(link.url);
                        }
                        submenu[link.label]=menu_item;
                    });

                    return {
                        'Remove': {
                            'separator_before': false,
                            'separator_after': false,
                            'label': 'Удалить',
                            'icon': 'delete-item',
                            'action': function (obj) {
                                self.deleteTreeItem(obj, node, tree);
                            }
                        },
                        'Edit': {
                            'label': 'Изменить',
                            'icon': 'edit-item',
                            'action': function () {
                                self.changeTreeItem(node);
                            }
                        },
                        'Add': {
                            'label': 'Добавить',
                            'submenu': submenu,
                            '_disabled': node.type === 'leaf'
                        },
                        'Watch': {
                            'separator_before': false,
                            'separator_after': false,
                            'label': 'Смотреть на сайте',
                            // 'icon': 'delete-item',
                            'action': function () {
                                self.watchTreeItem(node);
                            }
                        },
                    }
                }
            },
            'plugins' : [ 'dnd', 'search', 'types', 'contextmenu', 'state']
        });

        this.$el.on('select_node.jstree', function(e, data){
            self.renderListItemsView(data.node.id);
            $(self.rootEl).removeClass('active');
        });

        this.$el.on('ready.jstree', function(e, data){
            if (data.instance.get_selected().length == 0) {
                self.selectRoot();
            }
        });

        // search
        var to = false;
        $(self.searchId).keyup(function(e){
            if(e.which == 27){ //escape clear
                self.$el.jstree(true).clear_search();
                $(this).val('');
                return;
            }

            if(to) clearTimeout(to);
            to = setTimeout(function(){
                var v = $(self.searchId).val();
                self.$el.jstree(true).search(v);
            }, 300);
        });

        return this;
    },
    selectRoot: function() {
        this.$el.jstree().deselect_all();
        $(this.rootEl).addClass('active');
        this.renderListItemsView();
    },
    addTreeItem: function(url) {
        var win = window.open(url + '&_popup=1', '', '');
        win.focus();
    },
    changeTreeItem: function(node){
        var win = window.open(node.data.change_link + '?_popup=1' , '', '');
        win.focus();
    },
    deleteTreeItem: function(obj, node, tree){
        if(confirm('Вы уверенны? (если внутри обьекта есть другие обьекты они будут удалены)')){
            delete_tree_item(node, tree);
        }
    },
     watchTreeItem: function(node){
        var win = window.open(node.data.watch_link , '_blank');
        win.focus()
    },

    checkTreeCallbacks: function(operation, node, parent, position, more){
        if (operation === "move_node" && more && more.core) {
            var moving = false;
            if(parent.children.length !== 0){
                var i = 0;
                _.each(parent.children, function(child_id){
                    var target = this.get_node(child_id);
                    var parent_target = this.get_node(target.parent);
                    if (position === $.inArray(target.id, parent_target.children)) {
                        moving = move_tree_item(node.id, target.id, 'left');
                    }
                    if (i === parent.children.length - 1 && position === parent.children.length) {
                        moving = move_tree_item(node.id, target.id, 'right');
                    }
                    i++;
                }, this);
            } else {
                moving = move_tree_item(node.id, parent.id, 'last-child');
            }
            return moving;
        }
    },
    renderListItemsView: function(tree_id){
        if(this.listItemsView){
            this.listItemsView.reRender({
                parent_id: tree_id
            });
        } else {
            this.listItemsView = new CatalogApp.ListItemsView({
                parent_id: tree_id
            });
        }
    }
});

function dismissChangeRelatedObjectPopup(win) {
    win.close();
    location.reload();
}

function dismissAddRelatedObjectPopup(win) {
    win.close();
    location.reload();
}

$(document).ready(function(){
    var catalogTreeOneView = new CatalogApp.TreeView({});
});
