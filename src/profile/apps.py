from django.apps import AppConfig
from datetime import datetime
import pytz


class ProfileAppConfig(AppConfig):

    name = 'src.profile'

    def ready(self):
        from django.contrib.auth import get_user_model

        def cache_course_key(self, course):
            return 'user-%d-course-%d' % (self.id, course.id)

        def cache_quiz_key(self, quiz):
            return 'user-%d-quiz-%d' % (self.id, quiz.id)

        def get_course_solutions_data(self, course):
            from src.training.models import Solution
            data = {}
            for solution in Solution.objects.select_related('taskitem').filter(user=self, taskitem__topic__course=course):
                if solution.datetime is None:
                    dt = ''
                else:
                    dt = solution.datetime.strftime(format='%Y-%m-%d %H:%M:%S.%f')
                solution_data = {
                    'status': solution.status,
                    'score': solution.score,
                    'is_count': solution.is_count,
                    'datetime': dt,
                    'url': '%s?user=%d' % (solution.get_absolute_url(), self.id),
                }
                if solution.taskitem.manual_check:
                    solution_data['manual_check'] = {
                        'status': solution.manual_status
                    }
                data[f'taskitem__{solution.taskitem.id}'] = solution_data
            return data


        def get_quiz_solutions_data(self, quiz):
            from src.quizzes.models import Solution
            data = {}
            for solution in Solution.objects.select_related('taskitem').filter(user=self, taskitem__quiz=quiz):
                if solution.datetime is None:
                    dt = ''
                else:
                    dt = solution.datetime.strftime(format='%Y-%m-%d %H:%M:%S.%f')
                solution_data = {
                    'status': solution.status,
                    'score': solution.score,
                    'is_count': solution.is_count,
                    'datetime': dt,
                    'url': '%s?user=%d' % (solution.get_absolute_url(), self.id),
                }
                if solution.taskitem.manual_check:
                    solution_data['manual_check'] = {
                        'status': solution.manual_status
                    }
                data[f'taskitem__{solution.taskitem.id}'] = solution_data
            return data

        def get_cache_course_solutions_data(self, course):
            import json
            from django.core.cache import cache
            json_data = cache.get(self.cache_course_key(course))
            if not json_data:
                data = self.get_course_solutions_data(course)
                cache.set(self.cache_course_key(course), json.dumps(data, ensure_ascii=False))
            else:
                data = json.loads(json_data)
            return data
        
        
        def get_cache_quiz_solutions_data(self, quiz):
            import json
            from django.core.cache import cache
            json_data = cache.get(self.cache_quiz_key(quiz))
            if not json_data:
                data = self.get_quiz_solutions_data(quiz)
                cache.set(self.cache_quiz_key(quiz), json.dumps(data, ensure_ascii=False))
            else:
                data = json.loads(json_data)
            return data        

        def update_cache_course_solutions_data(self, course):
            from django.core.cache import cache
            cache.delete(self.cache_course_key(course))
            _ = self.get_cache_course_solutions_data(course)
            
        def update_cache_quiz_solutions_data(self, quiz):
            from django.core.cache import cache
            cache.delete(self.cache_quiz_key(quiz))
            _ = self.get_cache_quiz_solutions_data(quiz)

        def get_full_name(self):
            if self.last_name or self.first_name:
                return ('%s %s' % (self.last_name, self.first_name)).strip()
            else:
                return self.username

        def __str__(self):
            return self.get_full_name()

        UserModel = get_user_model()
        setattr(UserModel, 'cache_course_key', cache_course_key)
        setattr(UserModel, 'get_course_solutions_data', get_course_solutions_data)
        setattr(UserModel, 'get_cache_course_solutions_data', get_cache_course_solutions_data)
        setattr(UserModel, 'update_cache_course_solutions_data', update_cache_course_solutions_data)
        setattr(UserModel, 'cache_quiz_key', cache_quiz_key)
        setattr(UserModel, 'get_quiz_solutions_data', get_quiz_solutions_data)
        setattr(UserModel, 'get_cache_quiz_solutions_data', get_cache_quiz_solutions_data)
        setattr(UserModel, 'update_cache_quiz_solutions_data', update_cache_quiz_solutions_data)
        setattr(UserModel, '__str__', __str__)
        setattr(UserModel, 'get_full_name', get_full_name)
