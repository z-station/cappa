from src.langs.providers.python.tests import ProviderTestCase as PythonTestCase
from src.langs.providers.cpp.tests import ProviderTestCase as CppTestCase
from src.langs.providers.csharp.tests import ProviderTestCase as CSharpTestCase

if __name__ == '__main__':
    PythonTestCase()
    CppTestCase()
    CSharpTestCase()
