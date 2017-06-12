# Do NOT change this file!


ASFLAGS := -m32
CFLAGS  := -m32 -g -std=c11 -Wall -Werror -D_GNU_SOURCE
LDFLAGS := -m32
LDLIBS  := -lcrypto
PROGS   := zookld zookfs zookd \
           zookfs-exstack zookd-exstack \
           zookfs-nxstack zookd-nxstack \
           zookfs-withssp zookd-withssp \
           shellcode.bin run-shellcode

ifeq ($(wildcard /usr/bin/execstack),)
  ifneq ($(wildcard /usr/sbin/execstack),)
    ifeq ($(filter /usr/sbin,$(subst :, ,$(PATH))),)
      PATH := $(PATH):/usr/sbin
    endif
  endif
endif

all: $(PROGS)
.PHONY: all

zookld zookd zookfs: %: %.o http.o
zookfs-withssp zookd-withssp: %: %.o http-withssp.o
run-shellcode: %: %.o

%-nxstack: %
	cp $< $@

%-exstack: %
	cp $< $@
	execstack -s $@

%.o: %.c
	$(CC) $< -c -o $@ $(CFLAGS) -fno-stack-protector

%-withssp.o: %.c
	$(CC) $< -c -o $@ $(CFLAGS)

%.bin: %.o
	objcopy -S -O binary -j .text $< $@

.PHONY: test_bugs
test_bugs:
	tests/test_bugs.py bugs.txt

.PHONY: test_crash_1
test_crash_1: bin.tar.gz crash_1.py shellcode.bin
	tar xf bin.tar.gz
	tests/test_crash.sh zook-exstack.conf ./crash_1.py

.PHONY: test_crash_2
test_crash_2: bin.tar.gz crash_2.py shellcode.bin
	tar xf bin.tar.gz
	tests/test_crash.sh zook-exstack.conf ./crash_2.py

.PHONY: test_unlink_exstack
test_unlink_exstack: bin.tar.gz unlink_exstack.py shellcode.bin
	tar xf bin.tar.gz
	tests/test_unlink.sh zook-exstack.conf ./unlink_exstack.py

.PHONY: test_unlink_libc_1
test_unlink_libc_1: bin.tar.gz unlink_libc_1.py shellcode.bin
	tar xf bin.tar.gz
	tests/test_unlink.sh zook-nxstack.conf ./unlink_libc_1.py

.PHONY: test_unlink_libc_2
test_unlink_libc_2: bin.tar.gz unlink_libc_2.py shellcode.bin
	tar xf bin.tar.gz
	tests/test_unlink.sh zook-nxstack.conf ./unlink_libc_2.py

.PHONY: test
test: test_bugs test_crash_1 test_crash_2 test_unlink_exstack test_unlink_libc_1 test_unlink_libc_2


.PHONY: clean
clean:
	rm -f *.o *.pyc *.bin $(PROGS)
