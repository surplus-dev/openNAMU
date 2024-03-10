from .tool.func import *

def login_register_submit_2():
    with get_db_connect() as conn:
        curs = conn.cursor()

        session_reset_list = ['submit_id', 'submit_pw', 'submit_email']

        if not 'submit_id' in flask.session:
            for for_a in session_reset_list:
                flask.session.pop(for_a, None)

            return redirect(conn, '/register')

        curs.execute(db_change('select data from other where name = "approval_question"'))
        sql_data = curs.fetchall()
        if not sql_data:
            for for_a in session_reset_list:
                flask.session.pop(for_a, None)

            return redirect(conn, '/register')

        data_que = sql_data[0][0]

        if do_user_name_check(conn, flask.session['submit_id']) == 1:
            for for_a in session_reset_list:
                flask.session.pop(for_a, None)
        
            return redirect(conn, '/register')

        if flask.request.method == 'POST':
            curs.execute(db_change('select data from other where name = "encode"'))
            data_encode = curs.fetchall()
            data_encode = data_encode[0][0]

            user_app_data = {}
            user_app_data['id'] = flask.session['submit_id']
            user_app_data['pw'] = pw_encode(conn, flask.session['submit_pw'])
            user_app_data['encode'] = data_encode
            user_app_data['question'] = data_que
            user_app_data['answer'] = flask.request.form.get('answer', '')

            if 'submit_email' in flask.session:
                user_app_data['email'] = flask.session['submit_email']
            else:
                user_app_data['email'] = ''

            for for_a in session_reset_list:
                flask.session.pop(for_a, None)

            curs.execute(db_change("insert into user_set (id, name, data) values (?, ?, ?)"), [user_app_data['id'], 'application', json.dumps(user_app_data)])
            conn.commit()

            for for_a in get_admin_list(conn):
                add_alarm(conn, for_a, user_app_data['id'], '<a href="/app_submit">' + get_lang(conn, 'new_application') + '</a>')

            return re_error(conn, '/error/43')
        else:
            return easy_minify(conn, flask.render_template(skin_check(conn),
                imp = [get_lang(conn, 'approval_question'), wiki_set(conn), wiki_custom(conn), wiki_css([0, 0])],
                data = '''
                    <form method="post">
                        ''' + get_lang(conn, 'approval_question') + ' : ' + data_que + '''
                        <hr class="main_hr">
                        <input placeholder="''' + get_lang(conn, 'approval_question') + '''" name="answer">
                        <hr class="main_hr">
                        <button type="submit">''' + get_lang(conn, 'save') + '''</button>
                    </form>
                ''',
                menu = [['user', get_lang(conn, 'return')]]
            ))