/*
 * @file name: tcp-client.c
 * Created by zhaozhang@yxlink.com
 * on 2016/10/10.
 */

#include <getopt.h>
#include "util-afpacket.h"
#include "util-tools.h"

#define PKT_SEND_COUNT     5
#define PKT_RECEIVE_COUNT  5


void usage(char *prg, int exit_code)
{
    printf("tcp-client usage: %s [OPTION]\n\n", prg);
    printf("Options:\n");
    printf("  -i, --ether              set bind ether interface\n");
    printf("  -s, --smac               set source Mac Address\n");
    printf("  -d, --dmac               set destination Mac Address\n");
    printf("  -c, --count              set running thread count\n");
    printf("  -D, --daemon             run in daemon mode\n");
    printf("  -v, --verbose            be verbose\n");
    printf("  -h, --help               display this help and exit\n");
    exit(exit_code);
}

int parse_cmd_line(int argc, char** argv, AFCtx *afctx)
{
    int opt;

    struct option long_opts[] = {
            { "ether", required_argument, 0, 'i'},
            { "smac", required_argument, 0, 's' },
            { "dmac", required_argument, 0, 'd' },
            { "count", required_argument, 0, 'c'},
            { "daemon", no_argument, 0, 'D'},
            { "help", no_argument, 0, 'h' },
            { 0, 0, 0, 0}
    };

    /* getopt_long stores the option index here. */
    int option_index = 0;

    char short_opts[] = "i:s:d:c:D";
    while ((opt = getopt_long(argc, argv, short_opts, long_opts, &option_index)) != -1) {
        switch (opt) {
            case 'i':
                afctx->iface = optarg;
                break;
            case 's':
                afctx->src_mac = optarg;
                break;
            case 'd':
                afctx->dst_mac = optarg;
                break;
            case 'c':
                afctx->thread_num = atoi(optarg);
                break;
            case 'D':
                afctx->daemon = 1;
                break;
            case 'h':
                usage(argv[0], 0);
                break;
            default:
                fprintf(stderr, "unknown option\n");
                usage(argv[0], 1);
                break;
        }
    }

    return 0;
}

void *pkt_send(void *data)
{
    AFPacketInstance    *instance;
    AFCtx  *afctx  = (AFCtx*)data;
    Packet *p = afctx->pkt;
    int  i, send_success = -1;

    if (afpacket_init(afctx->iface, (void **)(&instance)) == AF_ERROR) {
        printf("afpacket_init fail , pkt_send thread quit!\n");
        goto error;
    }
    if (afpacket_start((void *)instance) == AF_ERROR) {
        printf("afpacket_start fail , pkt_send thread quit!\n");
        goto error;
    }

    printf("[*] into pkt_send thread.\n");
    for(i = 1; i <= PKT_SEND_COUNT; i++) {
        /* TDD: mutithread should lock it first */
        (uint32_t)p->ip4h->s_ip_src.s_addr++;  //ip_src change for test

        send_success = afpacket_send(instance, p);
        if (send_success <= 0) {
//            printf("afpcket_send fail!\n");
        } else{
//            printf("[*] we have send :%d pkts.\n", i);
//            print_packet_info(p);
        }
    }
    error:
    afpacket_close(instance);
}

void *pkt_receive(void *data)
{
    AFPacketInstance    *instance;
    Packet    p, *new_pkt;
    p.pkt   = calloc(2000,1);
    int    pkt_len = 0;
    AFCtx  *afctx  = (AFCtx*)data;
    int  i, j, send_success = -1;;

    if (afpacket_init(afctx->iface, (void **)(&instance)) == AF_ERROR) {
        printf("afpacket_init fail , pkt_recv thread quit!\n");
        goto error;
    }
    if (afpacket_start((void *)instance) == AF_ERROR) {
        printf("afpacket_start fail , pkt_recv thread quit!\n");
        goto error;
    }

    printf("[*] into pkt_receive thread.\n");
    int k;
    for(i = 0, j = 0, k = 0; k < PKT_RECEIVE_COUNT; i++) {
        pkt_len = afpacket_acquire(instance, &p, 2000);
        if (pkt_len > 0) {
            printf("[*] we have receive :%d pkts.\n", i);
//            print_packet_info(&p);
            /* Just deal with (SYN|ACK) pkt from server */
            if((p.tcph->th_flags & (TH_SYN|TH_ACK)) == (TH_SYN|TH_ACK)) {
                if(p.payload_len > 0){
                    continue;
                }
                printf("[*] we have receive :%d pkts.\n", ++k);
//                print_packet_info(&p);
                new_pkt = exchange_for_respond_pkt(&p, TH_ACK);
                /* update Seq & Ack. */
                new_pkt->tcph->th_ack = htonl(ntohl(new_pkt->tcph->th_seq) + 1);
                new_pkt->tcph->th_seq = htonl(1);
//                print_packet_info(&p);
//                ReCalculateChecksum(new_pkt);
                send_success = afpacket_send(instance, new_pkt);
                if (send_success <= 0) {
                    printf("afpcket_send fail!\n");
                } else{
                    printf("[*] we have send :%d pkts.\n", ++j);
                }
            }
        }
    }
    error:
    afpacket_close(instance);
}

