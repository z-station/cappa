import re
from ..base import BaseProvider
from src.tasks.models import Task
import os.path
from src.utils.editor import clear_text
import sqlite3
import shutil


def create_db(db1: str, db2: str):                             #копирование тестовой б.д. в б.д. пользователя
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db1_path = os.path.join(current_dir, "tests_db\\" + db1)     #путь к тестовой б.д.
    db2_path = os.path.join(current_dir, "users_db\\" + db2)     #путь к б.д. пользователя
    try:
        os.remove(db2_path)
    except:
        pass
    shutil.copy2(db1_path, db2_path)

class Provider(BaseProvider):
    @classmethod
    def _get_decoded(cls, stdout: bytes, stderr: bytes) -> tuple:

        """ Преобразует bytes (вывод интерпретатора) в unicode, удаляет лишние смиволы из вывода """

        output = stdout.decode()
        error = re.sub(r'\s*File.+.py",', "", stderr.decode()) if stderr else ''
        return output, error

    @classmethod
    def debug(cls, input: str, content: str,**kwargs) -> dict:

        if ".db" in input:           #если б.д. уточнена пользователем
            stdin=input
        else:                         #иначе выполнять запрос на первой б.д.
            stdin="bd_1.db"
        error=""
        output = ""
        try:
            create_db(stdin,kwargs['session_key']+".db")
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "users_db\\"+kwargs['session_key']+".db")
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute(content)
        except Exception as e:
            error = str(e)
        else:
            for res in c.fetchall():
                output += str(res)+"\n"
            c.close()
        return {
            'output': output,
            'error': error
        }

    @classmethod
    def check_tests(cls, content: str, task: Task, **kwargs) -> dict:
        compare_method_name = f'_compare_{task.output_type}'
        compare_method = getattr(cls, compare_method_name)
        tests_data = []
        tests_num_success = 0
        ind = 0                      #индекс б.д. текущего теста
        for test in task.tests:    #почему несколько файлов б.д.
            ind += 1
            error = ""
            output = ""
            success = False
            try:
                create_db("bd_"+str(ind)+".db", kwargs['session_key'] + ".db")      #все б.д. назвать bd_1, bd_2 и т.д.
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(BASE_DIR, "users_db\\"+kwargs['session_key']+".db")  #путь к б.д. пользователя
                conn = sqlite3.connect(db_path)                                     #стандартное выполнение запроса в sqlite3
                c = conn.cursor()
                c.execute(content)
                conn.commit()
            except Exception as e:
                error=str(e)
            else:
                if "sqlselect" not in compare_method_name:        #не изм. б.д. запрос
                    for res in c.fetchall():
                        output += str(res)+"\n"
                    success = compare_method(
                        etalon=clear_text(test['output']),
                        val=clear_text(output)
                    )
                    c.close()
                else:                                              #изм. б.д. запрос
                    c.execute(test['input'])
                    for res in c.fetchall():
                        output += str(res)+"\n"
                    c.close()
                    success = compare_method(
                        etalon=test["output"],
                        val=output
                    )

            tests_num_success += success

            tests_data.append({
                "output": output,
                "error": error,
                "success": success
            })

        tests_num = len(task.tests)
        return {
            'num': tests_num,
            'num_success': tests_num_success,
            'data': tests_data,
            'success': tests_num == tests_num_success,
        }
