
(ns picasagrok.samus.picasa_upload.handlers
	(:use compojure.core
        hiccup.core
		hiccup.page-helpers
		hiccup.form-helpers)
	(:import (java.io StringBufferInputStream))		)

(defn picasa-upload-handler-rss-PUT-debug-echo [req r-current-db]
	(html (escape-html req)))

(defn picasa-upload-handler-rss-PUT [req r-current-db]
	(let [	rss-xml-text ((req :params) "rss")
			feed-xml-seq (xml-seq (clojure.xml/parse (StringBufferInputStream. rss-xml-text )))
			images-list (for [x feed-xml-seq :when (= :photo:imgsrc (:tag x))]
							;; the content is a vector of stuff, but we want only the string with the local addresses for the images
							(first (:content x)))
			thumbnails-list (for [x feed-xml-seq :when (= :photo:thumbnail (:tag x))]
								;; the content is a vector of stuff, but we want only the string with the local addresses for the images
								(first (:content x)))
			joint-list (loop [	accum [] A images-list B thumbnails-list]
								(if (or (empty? A) (empty? B))
									accum
								(recur (conj accum [(first A) (first B)]) (rest A) (rest B) )))
			]
		(html [:h3 "About to submit these images."]
				(form-to [:POST "/picasa_upload_submission"]
						;; later on we'll add something for labels in here, to specify them while submitting
						(for [[image-name thumbnail-name] joint-list]
							(html	[:img {:src thumbnail-name}]	[:input {:type "hidden" :name image-name}]))
						[:input {:type "submit" :value "apply"}]))))

(defn picasa-upload-handler-submission-PUT [req r-current-db]
	(do (println "(req :params)" (req :params))
		(println "(req :multipart-params)" (req :multipart-params))
	 	"picasa-upload-handler-submission-PUT not implemented yet"))
	
