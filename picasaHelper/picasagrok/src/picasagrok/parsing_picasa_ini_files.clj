(ns picasagrok.parsing-picasa-ini-files
(:import (java.io InputStreamReader BufferedReader)))


(defn parse-line-matching-filename [s]
	;; [Screen shot 2010-07-26 at 4.13.29 AM.png]
	(let [	X	(re-seq #"^\[(.+\.(.+))\]$" s)	]
		(if (empty? X)
			nil
			;; if we have a good match, extract more information
			(let [[_junk1 filename extension] (nth X 0)]
				{:filename filename, :extension extension}))))

(defn parse-line-matching-tags [s]
	;; keywords="test",age{20},Buffy The Vampire Slayer,chien,lupi,spike
	(let [	X	(re-seq #"^keywords=(.+)$" s)	]
		(if (empty? X)
			nil
			;; If we have a good match, extract more information (from the string with the tags, (nth X 1)).
			;; Clump together anything that's not a comma (they're not legal in picasa tags).
			(let [tags (re-seq #"[^,]+" (nth (nth X 0) 1))]
				;; using a set to signify that we'll be treating tags in no order and will remove duplicates
				{:tags (set tags)}))))

(defn parse-line-matching-any [s] {})

(defn combine-matchers [matchers]
	(fn [s]
		(if (empty? matchers)
			nil
			(loop [	f	(first matchers)
					R	(rest matchers)	]
				(let [m (f s)]
					(if (nil? m)
						(if (nil? R)
							nil
							;; didn't match, but some matchers left to try out
							(recur (first R) (rest R)))
						;; it did match
						m))))))

(def picasa-combined-matchers (combine-matchers [	parse-line-matching-filename
													parse-line-matching-tags
													parse-line-matching-any	]))

(defn parse-line [s]
	(picasa-combined-matchers s))

(defn new-file-description? [pl]
	(not (nil? (:filename pl))))

(defn parse-picasa-ini-inputstream [istream]
	(let [	lsq	(line-seq (BufferedReader. (InputStreamReader. istream)))]
		(loop [result-accum #{} currentpic-accum {} lsq lsq]
			(if (empty? lsq)
				;; we're done, just put the last result in
				(conj result-accum currentpic-accum)
				;; not done, but not sure if we've encountered a new description
				;; or are still reading from an ongoing one
				(let [e (parse-line (first lsq))]
					(if (new-file-description? e)
						;; If we had read something, add that thing to the accumulation,
						;; and then start over from the result "e" that we have in hand.
						;; If we had nothing (like what happens when we start parsing the file),
						;; then we don't want to have this ugly empty set lying around.
						(if (empty? currentpic-accum)
							(recur result-accum e (rest lsq))
							(recur (conj result-accum currentpic-accum) e (rest lsq)))
						;; else merge the result of that line, probably of the
						;; form {:name "Screenshot Vampire.png"} or {:tags ["Beast", "Undead"]}
						;; or something like that, to be decided elsewhere
						(recur result-accum (merge currentpic-accum e) (rest lsq))))))))

