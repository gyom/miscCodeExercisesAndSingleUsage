
(ns picasagrok.samus.db.transient
	(:use picasagrok.samus.db.interface))

(deftype TransientServerDatabase [state]
	TanarkhDatabase
	(createEntry [this md5 E]
		(dosync (alter state
			(fn [dstate]
				(let [	;; just in case the md5 wasn't there 
						E (assoc E :md5 md5)
						table (:table dstate)
						entry (table md5)
						logs (:logs dstate)	]

					(cond	(nil? md5)
								;; error
								(let [	new-logs (conj logs (str "Tried to add element " md5 " to table, but we don't allow that value as key."))	]
									;; _junk (println "error")		
									(assoc @state :logs new-logs))
							(nil? entry)
								;; proceed
								(let [	new-table (assoc table md5 E)
										new-logs (conj logs (str "Added element " md5 " to table."))	]
										;; _junk (println "proceed")
										;; _junk0 (println new-table)
										;; _junk1 (println new-logs)		
									(merge dstate {:table new-table, :logs new-logs}))
							true
								;; already an existing entry, and we're not overwriting things here
								(let [	new-logs (conj logs (str "Tried to add element " md5 " to table, but didn't because it would have overwritten an element present."))	]
										;; _junk (println "already present, don't overwrite")
									(assoc dstate :logs new-logs)) ))))))
	(createEntry [this E-with-md5]
		(.createEntry this (:md5 E-with-md5) E-with-md5))
	(deleteEntryByMd5 [this md5]
		(dosync	(alter state
			(fn [dstate]
				(let [	table (:table dstate)
						entry (table md5)
						new-table (dissoc table md5)
						logs (:logs dstate)
						new-logs (if 	(nil? entry)
				 						(conj logs (str "Attempted to remove element " md5 " from table, but none was found."))
										(conj logs (str "Removed element " md5 " from table.")))	]
					(merge dstate {:table new-table, :logs new-logs}) )))))	
	(retrieveEntryByMd5 [this md5] ((.retrieveTable this) md5))
	(retrieveTable [this] (:table @state))
	(retrieveAllEntries [this] (set (vals (:table @state))))
	(retrieveLogs [this] (:logs @state))
	(clearTable [this] (dosync (alter state #(assoc % :table {}))))
	(clearLogs [this] (dosync (alter state #(assoc % :logs []))))
	(clearAll [this ] (dosync (alter state #(assoc (assoc % :logs []) :table {}) )))
	(shortDescription [this]
		{:image "clojure-icon.gif", :title "Clojure Transient Database", :desc "Lasts only while the server is up. Vanishes into nothingness after. Supports arbitrary fields. Indexed by the md5 values."})
	)
	
;; this is what is exported from this namespace
(defn make-transient-db []
	(TransientServerDatabase. (ref {:table {}, :logs []})))