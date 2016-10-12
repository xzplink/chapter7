/*
 * @file name: tcp-server.c
 * Created by zhaozhang@yxlink.com
 * on 2016/10/10.
 */

#include "util-afpacket.h"
#include "util-tools.h"

int main(int argc, char* argv[])
{
    AFPacketInstance    *instance;
    Packet    p, *new_pkt;
    p.pkt   = calloc(2000,1);
    uint64_t   pkt_len;

    if (argc!=2) {
        printf("ethx num_per_printf !\n");
        exit(0);
    }

    //afpacket init
    if (afpacket_init(argv[1], (void **)(&instance)) == AF_ERROR) {
        printf("afpacket_init fail , pkt_recv thread quit!\n");
        return ;
    }
    if (afpacket_start((void *)instance) == AF_ERROR) {
        printf("afpacket_start fail , pkt_recv thread quit!\n");
        return ;
    }

    while(1){
        memset(p.pkt, 0, 2000);
        pkt_len = afpacket_acquire(instance, &p, 2000);
        if(pkt_len>0){
            /* Just deal with ACK pkt from client, not (SYN|ACK) */
             if((p.tcph->th_flags & TH_ACK) && !(p.tcph->th_flags & TH_SYN)){
                 printf("^^^^^^^^^^^^^^^^^^^^^^\n");
                 continue;
             } else if (p.tcph->th_flags & TH_SYN) {
                 printf("aaaaaaaaaa\n");
                 new_pkt = exchange_for_respond_pkt(&p, (TH_SYN|TH_ACK));
                 printf("bbbbbbbbbbbb\n");
                 ReCalculateChecksum(new_pkt);
                 printf("ccccccccccc\n");
                 afpacket_send(instance, new_pkt);
                 printf("dddddddddddd\n");
            }
        }
    }
}
