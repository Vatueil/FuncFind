arch = {'REGISTER' : '$(zero|at|v0|v1|v2|v3|v4|a0|a1|a2|a3|t0|t1|t2|t3|t4|t5|t6|t7|t8|t9|s0|s1|s2|s3|s4|s5|s6|s7|s8|k0|k1|gp|sp|ra|f0|f12|f13|f14|f15)',
'NUMBER' : '(0-9A-F)|(0x[0-9A-F])',
'ADDRESS' : '.*0x[0-9A-F]h',
'MEM_ACCSESS' : '.*\(.+\)',
'LOAD' : 'LB|LW|LI',
'STORE' : 'SB|SW'
}
