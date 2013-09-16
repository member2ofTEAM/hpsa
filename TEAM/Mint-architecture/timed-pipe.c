#include "utils.h"
#include <signal.h>
#include <sys/wait.h>

#define TIME_LIMIT 120	// time limit in seconds

void launch_prgm(char *solver, char *architecture, char *args[], char *envp[]);
void terminate_process(pid_t pid);
void alarm_handler(int signum);

volatile pid_t solver_pid;
volatile pid_t architecture_pid;

int main(int argc, char *argv[], char *environ[])
{
	if(argc < 3) {
		fprintf(stderr, "Usage: %s path/to/problem-solver path/to/architecture [Arg1 [Arg2 ...]]\n", argv[0]);
		return 0;
	}

	/* when the program receives the signal SIGALRM (alarm went off),
	 * call function alarm_handler */
	register_signal_handler(SIGALRM, alarm_handler);
	
	launch_prgm(argv[1], argv[2], &argv[2], environ);

	/* wait until solver program finishes, then reset the alarm */
	waitpid(solver_pid, NULL, 0);
	alarm(0);
	/* wait for architecture program to terminate */
	waitpid(architecture_pid, NULL, 0);
	return 0;
}

/* Function called when alarm goes off. It should not be called manually
 * Terminates both the architecture and the solver programs, then exits */
void alarm_handler(int signum)
{
	switch(signum) {
		case SIGALRM:
			terminate_process(solver_pid);
			terminate_process(architecture_pid);
			fputs("Time's up!\n", stderr);
			exit(0);
			break;
		default:	// we should never get here
			fprintf(stderr, "Caught signal number %d\n"
					"Undefined program state, exiting now.\n", signum);

	}
}

/* Self-explanatory name */
void terminate_process(pid_t pid)
{
	int status;
	/* try terminating program 'gently'. If that doesn't work, try more brutal methods
	 * If more brutal methods don't work, not much we can do -> give up */
	if(kill(pid, SIGTERM) != 0 && kill(pid, SIGKILL) != 0) {
		fprintf(stderr, "Unable to kill process %d ", (int) pid);
		perror("");
		exit(EXIT_FAILURE);
	}
	/* check return status of child program */
	if(waitpid(pid, &status, 0) == -1) {
		perror("Unable to terminate properly ");
		if(errno != ECHILD)	// if child process exists (see 'waitpid' manpage for details)
			fputs("You probably have a zombie process running.", stderr);
	}
}

/*
 * Launches architecture program and solver program
 * Creates a pipe between both program and sets it up so that
 * solver's standard output appears on architecture's standard input.
 * Ends by setting an alarm to ring in TIME_LIMIT seconds.
 * For an overview of pipes, check the 'pipe' manpages:
 * $ man 2 pipe
 * $ man 7 pipe
 */
void launch_prgm(char *solver, char *architecture, char *args[], char *envp[])
{
	int pipefd[2];
	
	// Create pipe
	xpipe(pipefd);
	args[0] = architecture;
	
	/* Create child process and exec architecture program from said child process */
	if((architecture_pid = vfork()) == -1) {
		perror("Error forking program ");
		exit(EXIT_FAILURE);
	} else if(architecture_pid == 0) {	/* If this is the child process */
		close(pipefd[1]);		/* We don't need to write anything to pipe -> close write end of pipe */
		xdup2(pipefd[0], STDIN_FILENO);	/* redirect read end of pipe to standard input */
		if(execve(architecture, args, envp) == -1) {	/* launch program */
			perror("Error launching architecture program ");
			exit(EXIT_FAILURE);
		}
	} else {
		/* No need for the read end of the pipe -> close it */
		close(pipefd[0]);
		args[1] = solver;
		/* the following is the same idea as above */
		if((solver_pid = vfork()) == -1) {
			perror("Error forking program ");
			exit(EXIT_FAILURE);
		} else if(solver_pid == 0) {	/* if this is the child process */
			xdup2(pipefd[1], STDOUT_FILENO);
			if(execve(solver, args, envp) == -1) {
				perror("Error launching architecture program ");
				exit(EXIT_FAILURE);
			}
		}
		/* Set the alarm */
		/* WARNING: DO NOT move this line anywhere between a call to vfork and the end of a child process block.
		 * This line MUST remain in parent process code. */
		alarm(TIME_LIMIT);
	}
	/* Unless you want to rig the scores, there is no reason to keep this part of the pipe open -> close it */
	close(pipefd[1]);
}

