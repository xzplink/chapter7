## core information
## build-configuration info
CC           = gcc

OBJ_DIR     = ./obj
OBJS        = $(OBJ_DIR)/util-afpacket.o \
              $(OBJ_DIR)/util-tools.o    \
              $(OBJ_DIR)/tcp-client.o    \
              $(OBJ_DIR)/tcp-server.o

HEADS   = util-tools.h util-afpacket.h ether-type.h

EXEC    = tcp-client tcp-server

all: $(EXEC)

$(OBJ_DIR)/tcp-client : $(OBJS)
	$(CC) -o tcp-client $(OBJS)

$(OBJ_DIR)/tcp-server :  $(OBJS)
	$(CC) -o tcp-server $(OBJS) -lpthread -lm -static

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

