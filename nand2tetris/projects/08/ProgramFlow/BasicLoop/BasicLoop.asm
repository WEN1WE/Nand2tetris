@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@0
D=A
@LCL
A=M
AD=D+A
@R15
M=D
@SP
A=M
D=M
@R15
A=M
M=D
(LOOP_START)
@0
D=A
@ARG
A=M
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@LCL
A=M
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
A=M
D=A+D
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@0
D=A
@LCL
A=M
AD=D+A
@R15
M=D
@SP
A=M
D=M
@R15
A=M
M=D
@0
D=A
@ARG
A=M
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
A=M
D=A-D
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@0
D=A
@ARG
A=M
AD=D+A
@R15
M=D
@SP
A=M
D=M
@R15
A=M
M=D
@0
D=A
@ARG
A=M
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@LOOP_START
D;JNE
@0
D=A
@LCL
A=M
AD=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
