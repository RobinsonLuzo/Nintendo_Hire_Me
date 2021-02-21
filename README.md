# Nintendo Hire Me!!!!

In November 2020 Fabien from [LiveOverflow](https://www.youtube.com/channel/UClcE-kVhqyiHCcjYwcpfj9w) described a challenge posted by Nintendo European Research & Development called "Hire Me". A C program that provides a multiple layered stage of encryption, the challenge was to find a way to provide an array of hexadecimals that, when inserted into the given code, results in the output "Hire Me!!!!!!!!".

While LiveOverflow did make a mathematical solution using Python, this used Sagemath. This version tries to make use of more regular Python to implement both the code as given to verify if a solution is correct and a solver method.

Note: the default is to generate a solution to "Hire Me!!!!!!!!" but other can also be done. A commented out version is done for "Live Overflow!!!" also to show it can be done in both the solver and problem.

There are 5 files here:
1. *hireme_problem.py* - the problem translated into Python. This has been modified from the C source to allow for the resulting string to be printed.
2. *solution.py* - the main solver for generating candidates and verifying if any of them work.
3. *calc_inverse_diff.py* - computes the inverse of the diffusion array using Gaussian-Jordan elimination. Helper file supplying methods to *main()* of *solution.py*.
4. *input_arr_soultion.txt* - when a candidate is found that satisfies the requirements for outputting the target it is written as an array of hexadecimals to this file. Stripping the resulting array of string quotations '' we can then paste this into *hireme_problem.py* as *input_arr* to generate the result.
5. *convert_bytearr_to_hex.py* - standalone version of method of writing solution bytearray to text file in hexadecimal. No longer used, but left here for illustration.

[NERD Hire Me source code:](https://www.nerd.nintendo.com/files/HireMe)
[Live Overflow video on topic:](https://www.youtube.com/watch?v=6sHSDoJ5a1s)