CFLAGS=-O3
LDFLAGS=-s

all: score-printer timed-pipe mint-scorer

mint-scorer: utilsV3
	$(CC) $(CFLAGS) $(LDFLAGS) $(addsuffix .o, $^) $@.c -o $@

score-printer: utilsV3
	$(CC) $(CFLAGS) $(LDFLAGS) $(addsuffix .o, $^) $@.c -o $@

timed-pipe: utilsV3
	$(CC) $(CFLAGS) $(LDFLAGS) $(addsuffix .o, $^) $@.c -o $@

utilsV3:
	$(CC) -c $(CFLAGS) $@.c -o $@.o

clean:
	rm -f *.o timed-pipe score-printer mint-scorer
