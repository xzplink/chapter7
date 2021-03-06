/*
 * @file name: tcp-server.c
 * on 2016/10/10.
 */

#include "util-afpacket.h"
#include "util-tools.h"

int main(int argc, char* argv[])
{
    AFPacketInstance    *instance;
    Packet    p, *new_pkt;
    p.pkt   = calloc(2000,1);
    int   pkt_len = 0;
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
        if(pkt_len > 0){
            printf("[*] we have receive :%d pkts.\n", ++i);
            if(p.tcph != NULL){
                /* Just deal with SYN pkt from client, not (SYN|ACK) */
                if((p.tcph->th_flags & (TH_SYN|TH_ACK)) == (TH_SYN|TH_ACK)){
                    print_packet_info(&p);
                    continue;
                } else if (p.tcph->th_flags & TH_SYN) {
                    print_packet_info(&p);
                    new_pkt = exchange_for_respond_pkt(&p, (TH_SYN|TH_ACK));
                    /* update Seq & Ack number. */
                    new_pkt->tcph->th_ack = htonl(ntohl(new_pkt->tcph->th_seq) + 1);
                    new_pkt->tcph->th_seq = 0;

                    ReCalculateChecksum(new_pkt);
                    print_packet_info(new_pkt);
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
}
