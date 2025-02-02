package route

import (
	"encoding/json"
	"log"
	"opennamu/route/tool"
)

func Api_w_set_reset(call_arg []string) string {
	db_set := map[string]string{}
	json.Unmarshal([]byte(call_arg[0]), &db_set)

	other_set := map[string]string{}
	json.Unmarshal([]byte(call_arg[1]), &other_set)

	db := tool.DB_connect(db_set)
	defer db.Close()

	doc_name := other_set["name"]
	ip := other_set["ip"]
	auth_name := tool.Get_user_auth(db, db_set, ip)
	auth_info := tool.Get_auth_group_info(db, db_set, auth_name)

	if auth_info["owner"] {
		stmt, err := db.Prepare(tool.DB_change(db_set, "delete from acl where title = ?"))
		if err != nil {
			log.Fatal(err)
		}
		defer stmt.Close()

		_, err = stmt.Exec(doc_name)
		if err != nil {
			log.Fatal(err)
		}

		stmt, err = db.Prepare(tool.DB_change(db_set, "delete from data_set where doc_name = ? and set_name = 'acl_date'"))
		if err != nil {
			log.Fatal(err)
		}
		defer stmt.Close()

		_, err = stmt.Exec(doc_name)
		if err != nil {
			log.Fatal(err)
		}

		set_list := []string{
			"document_markup",
			"document_top",
			"document_editor_top",
		}

		for for_a := 0; for_a < len(set_list); for_a++ {
			stmt, err = db.Prepare(tool.DB_change(db_set, "delete from data_set where doc_name = ? and set_name = ?"))
			if err != nil {
				log.Fatal(err)
			}
			defer stmt.Close()

			_, err = stmt.Exec(doc_name, set_list[for_a])
			if err != nil {
				log.Fatal(err)
			}
		}

		return_data := make(map[string]interface{})
		return_data["response"] = "ok"
		return_data["language"] = map[string]string{
			"reset": tool.Get_language(db, db_set, "reset", false),
		}

		json_data, _ := json.Marshal(return_data)
		return string(json_data)
	} else {
		return_data := make(map[string]interface{})
		return_data["response"] = "require auth"
		return_data["language"] = map[string]string{
			"authority_error": tool.Get_language(db, db_set, "authority_error", false),
		}

		json_data, _ := json.Marshal(return_data)
		return string(json_data)
	}
}
