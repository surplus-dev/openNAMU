from .tool.func import *

def api_bbs_w_post(sub_code : str = '') -> flask.Response:
    sub_code_split : list[str] = sub_code.split('-')
    if len(sub_code_split) < 2:
        sub_code_split = ['', '']

    conn : typing.Union[sqlite3.Connection, pymysql.connections.Connection]
    with get_db_connect() as conn:
        curs : typing.Union[sqlite3.Cursor, pymysql.cursors.Cursor] = conn.cursor()

        curs.execute(db_change('select set_name, set_data, set_code from bbs_data where set_id = ? and set_code = ?'), [sub_code_split[0], sub_code_split[1]])
        db_data : typing.Union[list[tuple[str, str, str]], None] = curs.fetchall()
        if not db_data:
            return flask.jsonify({})
        else:
            temp_id : str = ''
            temp_dict : dict[str, str] = {}

            for for_a in db_data:
                if temp_id != for_a[2]:
                    temp_id = for_a[2]
                    temp_dict['code'] = for_a[2]

                temp_dict[for_a[0]] = for_a[1]

            return flask.jsonify(temp_dict)