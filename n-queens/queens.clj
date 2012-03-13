;;
;; The purpose of this code is to check how dense are the solutions
;; to the n-queens problem. For example, what percentage of possible
;; arrangements of 8 queens on an 8-by-8 board are good solutions.
;;
;; The point of the question is to put actual numbers on the popular
;; idea that, because the solutions are sufficiently dense, greedy
;; methods work well.
;;
;; Some of the complexity of this code comes from the fact that we
;; are using a system of coordinate projections to detect conflicts
;; (queens sharing a row or a diagonal) without paying N^2 every time
;; we consider adding a queen somewhere. 

(ns queens)


(defn proj [x y]   [x y (+ x y) (- x y)]  )

;; profile :  [#{0 1 2 3}
;;             #{3 2 4 1}
;;             #{7 4 2 1}
;;             #{1 2 3 0}]
(defn check-profile [profile x y]
   (let [   myProj (proj x y)
            conflict    (or   (contains? (nth profile 0) (nth myProj 0))
                              (contains? (nth profile 1) (nth myProj 1))
                              (contains? (nth profile 2) (nth myProj 2))
                              (contains? (nth profile 3) (nth myProj 3)))  ]
      (not conflict)))

(defn augment-profile [profile x y]
   (let [   myProj (proj x y) ]
      [  (conj (nth profile 0) (nth myProj 0))
         (conj (nth profile 1) (nth myProj 1))
         (conj (nth profile 2) (nth myProj 2))
         (conj (nth profile 3) (nth myProj 3))
      ]))

;; partial-solution = sequence of [x,y] pairs where the queens are
(defn find-solutions-helper [partial-solution  current-profile  xRemaining  yRemaining]
   (if   (or (empty? xRemaining) (empty? yRemaining))
         ;; return a valid answer as a list of one valid solution 
         (list partial-solution)
         ;; otherwise build on that, but return a list !
         (let [   x (first xRemaining)
                  reducer  (fn [accum L] (lazy-cat accum L))
                  init []
            ]
            (reduce reducer init
               (for [y yRemaining]
                  (if   (check-profile current-profile x y)
                     (let [   new-partial-solution (conj partial-solution [x y])
                              new-profile (augment-profile current-profile x y)
                              new-xRemaining (disj xRemaining x)
                              new-yRemaining (disj yRemaining y)  ]
                              (find-solutions-helper new-partial-solution new-profile new-xRemaining new-yRemaining))))))))

(defn find-solutions [N]
   (let [   partial-solution  []
            current-profile   [#{} #{} #{} #{}]
            xRemaining        (set (range 0 N))
            yRemaining        (set (range 0 N)) ]
   (find-solutions-helper partial-solution current-profile xRemaining yRemaining)))


;; board = sequence of [x,y] pairs
;; (  [  [0 1] [1 3] [2 0] [3 2] ]
;;    [  [0 2] [1 0] [2 3] [3 1] ]  )
(defn print-board [board]
   (let [   board (set board)
            N (inc (apply max (for [[x y] board] (max x y) )))]
      (doseq [y (reverse (range 0 N))]
         (let [rowString (apply str (for [x (range 0 N)] (if (contains? board [x y]) "R" "0")))]
            (println rowString)))))


(def S8 (find-solutions 8))


;; testing to see if it works
(for [n (range 1 10)]
   (let [howMany (count (find-solutions n))]
      (println "n = " n " : " howMany)))






(def counter (ref 0))
;; 
;; partial-solution = sequence of [x,y] pairs where the queens are
(defn count-solutions-helper [partial-solution  current-profile  xRemaining  yRemaining]
   (if   (or (empty? xRemaining) (empty? yRemaining))
         (dosync (commute counter inc))
         (let [   x (first xRemaining)  ]
            (doseq [y yRemaining]
               (if   (check-profile current-profile x y)
                  (let [   new-partial-solution (conj partial-solution [x y])
                           new-profile (augment-profile current-profile x y)
                           new-xRemaining (disj xRemaining x)
                           new-yRemaining (disj yRemaining y)  ]
                           (count-solutions-helper new-partial-solution new-profile new-xRemaining new-yRemaining)))))))

(defn count-solutions [N]
   (let [   partial-solution  []
            current-profile   [#{} #{} #{} #{}]
            xRemaining        (set (range 0 N))
            yRemaining        (set (range 0 N))  ]
      (do   (dosync (ref-set counter 0))
            (count-solutions-helper partial-solution current-profile xRemaining yRemaining)
            @counter)))


(defn factorial [n]
   (loop [r 1 n n]
      (if   (= n 0)
            r
            (recur (* n r) (dec n)))))

;; now use everything to find the ratios that we're looking for

(for [n (range 1 12)]
   (let [howMany (count-solutions n)]
      (println "n = " n " : " howMany ",  ratio = " (/ (double howMany) (double (factorial n))))))

(for [n (range 1 12)]
   (let [t (time (count-solutions n))]
      (println "time for n = " n " : " t)))






