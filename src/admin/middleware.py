# -*- coding: utf-8 -*-
from copy import deepcopy
from admin_reorder.middleware import ModelAdminReorder


class CustomModelAdminReorder(ModelAdminReorder):

    """ Кастомизован чтобы плагин выводил правильно список моделей из settings.ADMIN_REORDER """

    def find_app(self, app_config):
        for app in self.app_list:
            for model in app.get('models', []):
                app_model = '.'.join([app['app_label'], model['object_name']])
                # Кастомизованно тут
                if app_config['app'] == app['app_label'] or app_model in app_config.get('models', []):
                    return app

    def process_app(self, app_config):
        if 'app' not in app_config:
            raise NameError('ADMIN_REORDER list item must define '
                            'a "app" name. Got %s' % repr(app_config))

        app = self.find_app(app_config)
        if app:
            app = deepcopy(app)
            # Rename app
            if 'label' in app_config:
                app['name'] = app_config['label']

            # Process app models
            if 'models' in app_config:
                models_config = app_config.get('models')
                models = self.process_models(models_config)
                if models:
                    app['models'] = models
                else:
                    return None
            return app
