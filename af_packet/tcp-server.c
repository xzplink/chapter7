/*
 * @file name: tcp-server.c
 * Created by zhaozhang@yxlink.com
 * on 2016/10/10.
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "util-afpacket.h"

int main(int argc, char* argv[])
{
    AFPacketInstance    *instance;
    Packet    p, *new_pkt;
    p.pkt   = calloc(200000,1);
    uint64_t   pkt_len;

    if (argc!=2)
    {
        printf("ethx num_per_printf !\n");
        exit(0);
    }

    //afpacket init
    if (afpacket_init(argv[1], (void **)(&instance)) == AF_ERROR)
    {
        printf("afpacket_init fail , pkt_recv thread quit!\n");
        return ;
    }
    if (afpacket_start((void *)instance, 1) == AF_ERROR)
    {
        printf("afpacket_start fail , pkt_recv thread quit!\n");
        return ;
    }

    while(1){
        pkt_len = afpacket_acquire(instance, &p, 200000);

        new_pkt = change_to_respond_pkt(&p);

        if (pkt_len>0) {
            afpacket_send(instance, new_pkt);
        }
    }
}
