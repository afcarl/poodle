(define (domain route)
    (:requirements :strips :typing :equality :negative-preconditions :disjunctive-preconditions)
    (:types 
       hashnum - object
    )

    (:predicates
        (done ?num1 - hashnum ?num2 - hashnum)
	(hash-number ?num - hashnum)
	(class1-object-exists ?num1 - hashnum ?num2 - hashnum)
    )

    (:action test1 
        :parameters (?num1 - hashnum ?num2 - hashnum)
        :precondition (and
	    (hash-number ?num1)
	    (hash-number ?num2)
	    (class1-object-exists ?num1 ?num2)
        )
        :effect (and
	    (done ?num1 ?num2)
        )
    )
 
)
