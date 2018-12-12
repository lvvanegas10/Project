# Sequencing of two-dimensional cut of material

contains a solution for the problem of sequencing of two-dimensional cut of material, based on the problem of the traveling salesman (TSP). The problem of two-dimensional material cutting sequencing (PSCB) consists of generating a sequence of movements required to cut a rectangular two-dimensional plate into smaller rectangular pieces from a stipulated pattern for the plate. To achieve a solution, in this paper we discuss the generation of a graph based on distance matrix that allows using a heuristic to solve the problem with TSP. To solve the problem with TSP we use the Lin-Kernighan heuristic, with the implementation provided by LKH. 

This is factible and relative fast solution to the problem of sequencing of two-dimensional cut of material.

In the LKH folder, dowload and unzip LKH (http://akira.ruc.dk/~keld/research/LKH/). Then, follow the install instructions. 

To run, type in console 

      python InvokeLKH.py

This is an adaptation of the interface provided in https://github.com/perrygeo/pytsp
