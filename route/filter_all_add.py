from .tool.func import *

def filter_all_add(tool, name = None):
    with get_db_connect() as conn:
        curs = conn.cursor()

        if not name and tool == 'edit_filter':
            return redirect(conn, '/manager/9')

        if flask.request.method == 'POST':
            if admin_check(conn) != 1:
                return re_error(conn, '/error/3')

            title = flask.request.form.get('title', 'test')
            if tool in ('inter_wiki', 'outer_link'):
                link = flask.request.form.get('link', 'test')
                icon = flask.request.form.get('icon', '')
                inter_type = flask.request.form.get('inter_type', '')

                curs.execute(db_change("delete from html_filter where html = ? and kind = ?"), [title, tool])
                curs.execute(db_change('insert into html_filter (html, plus, plus_t, kind) values (?, ?, ?, ?)'), [title, link, icon, tool])
                if tool == 'inter_wiki':
                    curs.execute(db_change("delete from html_filter where html = ? and kind = 'inter_wiki_sub'"), [title])
                    curs.execute(db_change('insert into html_filter (html, plus, plus_t, kind) values (?, "inter_wiki_type", ?, "inter_wiki_sub")'), [title, inter_type])
                
                admin_check(conn, None, tool + ' edit')
            elif tool == 'edit_filter':
                sec = flask.request.form.get('second', '0')
                end = 'X' if sec == '0' else sec

                content = flask.request.form.get('content', 'test')
                try:
                    re.compile(content)
                except:
                    return re_error(conn, '/error/23')
                
                curs.execute(db_change("delete from html_filter where html = ? and kind = 'regex_filter'"), [name])
                curs.execute(db_change("insert into html_filter (html, plus, plus_t, kind) values (?, ?, ?, 'regex_filter')"), [name, content, end])
                admin_check(conn, None, 'edit_filter edit')
            elif tool == 'document':
                post_name = flask.request.form.get('name', '')
                if post_name == '':
                    return redirect(conn, '/filter/document')
            
                post_acl = flask.request.form.get('acl', '')
                post_regex = flask.request.form.get('regex', '')
                try:
                    re.compile(post_regex)
                except:
                    return re_error(conn, '/error/23')
                
                curs.execute(db_change('insert into html_filter (html, kind, plus, plus_t) values (?, "document", ?, ?)'), [post_name, post_regex, post_acl])
                admin_check(conn, None, 'document_filter edit')
            else:
                plus_d = ''
                if tool == 'name_filter':
                    try:
                        re.compile(title)
                    except:
                        return re_error(conn, '/error/23')

                    admin_check(conn, None, 'name_filter edit')
                    type_d = 'name'
                elif tool == 'file_filter':
                    try:
                        re.compile(title)
                    except:
                        return re_error(conn, '/error/23')

                    admin_check(conn, None, 'file_filter edit')
                    type_d = 'file'
                elif tool == 'email_filter':
                    admin_check(conn, None, 'email_filter edit')
                    type_d = 'email'
                elif tool == 'image_license':
                    admin_check(conn, None, 'image_license edit')
                    type_d = 'image_license'
                elif tool == 'extension_filter':
                    admin_check(conn, None, 'extension_filter edit')
                    type_d = 'extension'
                elif tool == 'template':
                    admin_check(conn, None, 'template_document edit')
                    type_d = 'template'
                    plus_d = flask.request.form.get('exp', 'test')
                else:
                    admin_check(conn, None, 'edit_top edit')
                    type_d = 'edit_top'
                    plus_d = flask.request.form.get('markup', 'test')

                if name:
                    curs.execute(db_change("delete from html_filter where html = ? and kind = ?"), [name, type_d])

                curs.execute(db_change('insert into html_filter (html, kind, plus, plus_t) values (?, ?, ?, ?)'), [title, type_d, plus_d, ''])

            conn.commit()

            return redirect(conn, '/filter/' + tool)
        else:
            get_sub = 0
            stat = 'disabled' if admin_check(conn) != 1 else ''
            name = name if name else ''

            if tool in ('inter_wiki', 'outer_link'):
                value = ['', '', '']
                if name != '':
                    curs.execute(db_change("select html, plus, plus_t from html_filter where html = ? and kind = ?"), [name, tool])
                    exist = curs.fetchall()
                    value = exist[0] if exist else value

                select = ''
                if tool == 'inter_wiki':
                    ex = 'https://namu.wiki/w/'

                    select = ['', '']
                    curs.execute(db_change("select plus_t from html_filter where kind = 'inter_wiki_sub' and html = ?"), [name])
                    db_data = curs.fetchall()
                    if db_data and db_data[0][0] == 'under_bar':
                        select = ['', 'selected']

                    select = '''
                        <hr class="main_hr">
                        ''' + get_lang(conn, 'inter_wiki_space_change') + '''
                        <hr class="main_hr">
                        <select name="inter_type">
                            <option ''' + select[0] + ''' value="url_encode">%20</option>
                            <option ''' + select[1] + ''' value="under_bar">_</option>
                        </select>
                    '''
                else:
                    ex = 'youtube.com'

                title = get_lang(conn, 'interwiki_add') if tool == 'inter_wiki' else get_lang(conn, 'outer_link_add')
                form_data = '''
                    ''' + get_lang(conn, 'name') + '''
                    <hr class="main_hr">
                    <input value="''' + html.escape(value[0]) + '''" type="text" name="title">
                    <hr class="main_hr">
                    ''' + get_lang(conn, 'link') + ''' (EX : ''' + ex + ''')
                    <hr class="main_hr">
                    <input value="''' + html.escape(value[1]) + '''" type="text" name="link">
                    <hr class="main_hr">
                    ''' + get_lang(conn, 'icon') + ''' (''' + ('HTML' if tool == 'inter_wiki' else get_lang(conn, 'html_or_link')) + ''') (''' + get_lang(conn, 'link') + ' - EX' + ''' : /image/Test.svg)
                    <hr class="main_hr">
                    <input value="''' + html.escape(value[2]) + '''" type="text" name="icon">
                    ''' + select + '''
                '''
            elif tool == 'edit_filter':            
                curs.execute(db_change("select plus, plus_t from html_filter where html = ? and kind = 'regex_filter'"), [name])
                exist = curs.fetchall()
                if exist:
                    textarea = exist[0][0]
                    time_data = '' if exist[0][1] == 'X' else exist[0][1]
                else:
                    textarea = ''
                    time_data = ''

                insert_data = ''
                if stat == '':
                    t_data = [
                        ['86400', get_lang(conn, '1_day')],
                        ['432000', get_lang(conn, '5_day')],
                        ['2592000', get_lang(conn, '30_day')],
                        ['15552000', get_lang(conn, '180_day')],
                        ['31104000', get_lang(conn, '360_day')],
                        ['0', get_lang(conn, 'limitless')]
                    ]
                    insert_data += ''.join(['<a href="javascript:opennamu_insert_v(\'second\', \'' + for_a[0] + '\')">(' + for_a[1] + ')</a> ' for for_a in t_data])

                title = get_lang(conn, 'edit_filter_add')
                form_data = '''
                    ''' + insert_data + '''
                    <hr class="main_hr">
                    <input placeholder="''' + get_lang(conn, 'second') + '''" id="second" name="second" type="text" value="''' + html.escape(time_data) + '''">
                    <hr class="main_hr">
                    <input placeholder="''' + get_lang(conn, 'regex') + '''" name="content" value="''' + html.escape(textarea) + '''" type="text">
                '''
            elif tool == 'name_filter':
                title = get_lang(conn, 'id_filter_add')
                form_data = '' + \
                    get_lang(conn, 'regex') + \
                    '<hr class="main_hr">' + \
                    '<input value="' + html.escape(name) + '" type="text" name="title">' + \
                ''
            elif tool == 'file_filter':
                title = get_lang(conn, 'file_filter_add')
                form_data = '' + \
                    get_lang(conn, 'regex') + \
                    '<hr class="main_hr">' + \
                    '<input value="' + html.escape(name) + '" type="text" name="title">' + \
                ''
            elif tool == 'email_filter':
                title = get_lang(conn, 'email_filter_add')
                form_data = '' + \
                    get_lang(conn, 'email') + \
                    '<hr class="main_hr">' + \
                    '<input value="' + html.escape(name) + '" type="text" name="title">' + \
                ''
            elif tool == 'image_license':
                title = get_lang(conn, 'image_license_add')
                form_data = '' + \
                    get_lang(conn, 'license') + \
                    '<hr class="main_hr">' + \
                    '<input value="' + html.escape(name) + '" type="text" name="title">' + \
                ''
            elif tool == 'extension_filter':
                title = get_lang(conn, 'extension_filter_add')
                form_data = '' + \
                    get_lang(conn, 'extension') + \
                    '<hr class="main_hr">' + \
                    '<input value="' + html.escape(name) + '" type="text" name="title">' + \
                ''
            elif tool == 'document':
                acl_list = get_acl_list()
                
                curs.execute(db_change("select plus, plus_t from html_filter where html = ? and kind = 'document'"), [name])
                db_data = curs.fetchall()
                acl_list = [['selected' if db_data and db_data[0][1] == for_a else '', for_a] for for_a in acl_list]

                title = get_lang(conn, 'document_filter_add')
                form_data = '''
                    ''' + get_lang(conn, 'name') + '''
                    <hr class="main_hr">
                    <input value="''' + html.escape(name) + '''" type="text" name="name">
                    <hr class="main_hr">
                    ''' + get_lang(conn, 'regex') + '''
                    <hr class="main_hr">
                    <input value="''' + (html.escape(db_data[0][0]) if db_data else '') + '''" type="text" name="regex">
                    <hr class="main_hr">
                    <a href="/acl/Test#exp">''' + get_lang(conn, 'acl') + '''</a>
                    <hr class="main_hr">
                    <select name="acl">
                        ''' + ''.join(['<option ' + for_a[0] + ' value=' + for_a[1] + '>' + ('normal' if for_a[1] == '' else for_a[1]) + '</option>' for for_a in acl_list]) + '''
                    </select>
                '''
            elif tool == 'template':
                title = get_lang(conn, 'template_document_add')

                value = ''
                if name:
                    curs.execute(db_change("select plus from html_filter where html = ? and kind = 'template'"), [name])
                    exist = curs.fetchall()
                    value = exist[0][0] if exist else '' 

                form_data = '' + \
                    get_lang(conn, 'template') + \
                    '<hr class="main_hr">' + \
                    '<input value="' + html.escape(name) + '" type="text" name="title">' + \
                    '<hr class="main_hr">' + \
                    get_lang(conn, 'explanation') + \
                    '<hr class="main_hr">' + \
                    '<input value="' + html.escape(value) + '" type="text" name="exp">' + \
                    '<hr class="main_hr">' + \
                ''
            else:
                title = get_lang(conn, 'edit_tool_add')
                
                value = ''
                if name:
                    curs.execute(db_change("select plus from html_filter where html = ? and kind = 'edit_top'"), [name])
                    exist = curs.fetchall()
                    value = exist[0][0] if exist else ''    

                form_data = '''
                    ''' + get_lang(conn, 'title') + '''
                    <hr class="main_hr">
                    <input value="''' + html.escape(name) + '''" type="text" name="title">
                    <hr class="main_hr">
                    ''' + get_lang(conn, 'markup') + '''
                    <hr class="main_hr">
                    <input value="''' + html.escape(value) + '''" type="text" name="markup">
                '''

            return easy_minify(conn, flask.render_template(skin_check(conn),
                imp = [title, wiki_set(conn), wiki_custom(conn), wiki_css([get_sub, 0])],
                data =  '''
                        <form method="post">
                            ''' + form_data + '''
                            <hr class="main_hr">
                            <button ''' + stat + ''' type="submit">''' + get_lang(conn, 'add') + '''</button>
                        </form>
                        ''',
                menu = [['filter/' + tool, get_lang(conn, 'return')]]
            ))