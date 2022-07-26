#include <stdio.h>
#include <stdlib.h>
#include <string.h>



char* s = "/bin/sh";

void _(){  
    __asm__("xor eax, eax");
    __asm__("ret");

    __asm__ __volatile__("inc eax");  
    __asm__ __volatile__("ret");

    __asm__ __volatile__("pop ebx");  
    __asm__ __volatile__("ret");

    __asm__ __volatile__("pop ecx");  
    __asm__ __volatile__("pop edx");  
    __asm__ __volatile__("ret");

    __asm__ __volatile__("int 0x80");  
    __asm__ __volatile__("ret");
}
int vuln(){
    puts("Now give me your age");
    char input[8];
    fgets(input,24,stdin);
}

int main(){
    setbuf(stdout, NULL);
    printf("First give me your name...");
    char name[512] = {0};
    fgets(name, 512, stdin);

    vuln();

    printf("Bye!\n");
}
