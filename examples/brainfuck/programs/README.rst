Brainfuck programs
==================

A few programs implemented in the Brainfuck language.

beer.bf
-------

Bottles of beer.

Copied from https://copy.sh/brainfuck.

.. code-block:: text

   ❯ brainfuck beer.bf | tail
   2 Bottles of beer on the wall
   2 Bottles of beer
   Take one down and pass it around
   1 Bottle of beer on the wall

   1 Bottle of beer on the wall
   1 Bottle of beer
   Take one down and pass it around
   0 Bottles of beer on the wall

bench.bf
--------

A benchmark program printing the alphabet.

Copied from https://github.com/kostya/benchmarks/blob/master/brainfuck/bench.b.

.. code-block:: text

   ❯ brainfuck bench.bf
   ZYXWVUTSRQPONMLKJIHGFEDCBA

hello_world.bf
--------------

Hellow World example.

Copied from https://en.wikipedia.org/wiki/Brainfuck.

.. code-block:: text

   ❯ brainfuck hello_world.bf
   Hello World!

os.bf
-----

A tiny OS.

Copied from https://www.linusakesson.net/programming/brainfuck/index.php.

.. code-block:: text

   ❯ brainfuck os.bf
   STARTING
   BRAINOS VER 1
   A FOR HELP
   OS>A
   A > HELP
   B > CHARCODE
   Z > HALT
   OS>1
   ENTER CHAR
   >
   31
   OS>Z
   HALTING

triangle.bf
-----------

Prints a triangle.

Copied from https://copy.sh/brainfuck.

.. code-block:: text

   ❯ brainfuck triangle.bf
                                   *
                                  * *
                                 *   *
                                * * * *
                               *       *
                              * *     * *
                             *   *   *   *
                            * * * * * * * *
                           *               *
                          * *             * *
                         *   *           *   *
                        * * * *         * * * *
                       *       *       *       *
                      * *     * *     * *     * *
                     *   *   *   *   *   *   *   *
                    * * * * * * * * * * * * * * * *
                   *                               *
                  * *                             * *
                 *   *                           *   *
                * * * *                         * * * *
               *       *                       *       *
              * *     * *                     * *     * *
             *   *   *   *                   *   *   *   *
            * * * * * * * *                 * * * * * * * *
           *               *               *               *
          * *             * *             * *             * *
         *   *           *   *           *   *           *   *
        * * * *         * * * *         * * * *         * * * *
       *       *       *       *       *       *       *       *
      * *     * *     * *     * *     * *     * *     * *     * *
     *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *
    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

yapi.bf
-------

Prints an approximation of the number pi.

Copied from https://copy.sh/brainfuck.

.. code-block:: text

   ❯ brainfuck yapi.bf
   3.14070455282885
