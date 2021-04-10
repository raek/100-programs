# Solving Kepler's Equation

This program numerically finds solutions to Kepler's equation. The
equation plays an important role in orbital mechanics and is written

    M = E - e sin E

where `M` is the "mean anomaly", `E` is the "eccentric anomaly", and
`e` is the "eccentricity". It is interesting because `E` occurs both
as an argument to `sin` and "on the same level" as the result of
`sin`. The equation is transendental which means that it cannot be
solved for `E` algebraically.

This program caluclates `E(M)` numerically using the Newton-Raphson
method by finding the root to the function

    f(E) = E - e sin E - M

Do do that, the derivative of `f` is needed, which is

    f'(E) = 1 - e cos E

These can then be plugged into the Newton-Raphson formula for
incrementally improving solution values:

                    E - e sin E - M
    E_(n+1) = E_n - ---------------
                      1 - e cos E

The formula is iterated until the difference between the value plugged
in and the improved value that comes out is less than some epsilon. A
way of implementing this is beatifully explained in the paper "Why
Functional Programming Matters" by John Hughes.

The program then plots `M(E)`. The values for `E(M)` (which can be
computed analytically) are also plotted with dots for comparison, but
with axes flipped so that the two functions overlap.

## How to Run It

    stack install Chart Chart-cairo
    stack runhaskell Plot.hs

## What I Learned

* Sometimes there are libraries that does exactly what you need. In
  this case Chart was a perfect fit for me. I did not have to digress
  from the problem I actually wanted to solve. I copied an example and
  it worked.
* It is easy to make errors when you code (duh!). I made a silly
  mistake when I differentiated `f(E)` and it took a while to figure
  out where the problem was. It was hard to debug the program since I
  could only excercie the "leaves" (the numerics) by running the
  "root" (the main program). Had I written some tests, I could have
  excercied only the parts of the program I needed to debug (DUH!).

## My Story of the Problem and the Solution

I read "Why Functional Programming Matters" out of curiosity and
because I really like FP in general. I thought that eploiting laziness
to implement Newton-Raphson in a such composable way was very
elegant. I had no use for numerical methods for any of my projects at
that point, though.

A year or two later I started to play Kerbal Space Program and got
interested in accurately calculating the position of a celestial body
in an elliptical orbit at a given point in time. That would be a
different and interesting alternative to the "standard" approach to
use Euler's method in computer ga mes. Reading up on Wikipedia I found
out that I would need to solve Kepler's equation, and that it was
common to do it numerically. I then recalled that there was a
beautiful way of doing this in Haskell!

Yet another year or two later I actually implemented it, because I
wanted to practice coding by writing lots of small but purposeful
programs.
