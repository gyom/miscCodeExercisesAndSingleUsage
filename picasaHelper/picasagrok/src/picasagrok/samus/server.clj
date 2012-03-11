
(ns picasagrok.samus.server
  (:use compojure.core
        ring.adapter.jetty
		ring.middleware.reload
		ring.middleware.file
		ring.middleware.file-info
		ring.middleware.session
		ring.middleware.multipart-params
		hiccup.core
		hiccup.page-helpers
		hiccup.form-helpers
		clojure.set
		[clojure.contrib.sql :as sql :only ()]
		picasagrok.samus.db.handlers
		picasagrok.samus.db.transient
		picasagrok.samus.picasa_upload.handlers
		)
  (:import	(java.util.regex Matcher Pattern)
			(java.io StringBufferInputStream)
			(org.apache.commons.fileupload MultipartStream))
  (:require [compojure.route :as route]))


(defn standard-samus-interface [right-frame-html]
	(html 	[:html
				[:head 	[:title "Listing images."]
					[:style {:type "text/css"}]
					[:link {:href "/css/title_and_frames.css" :rel "stylesheet" :type "text/css"}]
					[:link {:href "/css/colors_oriss.css" :rel "stylesheet" :type "text/css"}]]
				[:body 	[:div#titleBar [:p "tanarkh"]]
						[:div#framedBox
							[:div#leftMenu
								[:p (link-to "/select_database" "select database")]
								[:p (link-to "/import_picasa_ini" "import .picasa.ini")]
								[:p (link-to "/import_files_on_disk" "import files on disk")]
								[:p (link-to "/import_files_by_http" "import file by http")]
								[:hr]
								[:p (link-to "/status" "status")]
								[:p (link-to "/contents" "contents")]
								[:p (link-to "/logs" "logs")]
								[:hr]
								]
							[:div#rightContent right-frame-html]
						]]]))

(def current-db (ref (make-transient-db)))

(defroutes tanarkh-routes
	;; can't change that without changing the button, later on it'll be "/picasa_prepare_submission"
	(POST "/echo" req (standard-samus-interface (picasa-upload-handler-rss-PUT req current-db)))
	(POST "/picasa_upload_submission" req (standard-samus-interface (picasa-upload-handler-submission-PUT req current-db)))
	(GET "/select_database" req (standard-samus-interface (select-db-handler-GET req current-db)))
	(PUT "/select_database" req (standard-samus-interface (select-db-handler-PUT req current-db)))
	(GET "/*" req (standard-samus-interface "<h1>GET : Hello World Wide Web!</h1>"))
  	(POST "/*" req (standard-samus-interface "<h1>POST : Hello World Wide Web!</h1>"))
	(route/not-found (standard-samus-interface "Page not found. Patate."))
	)

(def app-tanarkh-routes
	(-> 	tanarkh-routes
			;; experimenting with these naked instead of with parentheses
			wrap-session
			wrap-multipart-params
			(wrap-file "public")
			(wrap-file-info)))

(def server
	(run-jetty (var app-tanarkh-routes) {:port 8081 :join? false}))

(.start server)

;; lein repl
;; (load-file "src/picasagrok/samus/server.clj")
