;lang scheme/base

(require rnrs)
;(require rnrs base)

; The 'fail' function here takes two arguments instead of none (as expected) because
; we're trying to support the 'not' function for tokens read. It's a bit strange to try
; that, but let's do it anyways. We have to know what's left in the stream after we
; successfully read 'not an A' or 'not (any number of A)'.

; fail <- (left over, accum)

; success <- (new fail, left over, accum)

(define (read-A fail success input-stream accum)
  (cond ((empty? input-stream) (fail '() accum))
        ((not (eq? #\A (car input-stream))) (fail (cdr input-stream) accum))
        (else (success fail (cdr input-stream) accum))))

(define (make-char-reader char-to-match)
  (lambda (fail success input-stream accum)
  (cond ((empty? input-stream) (fail '() accum))
        ((not (eq? char-to-match (car input-stream))) (fail (cdr input-stream) accum))
        (else (success fail (cdr input-stream) (cons (car input-stream) accum))))))

(define (reg-or R S)
  (lambda (fail success input-stream accum)
    (R  (lambda (i a) (S fail success input-stream accum)) ; the new fail that tries S after that
        success
        input-stream
        accum)))

(define-syntax reg-or*
  (syntax-rules ()
    ((_) read-nothing)
    ((_ e) e)
    ((_ e1 e2 ...) (reg-or e1 (reg-or* e2 ...)))))

(define (reg-concat R S)
  (lambda (fail success input-stream accum)
    (R fail
       (lambda (f i a) (S f success i a)) ; the new success function that goes to read S after having read R
       input-stream
       accum)))

(define-syntax reg-concat*
  (syntax-rules ()
    ((_) read-nothing)
    ((_ e) e)
    ((_ e1 e2 ...) (reg-concat e1 (reg-concat* e2 ...)))))

(define (read-nothing fail success input-stream accum)
  (success fail input-stream accum))

(define (read-any fail success input-stream accum)
  (if (empty? input-stream)
      (fail '() accum) ; am I supposed to return even less than an empty list ?
      (success fail (cdr input-stream) (cons (car input-stream) accum))))

(define (make-str-reader str)
  (fold-left reg-concat read-nothing (map make-char-reader (string->list str))))

(define (reg-not R)
  (lambda (fail success input-stream accum)
    (R (lambda (i a) (success fail i a)) ; call success when we failed
       (lambda (f i a) (fail i a))
       input-stream
       accum)))
; try (reg-not (reg-not R)) ?= R  eventually by curiosity

(define (reg-zero-or-more R)
  (define (R*rec fail success input-stream accum)
    (R (lambda (i a) (success fail input-stream accum)) ; new fail, it "succeeds" by leaving the streams untouched
       (lambda (f i a) (R*rec f success i a))
       input-stream
       accum))
  R*rec) ; because we return the recursive function after defining it
       
(define (reg-one-or-more R)
  (reg-concat R (reg-zero-or-more R)))


;;;;;;;;;;;;;;;;; first unit tests;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define (simple-matching-test R str)
  (define (fail input-stream accum)
    (printf "Failed to match one character before position ~s\n" (list->string input-stream))
    #f)
  (define (success fail input-stream accum)
    (printf "Matched successfully.\n")
    ; (display accum) (newline)
    #t)
  (R fail success (string->list str) '()))

(assert (simple-matching-test (make-char-reader #\A) "A"))
(assert (not (simple-matching-test (make-char-reader #\A) "B")))

(assert (simple-matching-test (reg-concat (make-char-reader #\A) (make-char-reader #\B)) "ABa"))
(assert (not (simple-matching-test (reg-concat (make-char-reader #\A) (make-char-reader #\B)) "aBa")))

(assert (simple-matching-test (reg-not (reg-concat (make-char-reader #\A) (make-char-reader #\B))) "aBa"))

(assert (simple-matching-test (make-str-reader "patate") "patates pilees"))
(assert (not (simple-matching-test (make-str-reader "citron") "patates pilees")))

(assert (simple-matching-test (reg-or (make-str-reader "patates") (make-str-reader "citron")) "patates pilees"))
(assert (not (simple-matching-test (reg-or (make-str-reader "patates") (make-str-reader "citron")) "brocoli sucré")))

(define legume1 (make-str-reader "patate"))
(define legume2 (make-str-reader "tomate"))
(define legume3 (make-str-reader "pois"))

(assert (simple-matching-test (reg-concat* legume1 legume2 legume3) "patatetomatepois"))

(assert (not (simple-matching-test (reg-concat* legume1 (reg-zero-or-more read-any) legume2 (reg-zero-or-more read-any)) "patate et brocoli !")))
(assert (simple-matching-test (reg-concat* legume1 (reg-zero-or-more read-any) legume3 (reg-zero-or-more read-any)) "patate et pois !"))

(assert (simple-matching-test (reg-concat* (reg-zero-or-more (reg-or* legume1 legume2))
                                   legume1
                                   (reg-zero-or-more read-any)
                                   legume2)
                                   "patatepatatetomatepatatepatate et tomate !"))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (make-block-reader R tag)
  (lambda (fail success input accum)
    (R fail
       ; new success function that adds to the accumulator
       (lambda (f i a)
         (success f i (cons (list tag (reverse a)) ; because we accumulate upside down
                            accum)))
       input
       '() ; start empty at every block
       )))

; Don't accumulate anything from those blocks.
(define (make-block-reader-drop R)
  (lambda (fail success input accum)
    (R fail
       ; new success function that adds to the accumulator
       (lambda (f i a) (success f i accum))
       input
       '() ; start empty at every block
       )))



; Because sometimes we want to match the end of the expression.
; It's useful to say that we want nothing but whitespace after a termininating semi-colon.
(define (read-end fail success input accum)
  (if (empty? input)
      (success fail input accum)
      (fail input accum)))

(define legume1 (reg-concat (make-str-reader "patate") (reg-or read-nothing (make-char-reader #\s))))
(define legume2 (reg-concat (make-str-reader "tomate") (reg-or read-nothing (make-char-reader #\s))))
(define legume3 (make-str-reader "pois"))
(define LEGUME (make-block-reader (reg-or* legume1 legume2 legume3) 'legume))

(define fruit1 (reg-concat (make-str-reader "pomme") (reg-or read-nothing (make-char-reader #\s))))
(define fruit2 (reg-concat (make-str-reader "fraise") (reg-or read-nothing (make-char-reader #\s))))
(define FRUIT (make-block-reader (reg-or* fruit1 fruit2) 'fruit))

(define UNMATCHED (make-block-reader (reg-zero-or-more read-any) 'UNMATCHED))

(define PADDING (make-block-reader-drop (reg-zero-or-more read-any)))
(define END (make-block-reader-drop read-end))

;;;;;;;;;;;;;;;;; second unit tests;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define (simple-token-matching R str)
  (define (fail input-stream accum)
    (printf "Failed to match one character before position ~s\n" (list->string input-stream))
    #f)
  (define (success fail input-stream accum)
    (printf "Matched successfully.\n")
    ;(display accum) (newline)
    ;#t
    (list (cons 'accum accum) (cons 'fail (lambda () (fail input-stream accum)))))
  (R fail success (string->list str) '()))

(define (retrieve-match L)
  (cdr (assq 'accum L)))

; fails and retries at the same place ... something is wrong
(define (fail-match L)
  ((cdr (assq 'fail L))))

(simple-token-matching (reg-or* LEGUME FRUIT UNMATCHED) "patates et tomates")

(define A (simple-token-matching (make-block-reader (reg-concat* PADDING
                                                                 (reg-or* LEGUME FRUIT)
                                                                 PADDING
                                                                 (reg-or* LEGUME FRUIT)
                                                                 PADDING
                                                                 END)
                                                    'matches)
                                 "Je veux des patates et des tomates. Une fraise suffirait aussi."))

(define (exhaustive-match A)
  (if (not (eq? A #f))
      (begin (display (retrieve-match A))
             (newline)
             (exhaustive-match (fail-match A))
             )
      #f))

(exhaustive-match A)
;(retrieve-match A)
;(retrieve-match (fail-match A))
;(retrieve-match (fail-match (fail-match A)))
;(retrieve-match (fail-match (fail-match (fail-match A))))
;(retrieve-match (fail-match (fail-match (fail-match (fail-match A)))))