(ns yodle.trianglesolver
	;; for clojure 1.2
	;; (:use [clojure.contrib.io :only (reader)])
	;; for clojure 1.1
	(:use [clojure.contrib.duck-streams :only (reader)])
	)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; helper function
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; I don't like doing this like that instead of using a "zip" function, but
;; I don't think there is a zip like that as part of Clojure's base libraries.
;; I'd do (map + (zip A B)) instead if I could.
(defn vector-addition [A B]
	"(vector-addition [1 2 3] [4 5 6])  ->  [5 7 9]"
	(loop [accum [] A A B B]
		(if (or (empty? A) (empty? B))
			accum
			(recur (conj accum (+ (first A) (first B))) (rest A) (rest B)))))	
			
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; The function that solves the puzzle given a triangle.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defn triangle-maximum-value-through-path [triangle]
	"(triangle-maximum-value-through-path [[1] [2 3] [4 5 6]])  -> 27"
	(if (empty? triangle)
		;; degenerate case, let's go for the default answer zero
		0
		(loop [	maxima-slice	[]
				triangle	triangle]
			(if (empty? triangle)
				;; no way to recover the path to the maximum if
				;; we don't save any of the partial work
				(apply max maxima-slice)
				(let [	;; transforming [1 2 3] into [0 1 2 3 0] 
						padded-maxima-slice	(cons 0 (conj maxima-slice 0))
						;; transforming [0 1 2 3 0] into [[0 1] [1 2] [2 3] [3 0]]
						pairs	(partition 2 1 padded-maxima-slice)
						;; getting the maximum of every pair above
						max-by-pairs	(for [[a b] pairs] (max a b))
						;; this iteration's argument
						next-triangle-slice	(first triangle)
						;; compounding the results with the maxima found at previous line
						next-maxima-slice	(vector-addition max-by-pairs next-triangle-slice)	]
					;; proceed to the next level of the pyramid
					(recur next-maxima-slice (rest triangle)))))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Some testing to be sure.
;; This would be in a separate file for a more serious project.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; should give 10
(println (triangle-maximum-value-through-path [[1] [2 3] [4 5 6]]))

;; should give 27, Yodel's example
(println (triangle-maximum-value-through-path [[5] [9 6] [4 6 8] [0 7 1 5]]))

;; should give 0
(println (triangle-maximum-value-through-path []))
;; should give 1
(println (triangle-maximum-value-through-path [[1]]))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;  Solving the actual problem, reading the data.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defn read-triangle-file [filename]
	(let [	lines	(line-seq (reader filename))	]
		(for [line lines]
			;; match numbers grouped (separated by spaces)
			(map #(Integer. %) (re-seq #"\d+" line)))))
		
(def triangle (read-triangle-file "triangle.txt"))

(println (triangle-maximum-value-through-path triangle))
;; 732506  -> yay !






