## core information
## build-configuration info
CC           = gcc

OBJ_DIR     = ./obj
OBJS        = $(OBJ_DIR)/util-afpacket.o \
              $(OBJ_DIR)/util-tools.o


HEADS   = util-tools.h util-afpacket.h ether-type.h

EXEC    = tcp-server tcp-client

all: $(EXEC)

tcp-client : $(OBJS) $(OBJ_DIR)/tcp-client.o
	$(CC) $(OBJS) $(OBJ_DIR)/tcp-client.o -o tcp-client -lpthread -lm

tcp-server :  $(OBJS) $(OBJ_DIR)/tcp-server.o
	$(CC) $(OBJS) $(OBJ_DIR)/tcp-server.o -o tcp-server -lpthread -lm

$(OBJ_DIR)/util-afpacket.o : util-afpacket.c $(HEADS)
	$(CC)  -c util-afpacket.c -o $(OBJ_DIR)/util-afpacket.o

$(OBJ_DIR)/util-tools.o : util-tools.c $(HEADS)
	$(CC)  -c util-tools.c -o $(OBJ_DIR)/util-tools.o

$(OBJ_DIR)/tcp-client.o : tcp-client.c $(HEADS)
	$(CC)  -c tcp-client.c -o $(OBJ_DIR)/tcp-client.o

$(OBJ_DIR)/tcp-server.o : tcp-server.c $(HEADS)
	$(CC)  -c tcp-server.c -o $(OBJ_DIR)/tcp-server.o

.PHONY : clean
clean:
	-rm -f $(EXEC) $(OBJS) *.bak

