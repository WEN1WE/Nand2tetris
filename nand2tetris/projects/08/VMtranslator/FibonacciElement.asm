(Sys.init)
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
@LABEL1
D=A
@SP
A=M
M=D
@SP
M=M+1
@R1
D=M
@SP
A=M
M=D
@SP
M=M+1
@R2
D=M
@SP
A=M
M=D
@SP
M=M+1
@R3
D=M
@SP
A=M
M=D
@SP
M=M+1
@R4
D=M
@SP
A=M
M=D
@SP
M=M+1
@6
D=A
@R0
A=M
D=A-D
@R2
M=D
@R0
D=M
@R1
M=D
@Main.fibonacci
0;JMP
(LABEL1)
(WHILE)
@WHILE
0;JMP