int construct_pkt_fun(AFCtx *afctx, Packet *p)
{
    EtherHdr        eh;
    IP4Hdr          ip4h;
    TCPHdr          tcph;
    uint32_t        len = 0;
    char            *p_str = NULL;
    char            *p_pos = NULL;
    int             i;

    memset(&eh, 0, sizeof(EtherHdr));
    memset(&ip4h, 0, sizeof(IP4Hdr));
    memset(&tcph, 0, sizeof(TCPHdr));

    /* Layer 2 :Ether header */
    p_pos = afctx->src_mac;
    printf("src_mac:%s\n",p_pos);
    for(p_str = p_pos,i = 0; *p_pos != '\0' && i < 6; p_pos++){
        if(*p_pos != ':' && *(p_pos+1) != '\0'){
            continue;
        }
        if(*p_pos == ':'){
            *p_pos = '\0';
        }
        if(strlen(p_str) > 0){
            eh.ether_src[i] = strtol(p_str, NULL, 16);
            i++;
        }
        p_str = p_pos + 1;
    }

    p_pos = afctx->dst_mac;
    printf("dst_mac:%s\n",p_pos);
    for(p_str = p_pos,i = 0; *p_pos != '\0' && i < 6; p_pos++){
        if(*p_pos != ':' && *(p_pos+1) != '\0'){
            continue;
        }
        if(*p_pos == ':'){
            *p_pos = '\0';
        }
        if(strlen(p_str) > 0){
            eh.ether_dst[i] = strtol(p_str, NULL, 16);
            i++;
        }
        p_str = p_pos + 1;
    }
    eh.ether_type = htons(2048);

    /* Layer 3: IP header */
    ip4h.ip_verhl  = 69;
    ip4h.ip_tos    = 00;
    ip4h.ip_len    = htons(40);
    ip4h.ip_id     = htons(3620);
    ip4h.ip_off    = htons(16384);
    ip4h.ip_ttl    = 64;
    ip4h.ip_proto  = 6;
    ip4h.ip_csum   = htons(0x00);
    ip4h.s_ip_src.s_addr = inet_addr("0.1.1.1");
    ip4h.s_ip_dst.s_addr = inet_addr("10.60.20.10");

    /* Layer 4: TCP header */
    tcph.th_sport  = htons(59609);
    tcph.th_dport  = htons(80);
    tcph.th_seq    = 0;
    tcph.th_ack    = 0;
    tcph.th_offx2  = 0x50;
    tcph.th_flags  = TH_SYN;
    tcph.th_win    = htons(8192);
    tcph.th_sum    = htons(0xec84);
    tcph.th_urp    = 0;

    /* Fill the construct content into packet */
    p->ethh = (EtherHdr *)(p->pkt);
    memcpy(p->ethh, &eh, sizeof(EtherHdr));
    len = sizeof(EtherHdr);

    p->ip4h = (IP4Hdr *)(p->pkt + len);
    memcpy(p->ip4h, &ip4h, sizeof(IP4Hdr));
    len += sizeof(IP4Hdr);

    p->tcph = (TCPHdr *)((uint8_t *)p->ip4h + IPV4_GET_HLEN(p));
    memcpy(p->tcph, &tcph, sizeof(TCPHdr));

    p->payload = (uint8_t *)p->tcph + TCP_GET_HLEN(p);
    p->payload_len = 0;
    p->pkt_len = len + sizeof(TCPHdr);
    printf("pkt len is :%d\n", p->pkt_len);

    return 0;
}

void main(int argc, char **argv)
{
    AFPacketInstance    *instance;
    pthread_t          tid[10];
    Packet             p;
    AFCtx           afctx;

    int  i, cpu_index = 1;
    int cpu_start = 1;

    if (argc < 2){
        usage(argv[0], 0);
    }
    memset(&afctx, 0, sizeof(AFCtx));
    memset(&p, 0 , sizeof(Packet));
    p.pkt  = calloc(2000,1);

    parse_cmd_line(argc, argv, &afctx);

    if(afctx.daemon == 1){
        if (daemon_init() == -1){
            printf("can't fork self\n");
            exit(0);
        }
    }
    /* TDD: Construct a Packet for send here, to be done. */
    construct_pkt_fun(&afctx, &p);
//    print_packet_info(&p);
//    printf("----^before----v-after---\n");
    ReCalculateChecksum(&p);
    afctx.pkt = &p;
//    Packet *new_pkt = exchange_for_respond_pkt(&p, (TH_SYN|TH_ACK));
//    print_packet_info(new_pkt);

    printf("thread num is :%d\n", afctx.thread_num);
    for(i = 0; i < afctx.thread_num; i++){
        if(i % 2 == 0){
            if (pthread_create(&tid[i], NULL, pkt_send, (void*)&afctx) != 0) {
                printf("create pkt_send thread failed!\n");
                return;
            }
        } else {
            if (pthread_create(&tid[i], NULL, pkt_receive, (void*)&afctx) != 0) {
                printf("create pkt_receive thread failed!\n");
                return;
            }
        }
        cpu_index   = (i + cpu_start)%(sysconf(_SC_NPROCESSORS_CONF));
        printf("tid[%d] is :%u\n", i, tid[i]);
        if (thread_set_cpu(tid[i], cpu_index, sysconf(_SC_NPROCESSORS_CONF)) == 0) {
            printf("create thread[%d] set cpu failed!\n", i);
            return;
        }
    }

    while(1) {
        sleep(100);
    }
}
