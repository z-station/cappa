from django import template
from project.executors.forms import CodeForm
from project.executors.models import Code, CodeTest, CodeSolution
from django.template.loader import render_to_string
import re


register = template.Library()
Context = template.Context


class ExecutorNode(template.Node):
    def __init__(self, obj, raw_str):
        self.raw_str = template.Variable(raw_str)
        self.obj = template.Variable(obj)

        self.code_tag_pattern = re.compile(r'<\w+>[&nbsp;]*#code[0-9]+#[&nbsp;]*</\w+>|[&nbsp;]*#code[0-9]+#[&nbsp;]*')
        self.id_code_pattern = re.compile(r'[0-9]+')
        self.html_tag_pattern = re.compile(r'<\w+>')

    def render(self, context):

        # разделилим строку по блокам, которые будут между блоков кода
        raw_str = self.raw_str.resolve(context)
        str_nodes = re.split(self.code_tag_pattern, raw_str)

        # чтобы порядок блоков текста кода был всегда один
        if raw_str.endswith("#"): str_nodes.append("")
        if raw_str.startswith("#"): str_nodes.insert(0, "")

        # Получили id кодов из тегов #code<id>#
        raw_code_tags = re.findall(self.code_tag_pattern, raw_str)
        code_ids = list()
        for raw_code_tag in raw_code_tags:
            code_tag = re.sub(self.html_tag_pattern, "", raw_code_tag)
            code_id = int(re.search(self.id_code_pattern, code_tag).group(0))
            code_ids.append(code_id)

        # формирование результативной строки путем подстановки на место тегов кода срендериных шаблонов кода
        result_str = ""
        for i in range(len(code_ids)):
            result_str += str_nodes[i]
            try:
                code = Code.objects.get(id=code_ids[i])
                tests = CodeTest.objects.filter(code=code)
                try:
                    code_solved = CodeSolution.objects.get(code=code, user=context["request"].user).success
                except CodeSolution.DoesNotExist:
                    code_solved = False

                code_context = {
                    "code_solved": code_solved,
                    "form": CodeForm(instance=code),
                    "code_num": i,
                    "csrf_token": context["csrf_token"],
                    "code_id": code_ids[i],
                    "tests": tests,
                }
                code_node = render_to_string(code.get_template(), code_context)
                result_str += code_node
            except Code.DoesNotExist:
                # если код с таким id не найден то пропускаем такой тег
                pass
        result_str += str_nodes.pop()

        # добавить скрипты иницализации ace-редактора
        result_str = '<link href="/static/css/ace/ace.css" type="text/css" media="all" rel="stylesheet" />\n' +\
                     '<link href="/static/css/prism.css" type="text/css" media="all" rel="stylesheet" />\n' +\
                     '<script src="/static/js/ace/ace_editor_v1.3.2.js"></script>\n' +\
                     '<script src="/static/js/ace/mode_python.js"></script>\n' +\
                     '<script src="/static/js/ace/ace_ajax_submit.js"></script>\n' +\
                     '<script src=/static/js/prism.js></script>\n' + result_str
        return result_str


@register.tag("show_executors")
def show_executors(parser, token):
    """ Парсинг html-разметки в raw_str, поиск тегов кода #code<id>#
        и замена их на срендеренные шаблоны кода"""
    try:
        content = token.split_contents()
        obj = content[3]
        raw_str = content[1]
    except:
        raise template.TemplateSyntaxError("Invalid syntax. Use {% show_with_executors [<raw_html_str>] %}")
    return ExecutorNode(obj, raw_str)
