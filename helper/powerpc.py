arch = {'REGISTER' : '(r0|r1|r2|r3|r4|r5|r6|r7|r8|r9|r10|r11|r12|r13|r14|r15|r16|r17|r18|r19|r20|r21|r22|r23|r24|r25|r26|r27|r28|r29|r30|r31|lr|cr)',
'NUMBER' : '([0-9A-F])|(#0x[0-9A-F])',
'ADDRESS' : '.*0x[0-9A-F]h',
'MEM_ACCESS' : '.*\(.+\)',
'LOAD' : 'LB|LH|LW|LS|LMW',
'STORE' : 'STW|STB|STH|STM|STS'
}