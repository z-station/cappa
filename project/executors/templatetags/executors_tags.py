from django import template
from project.executors.forms import CodeForm
from project.executors.models import Code, CodeTest, UserSolution
from django.template.loader import render_to_string
import re


register = template.Library()
Context = template.Context


class ExecutorNode(template.Node):
    def __init__(self, treeitem, raw_str, row_num=None):
        self.row_num = row_num
        self.raw_str = template.Variable(raw_str)
        self.treeitem = template.Variable(treeitem)

        self.code_tag_pattern = re.compile(r'<\w+>[&nbsp;]*#code[0-9]+#[&nbsp;]*</\w+>|[&nbsp;]*#code[0-9]+#[&nbsp;]*')
        self.id_code_pattern = re.compile(r'[0-9]+')
        self.html_tag_pattern = re.compile(r'<\w+>')

    def render(self, context):

        # разделилим строку по блокам, которые будут между блоков кода
        row_num = self.row_num
        raw_str = self.raw_str.resolve(context)
        str_nodes = re.split(self.code_tag_pattern, raw_str)
        treeitem = self.treeitem.resolve(context)
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
                code = Code.objects.get(id=code_ids[i], treeitem=treeitem)
                tests = CodeTest.objects.filter(code=code)
                form = CodeForm(instance=code)
                user_solution, content_exist = None, bool(code.content)
                if not context["request"].user.is_anonymous:
                    user_solution = UserSolution.objects.filter(code_id=code.id, user_id=context["request"].user.id).first()
                    if user_solution:
                        last_changes = user_solution.last_changes
                        if last_changes:
                            form = CodeForm(instance=code, data={"input": last_changes['input'], "content": last_changes['content']})
                            content_exist = bool(last_changes['content'])
                code_context = {
                    "object": treeitem,
                    "executor_name": code.get_executor_name(),
                    "form": form,
                    "code_num": i if not row_num else row_num,
                    "code_id": code_ids[i],
                    "show_tests": code.show_tests,
                    "show_input": code.show_input,
                    "tests": tests,
                    "csrf_token": context["csrf_token"],
                    "user": context['request'].user,
                    "show_versions_btn": not context['request'].user.is_anonymous and tests,
                    "disable_btns": not content_exist,
                    "solution": user_solution,
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
                     '<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.4/ace.js"></script>\n' +\
                     '<script src="/static/js/ace/ace_ajax_submit.js"></script>\n' +\
                     '<script src=/static/js/prism.js></script>\n' + result_str
        return result_str


@register.tag("show_executors")
def show_executors(parser, token):
    """ Парсинг html-разметки в raw_str, поиск тегов кода #code<id>#
        и замена их на срендеренные шаблоны кода"""
    try:
        content = token.split_contents()
        treeitem = content[3]
        raw_str = content[1]
        row_num = content[5] if len(content) >= 5 else None
    except:
        raise template.TemplateSyntaxError("Invalid syntax. Use {% show_executors object.content for object %}")
    return ExecutorNode(treeitem, raw_str, row_num)
