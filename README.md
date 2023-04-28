# NondeterministicTuringMachine

A simple example of a Nondeterministic Turing Machine. The program for the machine is written in a text file with a structure described below:

There are headers written single on a line: ```%STATES```, ```%ALPHABET```, ```%START_STATE```, ```%SPACE```, ```%FINAL_STATES```, ```%PROGRAM```, ```%END```.
File must end with an ```%END``` statement. After a header there must be a line break and then required information splitted with ```;```. All lines except headers must end with ```;```
An example of a configuring and programming NTM are given below:
```
%STATES
q0; q1;
q2; q3;
%ALPHABET
0; 1; B;
%START_STATE
q0;
%SPACE
B;
%FINAL_STATES
q3;
%PROGRAM
(q0, 1);(q0, 0, R);(q1, 0, R);
(q1, 0);(q2, 1, L);
(q1, B);(q3, B, R);
(q2, 0);(q0, 0, R);
%END
```

Running: ```./turing.py *path_to_program*```
