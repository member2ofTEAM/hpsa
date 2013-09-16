#include "utils.h"

void *xmalloc(size_t size)
{
	void *ptr = malloc(size);

	if(ptr == NULL) {
		perror("Error allocating memory ");
		exit(EXIT_FAILURE);
	} else
		return ptr;
}

void *xcalloc(size_t nmemb, size_t size)
{
	void *ptr = calloc(nmemb, size);

	if(ptr == NULL) {
		perror("Error allocating memory ");
		exit(EXIT_FAILURE);
	} else
		return ptr;
}

char *xstrdup(const char *str)
{
	char *newStr = strdup(str);

	if(newStr == NULL) {
		perror("Error allocating memory ");
		exit(EXIT_FAILURE);
	} else
		return newStr;
}

void *xrealloc(void *ptr, size_t size)
{
	ptr = realloc(ptr, size);
	if(ptr == NULL) {
		perror("Error allocating memory ");
		exit(EXIT_FAILURE);
	} else
		return ptr;
}

int xopen(const char *path, int flags)
{
	int fd = open(path, flags);

	if(fd == -1) {
		perror("Error opening file ");
		exit(EXIT_FAILURE);
	} else
		return fd;
}

FILE *xfopen(const char *path, const char *mode)
{
	FILE *f = fopen(path, mode);

	if(f == (FILE*) NULL) {
		perror("Error opening file ");
		exit(EXIT_FAILURE);
	} else
		return f;
}

FILE *xfdopen(int fd, const char *mode)
{
	FILE *f = fdopen(fd, mode);

	if(f == (FILE*) NULL) {
		perror("Error opening file ");
		exit(EXIT_FAILURE);
	} else
		return f;
}

pid_t xfork(void)
{
	pid_t pid = fork();
	if(pid == -1) {
		perror("Error forking ");
		exit(EXIT_FAILURE);
	} else
		return pid;
}

void str_tolower(char *str)
{
	for(; *str != '\0'; str++)
		if(*str >= 'A' && *str <= 'Z')
			*str = *str + 32;	// - 'A' + 'a'
}

char *neg_strchr(char *s, int c)
{
	while(*s++ == c);
	if(*s == '\0')
		return (char*) NULL;
	else
		return s;
}

char *itoa(int n, char *buffer)
{
	char *ptr = buffer;
	int log;

	if(n < 0) {
		*ptr++ = '-';
		n = 0 - n;
	}
	
	for(log = n; log != 0; log /= 10)
		ptr++;
	
	for(*ptr = '\0'; n != 0; n /= 10)
		*--ptr = n % 10 + '0';

	return buffer;
}

int hexatoi(const char *hex)
{
	register int size;
	register unsigned res, pow;
	
	for(size = 0; hex[size] != '\0'; size++);
		
	for(pow = 1, res = 0, size--; size >= 0; pow <<= 4, size--)
		res += pow * (hex[size] >= 'a' ? hex[size] - 87 : (hex[size] >= 'A' ? hex[size] - 55 : hex[size] - '0'));
	return res;
}

// xmalloc, strlen
char *const_append(const char *str1, const char *str2)
{
	char *newStr = (char*) NULL;
	size_t len = strlen(str1);

	newStr = (char*) xmalloc(len + strlen(str2) + 1);
	strcpy(newStr, str1);
	strcpy(newStr + len, str2);
	return newStr;
}

// xrealloc, strlen
char *append(char *str1, const char *str2)
{
	size_t len = strlen(str1);

	str1 = (char*) xrealloc(str1, len + strlen(str2) + 1);
	strcpy(str1 + strlen(str1), str2);
	return str1;
}

