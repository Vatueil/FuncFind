arch = {'REGISTER' : '^(?!.*\[.+\]).*(r0|r1|r2|r3|r4|r5|r6|r7|r8|r9|r10|r11|r12|r13|r14|sp|lr|pc)',
'NUMBER' : '(#[0-9A-F])|(#0x[0-9A-F])',
'ADDRESS' : '.*0x[0-9A-F]h',
'MEM_ACCESS' : '.*\[.+\]',
'LOAD' : 'LDR',
'STORE' : ('STR','SD')
}