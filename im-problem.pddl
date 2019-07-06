(define (problem poo-dom)
    (:domain poo-dom)
    (:objects
        num1 num2 num3 num4 num5 - hashnum
    )
    (:init
        (class1-object-exists num1 num2)
        (hash-number num1)
        (hash-number num2)
        (hash-number num3)
        (hash-number num4)
        (hash-number num5)
    )
    (:goal (and
        (done num1 num2)
    ))
)
