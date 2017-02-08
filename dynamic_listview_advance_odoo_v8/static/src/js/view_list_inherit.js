view_list_inherit = function(instance) {
    var _t = instance.web._t,
    _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.web.View.include({
        load_view: function(context) {
            var self = this;
            var view_loaded_def;
            if (!this.options.new_window){
                new instance.web.Model('show.fields').get_func('action')({'model_name': self.model, 'user_id': self.session.uid}, 'select').then(function (result){
                    self.result = result;
                });
            }
            if (this.embedded_view) {
                view_loaded_def = $.Deferred();
                $.async_when().done(function() {
                    view_loaded_def.resolve(self.embedded_view);
                });
            }else {
                if (! this.view_type){
                    console.warn("view_type is not defined", this);
                    }
                view_loaded_def = instance.web.fields_view_get({
                    "model": this.dataset._model,
                    "view_id": this.view_id,
                    "view_type": this.view_type,
                    "toolbar": !!this.options.$sidebar,
                    "context": this.dataset.get_context(),
                });
            }
            return this.alive(view_loaded_def).then(function(r) {
                self.fields_view = r;
                self.render_fields_show();
                // add css classes that reflect the (absence of) access rights
                self.$el.addClass('oe_view')
                    .toggleClass('oe_cannot_create', !self.is_action_enabled('create'))
                    .toggleClass('oe_cannot_edit', !self.is_action_enabled('edit'))
                    .toggleClass('oe_cannot_delete', !self.is_action_enabled('delete'));
                return $.when(self.view_loading(r)).then(function() {
//                    self.render_fields_show();
                    self.trigger('view_loaded', r);
                });
            });
        },
        render_fields_show: function () {
            var self = this;
            if (this.fields_view.type == 'tree' && typeof(this.result) != 'undefined'){
                var Show_Field = new instance.web.Model('show.fields');
                QWeb.add_template("/dynamic_listview_advance_odoo_v8/static/src/xml/my_control.xml");
                    String.prototype.replaceAll = function(target, replacement) {return this.split(target).join(replacement); };
                    var data_show_field = this.result.data || {};
                    self.data_show_field = data_show_field;
                    var all_fields_of_model = this.result.fields || {};
                    self.all_fields_of_model = all_fields_of_model;

                    var fields = self.fields_view.fields;
                    var children = self.fields_view.arch.children;

                    this._visible_columns = _.filter(this.fields_view.arch.children, function (column) {return column.attrs.invisible != '1'})

                    var field_visible = data_show_field.hasOwnProperty('fields_show') && data_show_field['fields_show'] ? eval(data_show_field['fields_show'].replaceAll("u'", "'")) : _.pluck(_.pluck(self._visible_columns, 'attrs'), 'name');
                    var fields_sequence = data_show_field.hasOwnProperty('fields_sequence') && data_show_field['fields_sequence'] ? JSON.parse(data_show_field['fields_sequence']) : {}
                    var fields_string = data_show_field.hasOwnProperty('fields_string') && data_show_field['fields_string'] ? JSON.parse(data_show_field['fields_string']) : {}

                    var list_data = [];

                    for (var field_name in all_fields_of_model){
                        var field_obj = all_fields_of_model[field_name];
                        var data = {value: field_name, string: field_obj.string}
                        if (field_visible.indexOf(field_name) >= 0){
                            data['checked'] = 'checked';
                            if (fields_sequence.hasOwnProperty(field_name)){
                               data['sequence'] = fields_sequence[field_name];
                            }
                            if (fields_string.hasOwnProperty(field_name)){
                                data['string'] = fields_string[field_name];
                            }
                        }
                        list_data.push(data);
                    }
                    list_data = _.sortBy(list_data, function (o){return o.sequence});
                    self.data = {suggestion: list_data, attrs: {color: data_show_field.color || 'check-primary'}}

                    var field = {}, children = [], _fields_show = [];
                    for (var idx in field_visible){
                        var _field = field_visible[idx];
                        _fields_show.push({'value': _field, 'sequence': fields_sequence[_field] || 100});
                    }
                    _fields_show = _.sortBy(_fields_show, function (o){return o.sequence});

                    for (var _field in _fields_show){
                        _field = _fields_show[_field];
                        children.push({attrs: {modifiers: "", name: _field.value}, children: [], tag: "field"});
                        var f = all_fields_of_model[_field.value];
                        if (fields_string.hasOwnProperty(_field.value)){
                            f.string = fields_string[_field.value];
                        }
                        field[_field.value] = f;
                    }

                    // prepare children
                    var _children = self.fields_view.arch.children
                    for (var _field in _children){
                        if (_children.hasOwnProperty(_field)){
                            _field = _children[_field]
                            if ((!field.hasOwnProperty(_field.attrs.name) && _field.attrs.invisible == '1') || _field.attrs.name == 'state' || _field.attrs.name == 'virtual_available'){
                                field[_field.attrs.name] = all_fields_of_model[_field.attrs.name]
                                children.push(_field);
                            }
                        }
                    }
                    self.fields_view.fields = field;
                    self.fields_view.arch.children = children;
            }
        }
    });

   instance.web.ListView.include({
        load_list: function(data) {
            var self = this;
            this.fields_view = data;
            this.name = "" + this.fields_view.arch.attrs.string;

            if (this.fields_view.arch.attrs.colors) {
                this.colors = _(this.fields_view.arch.attrs.colors.split(';')).chain()
                    .compact()
                    .map(function(color_pair) {
                        var pair = color_pair.split(':'),
                            color = pair[0],
                            expr = pair[1];
                        return [color, py.parse(py.tokenize(expr)), expr];
                    }).value();
            }

            if (this.fields_view.arch.attrs.fonts) {
                this.fonts = _(this.fields_view.arch.attrs.fonts.split(';')).chain().compact()
                    .map(function(font_pair) {
                        var pair = font_pair.split(':'),
                            font = pair[0],
                            expr = pair[1];
                        return [font, py.parse(py.tokenize(expr)), expr];
                    }).value();
            }

            this.setup_columns(this.fields_view.fields, this.grouped);

            this.$el.html(QWeb.render(this._template, this));
            this.$el.addClass(this.fields_view.arch.attrs['class']);

            // Head hook
            // Selecting records
            this.$el.find('.oe_list_record_selector').click(function(){
                self.$el.find('.oe_list_record_selector input').prop('checked',
                    self.$el.find('.oe_list_record_selector').prop('checked')  || false);
                var selection = self.groups.get_selection();
                $(self.groups).trigger(
                    'selected', [selection.ids, selection.records]);
            });

            // Add button
            if (!this.$buttons) {
                this.$buttons = $(QWeb.render("ListView.buttons", {'widget':self}));
                if (this.options.$buttons) {
                    this.$buttons.appendTo(this.options.$buttons);
                } else {
                    this.$el.find('.oe_list_buttons').replaceWith(this.$buttons);
                }
                this.options.$buttons.find(".toggle_select_field").click(function() {
                    $(this).next().toggle();
                });
                this.options.$buttons.find(".sequence").change(function () {
                    $(this).parents('.setting_field').next('input').attr({'sequence': $(this).val()});
                });
                this.options.$buttons.find(".string_field").change(function () {
                    $(this).parents('.setting_field').next('input').attr({'string_field': $(this).val()});
                });
                this.options.$buttons.find("i[setting]").click(function () {
                    $(this).parent().find('.setting_field').toggle();
                });
                this.options.$buttons.find(".update_setting_field").click(function () {
                    var parent = $(this).parents('.setting_field');
                    parent.next().attr({string_field: parent.find('.string_field').val(), 'sequence': parent.find('.sequence').val()})
                    parent.toggle();
                });
                this.setting_fields_show(this.options.$buttons);
                this.update_show_fields(this.options.$buttons);
                this.$buttons.find('.oe_list_add')
                        .click(this.proxy('do_add_record'))
                        .prop('disabled', this.grouped);
            }

            // Pager
            if (!this.$pager) {
                this.$pager = $(QWeb.render("ListView.pager", {'widget':self}));
                if (this.options.$buttons) {
                    this.$pager.appendTo(this.options.$pager);
                } else {
                    this.$el.find('.oe_list_pager').replaceWith(this.$pager);
                }

                this.$pager
                    .on('click', 'a[data-pager-action]', function () {
                        var $this = $(this);
                        var max_page_index = Math.ceil(self.dataset.size() / self.limit()) - 1;
                        switch ($this.data('pager-action')) {
                            case 'first':
                                self.page = 0;
                                break;
                            case 'last':
                                self.page = max_page_index;
                                break;
                            case 'next':
                                self.page += 1;
                                break;
                            case 'previous':
                                self.page -= 1;
                                break;
                        }
                        if (self.page < 0) {
                            self.page = max_page_index;
                        } else if (self.page > max_page_index) {
                            self.page = 0;
                        }
                        self.reload_content();
                    }).find('.oe_list_pager_state')
                        .click(function (e) {
                            e.stopPropagation();
                            var $this = $(this);

                            var $select = $('<select>')
                                .appendTo($this.empty())
                                .click(function (e) {e.stopPropagation();})
                                .append('<option value="80">80</option>' +
                                        '<option value="200">200</option>' +
                                        '<option value="500">500</option>' +
                                        '<option value="2000">2000</option>' +
                                        '<option value="NaN">' + _t("Unlimited") + '</option>')
                                .change(function () {
                                    var val = parseInt($select.val(), 10);
                                    self._limit = (isNaN(val) ? null : val);
                                    self.page = 0;
                                    self.reload_content();
                                }).blur(function() {
                                    $(this).trigger('change');
                                })
                                .val(self._limit || 'NaN');
                        });
            }

            // Sidebar
            if (!this.sidebar && this.options.$sidebar) {
                this.sidebar = new instance.web.Sidebar(this);
                this.sidebar.appendTo(this.options.$sidebar);
                this.sidebar.add_items('other', _.compact([
                    { label: _t("Export"), callback: this.on_sidebar_export },
                    self.is_action_enabled('delete') && { label: _t('Delete'), callback: this.do_delete_selected }
                ]));
                this.sidebar.add_toolbar(this.fields_view.toolbar);
                this.sidebar.$el.hide();
            }
            //Sort
            var default_order = this.fields_view.arch.attrs.default_order,
                unsorted = !this.dataset._sort.length;
            if (unsorted && default_order && !this.grouped) {
                this.dataset.set_sort(default_order.split(','));
            }

            if(this.dataset._sort.length){
                if(this.dataset._sort[0].indexOf('-') == -1){
                    this.$el.find('th[data-id=' + this.dataset._sort[0] + ']').addClass("sortdown");
                }else {
                    this.$el.find('th[data-id=' + this.dataset._sort[0].split('-')[1] + ']').addClass("sortup");
                }
            }
            this.trigger('list_view_loaded', data, this.grouped);
        },
        update_show_fields: function (node) {
            var self = this;
            node.find('a[action="update"]').click(function () {
                var fields = []
                var sequence = {}
                var fields_string = {}
                self.$buttons.find('.choose_field_show').find('.suggestion input:checked').each(function () {
                    fields.push($(this).val());
                    var _seq = $(this).attr('sequence') || false;
                    if (_seq){
                        sequence[$(this).attr('id')] = parseInt(_seq);
                    }
                    var _str = $(this).attr('string_field') || false;
                    if (_str){
                        fields_string[$(this).attr('id')] = _str;
                    }
                });
                new instance.web.Model('show.fields').call('action', [{'model_name': self.model, 'fields_show': fields,
                'user_id': self.session.uid, 'fields_sequence': JSON.stringify(sequence),
                'fields_string': JSON.stringify(fields_string)}, 'update']).then(function (result) {
                    location.reload();
                });
            });
        },
        setting_fields_show: function (node) {
            var self = this;
            node.find(".fields_setting").click(function () {
                var $form_show = $(QWeb.render('FormShowField', self.data_show_field));
//  set data for form
                $form_show.find('input[name="color"][value="'+(self.data_show_field.color || 'check-primary')+'"]').attr('checked', true);
                if (self.data_show_field.all_user){
                    $form_show.find('#all_user').attr('checked', true);
                }
                if (self.data_show_field.color_for_list){
                    $form_show.find('#color_for_list').attr('checked', true);
                }
//                insert to body
                $form_show.insertAfter('body');

//                events
                $('.close-field-show').click(function () {
                    $form_show.remove();
                });
                $form_show.find('a[action="update"]').click(function () {
                    var data = {color: $form_show.find('input[name="color"]:checked').val(),
                                all_user: false, color_for_list: false, model_name: self.model,
                                user_id: self.session.uid}
                    if ($form_show.find('#all_user').is(':checked')){
                        data.all_user = true;
                    }
                    if ($form_show.find('#color_for_list').is(':checked')){
                        data.color_for_list = true;
                    }
                    new instance.web.Model('show.fields').call('action', [data, 'update']).then(function (result) {
                        location.reload();
                    });
                });
            });
        }
    });
};

openerp.dynamic_listview_advance_odoo_v8 = function(instance) {
    view_list_inherit(instance);
};
