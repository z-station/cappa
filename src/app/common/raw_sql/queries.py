from typing import Union, Iterable, Tuple


class SqlQueryObject:

    sql_params = None
    sql_template = None

    def _get_sql_list(
        self,
        values: Union[str, int, Iterable],
        prefix: str
    ) -> Tuple[str, dict]:

        if not isinstance(values, Iterable):
            values = (values, )

        result = ', '.join([f'%({prefix}_{i})s' for i in range(len(values))])
        params = {f'{prefix}_{i}': value for i, value in enumerate(values)}
        return f'({result})', params

    def get_sql(self) -> Union[str, Tuple[str, dict]]:
        if self.sql_params:
            return self.sql_template, self.sql_params
        else:
            return self.sql_template
