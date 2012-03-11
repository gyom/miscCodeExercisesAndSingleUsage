(ns picasagrok.test.parsing-picasa-ini-files
	(:use [picasagrok.parsing-picasa-ini-files] :reload)
	(:use [clojure.test])
	)

(deftest basic-matches-1
	(let [	X	(parse-line-matching-filename "[Screen shot 2010-07-26 at 4.13.29 AM.png]")]
		;; -> {:filename "Screen shot 2010-07-26 at 4.13.29 AM.png", :extension "png"}
		(do (is (= (:filename X) "Screen shot 2010-07-26 at 4.13.29 AM.png"))
			(is (= (:extension X) "png")))))

(deftest basic-matches-2
	(let [	X	(parse-line-matching-filename "[filename[a=222].png]")]
		(do (is (= (:filename X) "filename[a=222].png"))
			(is (= (:extension X) "png")))))

(deftest basic-matches-3
	(let [	X	(parse-line-matching-tags "keywords=\"test\",age{20},Buffy The Vampire Slayer,chien,lupi,spike")]
		;; -> {:tags #{"lupi" "age{20}" "spike" "chien" "\"test\"" "Buffy The Vampire Slayer"}}
		(is (= (:tags X) #{"lupi" "age{20}" "spike" "chien" "\"test\"" "Buffy The Vampire Slayer"}))))

(deftest basic-matches-4
	(let [	X	(parse-line-matching-tags ", , oiseau")]
		(is (nil? X))))
		
;; Do the same thing but now with the combined parsers.
(deftest basic-matches-1-1
	(let [	X	(parse-line "[Screen shot 2010-07-26 at 4.13.29 AM.png]")]
		;; -> {:filename "Screen shot 2010-07-26 at 4.13.29 AM.png", :extension "png"}
		(do (is (= (:filename X) "Screen shot 2010-07-26 at 4.13.29 AM.png"))
			(is (= (:extension X) "png")))))
			
(deftest basic-matches-3-1
	(let [	X	(parse-line "keywords=\"test\",age{20},Buffy The Vampire Slayer,chien,lupi,spike")]
		;; -> {:tags #{"lupi" "age{20}" "spike" "chien" "\"test\"" "Buffy The Vampire Slayer"}}
		(is (= (:tags X) #{"lupi" "age{20}" "spike" "chien" "\"test\"" "Buffy The Vampire Slayer"}))))
			

(deftest dummy-ini-test-1
	(let [s
"[Screen shot 2010-07-26 at 4.13.29 AM.png]
faces=rect64(5f161536ba83c4c0),1b462909048bf25c
backuphash=54288
keywords=\"test\",age{20},Buffy The Vampire Slayer,chien,lupi,spike
[Screen shot 2010-07-01 at 12.42.47 AM.png]
faces=rect64(37c519d88b94ba83),43aa6a6520fe87fb
backuphash=23217
[Screen shot 2010-06-01 at 10.53.13 PM.png]
faces=rect64(6381084ac1fabd31),43aa6a6520fe87fb
backuphash=23217"
	ppi (parse-picasa-ini-inputstream (java.io.ByteArrayInputStream. (.getBytes s)))]
	(is (= 	ppi
			#{{:filename "Screen shot 2010-06-01 at 10.53.13 PM.png", :extension "png"} {:tags #{"lupi" "age{20}" "spike" "chien" "\"test\"" "Buffy The Vampire Slayer"}, :filename "Screen shot 2010-07-26 at 4.13.29 AM.png", :extension "png"} {:filename "Screen shot 2010-07-01 at 12.42.47 AM.png", :extension "png"}}
		))))
	
	
	
	

			
			
			