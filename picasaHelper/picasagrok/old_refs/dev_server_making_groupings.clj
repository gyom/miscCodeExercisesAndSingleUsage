
(ns gendergame.dev_server_making_groupings
  (:use compojure.core
        ring.adapter.jetty
		ring.middleware.reload
		ring.middleware.file
		ring.middleware.file-info
		ring.middleware.session
		hiccup.core
		hiccup.page-helpers
		hiccup.form-helpers
		gendergame.database_definitions
		gendergame.directory_path_definitions
		gendergame.access_tools
		gendergame.formatting_tools
		clojure.set
		[clojure.contrib.sql :as sql :only ()])
  (:require [compojure.route :as route]))


(defroutes routes-for-playing-with-images
  (GET "/list_images" req
	(let [image-entries (get-db-filename-entries)]
			(html 	common-header-struct
					[:body (for [e image-entries]
								;; [:img {:src "/images/" (e :filename)}]
								(gen-image (e :filename))
								[:p (str e)]
								)
							])))
  (GET "/demo_checkbox_pick_images" req
	(let [image-entries (get-db-filename-entries)]
			(html 	common-header-struct
					[:body (for [e image-entries]
							;; [:img {:src "/images/" (e :filename)}]
							(gen-image-selection-box-thumbnail (e :filename) false (e :filename)))
						])))
  (GET "/show_grouping/:n" req
	(let [	groupings-entries (get-db-groupings-entries)
			params (req :params)
			grouping-number (Integer. (params "n"))
			groupings-entries-already-in-grouping (doall (filter #(= (:group_id %) grouping-number) groupings-entries))
			;; we want to display the images in a unique fashion now without getting duplicate entries
			;; when we have data about the sex and the counts
			filename-entries-in-grouping (set (for [e groupings-entries-already-in-grouping] (:filename e)))
			]
			(html 	common-header-struct
					[:body		[:h2 (str "Images in grouping " grouping-number ".")]
								[:br]
								(for [filename filename-entries-in-grouping]
									(gen-image-thumbnail filename))
								[:br] [:br]
								[:hr]
								[:br]
								[:h2 (str "params =  " params)]
								[:h2 (str "groupings-entries =  " groupings-entries)]
								[:br]
								[:h2 (str "groupings-entries-already-in-grouping =  " groupings-entries-already-in-grouping)]
								[:br]
								[:h2 (str "(count groupings-entries-already-in-grouping) =  " (count groupings-entries-already-in-grouping))]
								[:br]
								[:h2 (str "filename-entries-in-grouping =  " filename-entries-in-grouping)]
								])))
  (GET "/add_to_grouping/:n" req
	(let [	groupings-entries (get-db-groupings-entries)
			image-entries (get-db-filename-entries)
			filename-entries (set (for [e image-entries] (:filename e)))
			params (req :params)
			grouping-number (Integer. (params "n"))
			groupings-entries-already-in-grouping (filter #(= (:group_id %) grouping-number) groupings-entries)
			;; we want to display the images in a unique fashion now without getting duplicate entries
			;; when we have data about the sex and the counts
			filename-entries-in-grouping (set (for [e groupings-entries-already-in-grouping] (:filename e)))
			filename-entries-not-in-grouping (difference filename-entries filename-entries-in-grouping)
		]
			(html 	common-header-struct
					[:body	(form-to [:POST (str "/add_to_grouping/" grouping-number "/apply")] 
							; [:form {:method "post" :action (str "/add_to_grouping/" grouping-number "/apply")}
								;; [:input {:id "_method" :name "_method" :type "hidden" :value "post"}]
								[:h2 (str "Adding images to grouping " grouping-number ".")]
								[:br] [:br]
								[:hr]
								[:br]
								[:h4 (str "These images are already included in the grouping.")]
								(for [filename filename-entries-in-grouping]
									;; (gen-image-thumbnail filename)
									(gen-image-selection-box-thumbnail filename false "REMOVE"))
								[:br] [:br]
								[:hr]
								[:br]
								[:h4 (str "The images are available.")]
								(for [filename filename-entries-not-in-grouping]
									(gen-image-selection-box-thumbnail filename false "ADD"))
								[:input {:type "submit" :value "apply"}]
							;; ]
							)
						])))
  (POST "/add_to_grouping/:n/apply" req 
		(let [	params (req :params)
				;; groupings-entries (get-db-groupings-entries)
				grouping-number (Integer. (params "n"))
				;; groupings-entries-already-in-grouping (filter #(= (:group_id %) grouping-number) groupings-entries)
				
				;; Assuming the values are all correct and we're not going to remove files that aren't included.
				checked-filenames-to-add (for [[k v] params :when (= v "ADD")] k)
				checked-filenames-to-remove (for [[k v] params :when (= v "REMOVE")] k)
				
				;; as sanity check :
					groupings-entries (get-db-groupings-entries)
					groupings-entries-already-in-grouping (filter #(= (:group_id %) grouping-number) groupings-entries)
					image-entries (get-db-filename-entries)
					filename-entries (set (for [e image-entries] (:filename e)))
					filename-entries-in-grouping (set (for [e groupings-entries-already-in-grouping] (:filename e)))
					_1 (println "filename-entries-in-grouping : " filename-entries-in-grouping)
					filename-entries-not-in-grouping (difference filename-entries filename-entries-in-grouping)
					;; you can't add stuff that's already there
					E0_should_be_empty (difference (set checked-filenames-to-add) (set filename-entries-not-in-grouping))
					;; you can't take out stuff that's not there
					E1_should_be_empty (difference (set checked-filenames-to-remove) (set filename-entries-in-grouping))
					T0 (if (not (empty? E0_should_be_empty))
							(do (println E0_should_be_empty)
								(println checked-filenames-to-add)
								(println filename-entries-not-in-grouping)
								(throw (Exception. "you can't add stuff that's already there")))
							nil)
					T1 (if (not (empty? E1_should_be_empty))
					 		(do (println E1_should_be_empty)
								(println checked-filenames-to-remove)
								(println filename-entries-in-grouping)
								(throw (Exception. "you can't take out stuff that's not there")))
							nil)
			]
			(html common-header-struct
				[:body	(str "POST got params " params)
						(for [filename checked-filenames-to-add]
							(do (add-filename-to-grouping filename grouping-number)
								[:p "Added " filename " to grouping " grouping-number "."]))
						(for [filename checked-filenames-to-remove]
							(do	(remove-filename-from-grouping filename grouping-number)
								[:p "Removed " filename " from grouping " grouping-number "."]))
				])
			))
  ;; (GET "/public/*" [] "<h1>Hello World Wide Web!</h1>")
  (route/not-found "Page not found"))

(def app-routes-for-playing-with-images
	(-> 	routes-for-playing-with-images
			;; with-session
			(wrap-file "public")
			(wrap-file-info)))

(run-jetty (var app-routes-for-playing-with-images) {:port 8080})





;; lein repl src/gendergame/dev_server_making_groupings.clj

