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
    p.pkt   = calloc(20000,1);
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
        pkt_len = afpacket_acquire(instance, &p, 20000);
        if(pkt_len>0){
            /* Just deal with ACK pkt from client, not (SYN|ACK) */
             if((p.tcph->th_flags & TH_ACK) && !(p.tcph->th_flags & TH_SYN)){
                 continue;
             } else if (p.tcph->th_flags & TH_SYN) {
                 new_pkt = exchange_for_respond_pkt(&p, (TH_SYN|TH_ACK));
                 ReCalculateChecksum(new_pkt);
                 afpacket_send(instance, new_pkt);
            }
        }
    }
}
