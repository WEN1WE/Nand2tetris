// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@index
M=0
D=0
(LOOP) 
	@24576
	D=M
	@draw		//If a key is pressed, the program will draw a blackpoint.
	D;JGT
	@clear
	D;JEQ
(draw)
	@index
	D=M
	@SCREEN
	A=A+D       //Changing A will change memory[A]
	M=1
	@index
	M=M+1
	@LOOP
	0;JMP
(clear)
	@index
	D=M
	@LOOP
	D;JEQ
	@SCREEN
	A=A+D
	M=0
	@index
	M=M-1
	@LOOP
	0;JMP