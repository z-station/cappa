#from src.langs.providers.python.tests import ProviderTestCase as PythonTestCase
from src.langs.providers.cpp.tests import ProviderTestCase as CppTestCase
from src.langs.providers.csharp.tests import ProviderTestCase as CSharpTestCase
from src.langs.providers.sql.tests import ProviderTestCase as SqlTestCase
if __name__ == '__main__':
    #PythonTestCase()
    CppTestCase()
    CSharpTestCase()
    SqlTestCase()