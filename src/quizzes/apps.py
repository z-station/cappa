from django.apps import AppConfig


class QuizzesAppConfig(AppConfig):
    name = 'src.quizzes'
    verbose_name = 'Самостоятельные работы'
    
    def ready(self):
        import src.quizzes.signals
