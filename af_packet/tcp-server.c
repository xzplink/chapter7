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
    uint32_t   i = 0, send_success = -1;

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
            printf("[*] we have receive :%d pkts.\n", ++i);
            /* Just deal with ACK pkt from client, not (SYN|ACK) */
             if((p.tcph->th_flags & TH_ACK) && !(p.tcph->th_flags & TH_SYN)){
                 printf("^^^^^^^^^^^^^^^^^^^^^^\n");
                 continue;
             } else if (p.tcph->th_flags & TH_SYN) {
                 new_pkt = exchange_for_respond_pkt(&p, (TH_SYN|TH_ACK));
                 ReCalculateChecksum(new_pkt);
                 send_success = afpacket_send(instance, new_pkt);
                 if (send_success <= 0) {
                     printf("afpcket_send fail!\n");
                 } else{
                     printf("[*] we have send :%d (SYN|ACK) pkts.\n", ++i);
                 }

            }
        }
    }
}
