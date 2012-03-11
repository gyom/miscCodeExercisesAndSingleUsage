
(ns picasagrok.samus.db.handlers
  (:use compojure.core
        hiccup.core
		hiccup.page-helpers
		hiccup.form-helpers
		picasagrok.samus.db.interface
		picasagrok.samus.db.transient
		))
		
(defn select-db-handler-GET [req r-current-db]
	(let [	description (.shortDescription @r-current-db)
			image (:image description)
			desc (:desc description)
			title (:title description)	]
	(html [:div	[:p "Currently using"]
				[:div.db_box [:div.db_desc_title	[:h3 title]]
							[:div.db_desc_bottom
							[:div.db_desc_image [:img {:src (str "images/" image)}]]
							[:div.db_desc_desc desc]	]]
				[:br]
				[:hr]
				[:br]
				[:p "Other available options"]	])))
	
(defn select-db-handler-PUT [req r-current-db] "select-db-handler-PUT not implemented yet"	)

;; add something to run an automated test on the database