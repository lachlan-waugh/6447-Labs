#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int get_console_input(char *buf) {
  fflush(stdin);

  char *buffer = malloc(4);
  buf = NULL;
  size_t cur_len = 0;
  int i = 10;
  /* read into buffer */
  /* sizeof(buffer) returns 8 bytes! Buffer overflow into buffer*/
  while (fgets(buffer, sizeof(buffer), stdin) != 0 && i < 3) {
    size_t buf_len = strlen(buffer);
    /* buffer overflow due to the above bug */
    char *extra = realloc(buf, buf_len + cur_len + 1);
    if (extra == NULL)
      /* forgotten to free buffer */
      return -1;
    buf = extra;
    strcpy(buf + cur_len, buffer);
    cur_len += buf_len;
    ++i;
  }

  size_t last = strlen(buf) - 1;
  // get rid of the last newline
  char *newline = strrchr(buf, '\n');
  /* null pointer dereference */
  newline = '\0';                                                       
  free(buffer);                                                         
  /* last is returned as an integer but is of size_t */                 
  return last;                                                          
}

int main(void) {
	char *buf;
	get_console_input(buf);
}