// xmalloc, xrealloc
char *readLine(FILE *stream)
{
	register unsigned i = 0;
	unsigned currentSize = 32;
	register char c;
	char *str = (char*) xmalloc(32);
	flockfile(stream);

	while((c = fgetc_unlocked(stream)) != EOF && c != '\n') {
		if(i == currentSize)
			str = (char*) xrealloc(str, currentSize <<= 1);
		str[i++] = c;
	}

	funlockfile(stream);
	if(i == currentSize)
		str = (char*) xrealloc(str, currentSize += 1);
	else if(c == EOF && i == 0) {
		free(str);
		return (char*) NULL;
	} else
		str = realloc(str, i+1);	// freeing space -> no need to check for null
	str[i] = '\0';
	return str;
}

// xmalloc, xrealloc
char *read_file_descriptor(int fd)
{
	unsigned currentSize = 32;
	ssize_t i = 0;
	char *str = (char*) xmalloc(32);

	/* read (currentSize - i) chars at a time, double currentSize and increment
	 * i by the number of characters read and repeat until no more characters 
	 * are available */
	do {
		i += read(fd, str + i, currentSize - i);	
		if(i == currentSize)
			str = xrealloc(str, currentSize <<= 1);
	} while(i << 1 == currentSize);

	if(i == -1 || str[0] == 4) {	// 4 == EOT (End Of Transmission, for sockets),
		// see 'ascii' manpage for more details
		free(str);
		return (char*) NULL;
	} else {
		/* remove all non-printable characters from end of string
		 * see 'isprint' manpage for more details */
		while(! isprint(str[i-1]))
			i--;
		/* allocate precisely as much memory (not a single byte more)
		 * as is needed to contain the data */
		if(i == currentSize)
			str = (char*) xrealloc(str, currentSize += 1);
		else	// freeing space -> no need to check for NULL
			str = realloc(str, i+1);
		str[i] = '\0';
	}
	return str;
}

// xmalloc
// returnArray is set to NULL if all chars in str are separator
// returnArray and all elements in returnArray are dynamically allocated -> free them all when done
size_t split_str(const char *str, const char separator, char ***returnArray)
{
	register int i;
	size_t count = 1;

	// COMMENT NEXT 6 LINES TO NOT SKIP CONSECUTIVE separator
	// CHARS AT START OF str
	while(*str == separator)
		str++;
	if(*str == '\0') {
		*returnArray = (char**) NULL;
		return 0;
	}

	for(i = 0; str[i] != '\0'; i++)
		//count += (str[i] == separator);
		count += (str[i] == separator && str[i+1] != separator && str[i+1] != '\0');
	// REPLACE PREVIOUS LINE WITH ABOVE COMMENTED LINE
	// TO NOT SKIP OVER CONSECUTIVE SEPARATORS

	*returnArray = (char**) xmalloc(count * sizeof(char*));

	for(count = i = 0; str[i] != '\0'; i++) {
		if(str[i] == separator) {
			// COMMENT NEXT 3 LINES TO NOT SKIP OVER CONSECUTIVE SEPARATORS
			if(i == 0)
				str++;
			else {
				(*returnArray)[count] = (char*) xmalloc(i+1);
				strncpy((*returnArray)[count], str, i);
				(*returnArray)[count++][i] = '\0';
				str += i+1;
			}	// COMMENT THIS LINE TO NOT SKIP OVER CONSECUTIVE SEPARATORS
			i = -1;
		}
	}
	if(i != 0) {
		(*returnArray)[count] = (char*) xmalloc(i+1);
		strcpy((*returnArray)[count++], str);
	}
	return count;
}

#include <sys/stat.h>
int is_dir(char *path)
{
	struct stat buf;

	if(stat(path, &buf) != 0) {
		perror("Error statting file ");
		return -1;
	} else
		return S_ISDIR(buf.st_mode);
}

#ifdef	_WIN32
#define FILE_SEPARATOR	'\\'
#else
#define FILE_SEPARATOR	'/'
#endif
// xmalloc
char *make_path(const char *oldPath, const char *dirName)
{
	char *newPath = (char*) NULL;
	int len = strlen(oldPath);

	newPath = (char*) xmalloc(len + strlen(dirName) + 2);
	strcpy(newPath, oldPath);
	strcpy(newPath + len + 1, dirName);
	newPath[len] = FILE_SEPARATOR;
	return newPath;
}
#undef FILE_SEPARATOR

