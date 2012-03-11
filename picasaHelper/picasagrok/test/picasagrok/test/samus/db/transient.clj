
(ns picasagrok.test.samus.db.transient
	(:use picasagrok.samus.db.transient)
	(:use [clojure.test]))
	
(deftest basic-creation
	(let [	db (make-transient-db)	]
		(do	(.createEntry db {:md5 "lupi", :data 4320932})
			(.createEntry db {:md5 "zupi", :data -17000})
			;; (println (.retrieveTable db))
			(is (= #{4320932, -17000} (set (for [x (.retrieveAllEntries db)] (:data x)))))
			(.deleteEntryByMd5 db "lupi")
			(is (= #{-17000} (set (for [x (.retrieveAllEntries db)] (:data x)))))

			(.createEntry db {:md5 "zupi", :data "this won't fly because we already have an entry with that md5"})
			(is (= #{-17000} (set (for [x (.retrieveAllEntries db)] (:data x)))))

			(.createEntry db {:md5 "1", :data 10})
			(.createEntry db {:md5 :deux, :data 20})
			(.createEntry db {:md5 3, :data 30})
			;; (println (.retrieveTable db))
			(is (= (:data (.retrieveEntryByMd5 db "1")) 10))
			(is (= (:data (.retrieveEntryByMd5 db :deux)) 20))
			(is (= (:data (.retrieveEntryByMd5 db 3)) 30))
			
			(.clearAll db)
			(is (empty? (.retrieveAllEntries db)))
			(is (empty? (.retrieveLogs db)))
			
			)
		))