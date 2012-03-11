
(ns picasagrok.repeater
  (:use compojure.core
        ring.adapter.jetty
		ring.middleware.reload
		ring.middleware.file
		ring.middleware.file-info
		ring.middleware.session
		hiccup.core
		hiccup.page-helpers
		hiccup.form-helpers
		clojure.set
		[clojure.contrib.sql :as sql :only ()]
		)
  (:import	(java.util.regex Matcher Pattern)
			(java.io StringBufferInputStream)
			(org.apache.commons.fileupload MultipartStream))
  (:require [compojure.route :as route]))


(defn read-string-from-stream-given-length [istream n]
	(loop [	buffer (make-array Byte/TYPE n)
			location 0
			bytesRead (.read istream buffer 0 n) ]
			(if 	(or (= bytesRead -1) (= location n))
					(do (println "Finished reading " n " bytes from InputStream.")
						(String. buffer))
					(do (Thread/sleep 1000)
						(println "Blocked after having read " location " bytes.")
						(recur buffer (+ location bytesRead) (- n bytesRead))))))


(defn read-string-until-block [istream]
	(let [	length	(.available istream)
			buffer	(make-array Byte/TYPE length)
			bytesRead (.read istream buffer 0 length)]
		(do (Thread/sleep 200)
			(if (< 0 (.available istream))
				;; read some more, don't expect to recur far anyways
				(str (String. buffer) (read-string-until-block istream))
				;; stop there
				(String. buffer)))))

(defn get-image-href-from-picasa-rss-feed [msg]
	(let [	_1 (println "get-image-href-from-picasa-rss-feed called with :\n" msg)
			;; the (?s) in the regex is the DOTALL flag that makes it such that the dot matches anything (including line terminals)
			feed-contents-only (first (re-seq #"(?s)<rss.*</rss>" msg))
			_2 (println "feed-contents-only = " feed-contents-only)
			feed-xml-seq (xml-seq (clojure.xml/parse (StringBufferInputStream. feed-contents-only )))
			]
		(if (not (= "" feed-contents-only))
			(for [x feed-xml-seq :when (= :photo:imgsrc (:tag x))]
				;; the content is a vector of stuff, but we want only the string with the local addresses for the images
				(first (:content x)))
			[])))

;; We can test the above method with this code.
;; (def S (slurp "./test/first_rss.txt"))
;; (def feed-contents-only (first (re-seq #"<rss.*</rss>" S)))
;; (def feed-xml-seq (xml-seq (clojure.xml/parse (java.io.StringBufferInputStream. feed-contents-only))))
;; (apply str (for [x feed-xml-seq :when (= :photo:imgsrc (:tag x))] (:content x)))


(defn make-response-to-rss-submission [image-href-list]
	(html [:body
			[:h3 "About to submit these images."]
			(form-to [:POST "/uploading_images"]
				(for [imgname image-href-list]
					(do (println imgname)
						(str	"<img src=" imgname ">"
								"<input type=hidden name=" imgname ">")))
				[:input {:type "submit" :value "apply"}])
			]))

(defn get-boundary-from-content-type-str [content-type-str]
	(let [	;; content-type-str "\";multipart/form-data; boundary=---------------------------77215493A493\""
			X (re-seq #"boundary=(-*\w*)" content-type-str)
			boundary (nth (first X) 1)]
			boundary))

(defn get-data-from-submission-request [req]
	(let [	_0	(println (escape-html req))
			body-istream 	(:body req)
			content-type 	(:content-type req)
			;  hint : it's not just :boundary, but it's parsed from the MIME
			boundary		(get-boundary-from-content-type-str content-type)
			;; see http://commons.apache.org/fileupload/apidocs/org/apache/commons/fileupload/MultipartStream.html
			multipart-stream (org.apache.commons.fileupload.MultipartStream. body-istream (.getBytes boundary))
			form-contents (loop [accum [] next-part (.skipPreamble multipart-stream)]
								(if next-part
									(let [	headers	(.readHeaders multipart-stream)
											buffer (java.io.ByteArrayOutputStream.)
											;; Theoretically, we could leave it as a ByteOutputStream, if that's more
											;; convenient later on when we want to write it to a file.
											_junk (.readBodyData multipart-stream buffer)
											data (.toByteArray buffer)]
										(recur 	(conj accum {:headers headers, :data data})
												(.readBoundary multipart-stream) ))
									accum)) ]
		form-contents))

(defroutes grok-routes
  (GET "/echo" req
	(html (str "GET " req)))
  (POST "/echo" req
	(do (println "Will try to read " (:content-length req) " bytes for content.")
		(println (escape-html req))
		(make-response-to-rss-submission
			(get-image-href-from-picasa-rss-feed
				;; (read-string-until-block (:body req))
				(read-string-from-stream-given-length (:body req) (:content-length req))))))
;; 	(html (str "POST " req
;; 				"\n\n" 
;; 				"(read-string-until-block (:body req)) = "
;; 				(escape-html (read-string-until-block (:body req))))))
  (POST "/uploading_images" req
	(let [	entries	(get-data-from-submission-request req)]
		(do 
			(println "uploading_images req : \n" req)
			(println "entries headers are : ")
			(doall (for [e entries] (println (:headers e))))
			(html (str "POST " req
				"\n"
				(for [e entries] (escape-html (:headers e))))))))
  (POST "/uploading_images_to_dump" req
	(do 
		(println "uploading_images_to_dump req : \n" req)
		(println "\n")
		(spit "/Users/gyomalin/programmation/archiving_3/picasagrok/test/dump_form_submission" (read-string-from-stream-given-length (:body req) (:content-length req)))
		(println "uploading_images body : \n" (read-string-from-stream-given-length (:body req) (:content-length req)))
		(html (str "POST " req
				"\n\n" 
				"(read-string-until-block (:body req)) = "
				(escape-html (read-string-from-stream-given-length (:body req) (:content-length req)))))))
  (GET "/*" req "<h1>GET : Hello World Wide Web!</h1>")
  (POST "/*" req "<h1>POST : Hello World Wide Web!</h1>")
  (route/not-found "Page not found. Patate."))

(def app-grok-routes
	(-> 	grok-routes
			;; with-session
			(wrap-file "public")
			(wrap-file-info)))

(defonce server
	(run-jetty (var app-grok-routes) {:port 8081 :join? false}))

(.start server)
;; (.stop server)

;; (run-jetty (var app-grok-routes) {:port 8081})


;; lein repl
;; (load-file "src/picasagrok/repeater.clj") 