#include <dirent.h>
#include <errno.h>
void dirwalk(const char *path)
{
	DIR *dir;
	struct dirent *entry;
	char *newPath;

	dir = opendir(path);
	if(dir == (DIR*) NULL)
		fprintf(stderr, "Error opening directory '%s' : %s.\n", path, strerror(errno));
	else {
		// iterate over linked list. When we have examined all files in directory, readdir() returns NULL
		while((entry = readdir(dir)) != (struct dirent*)NULL) {
			if(strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0) {
				newPath = make_path(path, entry->d_name);
#ifdef _WIN32
				if(is_dir(newPath))
#else
				if(entry->d_type == DT_DIR)	// windows sucks, this line works on unix-based OSs only
#endif
					dirwalk(newPath);
				free(newPath);
			}
		}
		closedir(dir);
	}
}

void register_signal_handler(int signum, void (*sighandler)(int))
{
	struct sigaction new_sigaction;

	memset(&new_sigaction, 0, sizeof(struct sigaction));
	new_sigaction.sa_handler = sighandler;
	if(sigaction(signum, &new_sigaction, NULL) != 0) {
		perror("Error registering signal handler ");
		exit(EXIT_FAILURE);
	}
}

// Don't bother trying to run the following on windows. You're wasting your time
#ifndef _WIN32
// Color management

void setColorEnv(Color c, Color bgc, Font f)
{
	printf("\x1B[%d;%dm", c + 30, f);
	session.c = c;
	session.f = f;
	printf("\x1B[%dm", bgc + 40);
	session.bgc = bgc;
}

void printString(char *str, Color c, Color bgc, Font f)
{
	ColorEnv temp = session;
	setColorEnv(c, bgc, f);
	printf("%s", str);
	setColorEnv(temp.c, temp.bgc, temp.f);
}

#define reset_color_profile()		printf("\x1B[0m")

#include <termios.h>

// input character display
void turn_echoing_off(void)
{
	struct termios term;

	if(tcgetattr(STDIN_FILENO, &term) != 0) {
		perror("Error manipulating terminal ");
		exit(EXIT_FAILURE);
	}
	term.c_lflag &= ~ECHO;
	if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &term) != 0) {
		perror("Error manipulating terminal ");
		exit(EXIT_FAILURE);
	}
}

void turn_echoing_on(void)
{
	struct termios term;

	if(tcgetattr(STDIN_FILENO, &term) != 0) {
		perror("Error manipulating terminal ");
		exit(EXIT_FAILURE);
	}
	term.c_lflag |= ECHO;
	if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &term) != 0) {
		perror("Error manipulating terminal ");
		exit(EXIT_FAILURE);
	}
}

// program reads input without user having to press enter
void instant_getchar(void)
{
	struct termios term;

	if(tcgetattr(STDIN_FILENO, &term) != 0) {
		perror("Error manipulating terminal ");
		exit(EXIT_FAILURE);
	}
	term.c_lflag &= ~ICANON;
	term.c_cc[VMIN] = 1;	
	term.c_cc[VTIME] = 0;

	if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &term) != 0) {
		perror("Error manipulating terminal ");
		exit(EXIT_FAILURE);
	}
}

void normal_getchar(void)
{
	struct termios term;

	if(tcgetattr(STDIN_FILENO, &term) != 0) {
		perror("Error manipulating terminal ");
		exit(EXIT_FAILURE);
	}
	term.c_lflag |= ICANON;
	if (tcsetattr(STDIN_FILENO, TCSAFLUSH, &term) != 0) {
		perror("Error manipulating terminal ");
		exit(EXIT_FAILURE);
	}
}

#endif

