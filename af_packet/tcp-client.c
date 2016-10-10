/*
 * @file name: tcp-client.c
 * Created by zhaozhang@yxlink.com
 * on 2016/10/10.
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <getopt.h>
#include "util-afpacket.h"
#include "util-tools.h"


void usage(char *prg, int exit_code)
{
    printf("tcp-client usage: %s [OPTION]\n\n", prg);
    printf("Options:\n");
    printf("  -i, --ether              set bind ether interface\n");
    printf("  -s, --smac               set source Mac Address\n");
    printf("  -d, --dmac               set destination Mac Address\n");
    printf("  -c, --count              set running thread count");
    printf("  -D, --daemon             run in daemon mode");
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
                afctx->thread_num = optarg;
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
    SEND_ARG            *p_send_arg     = (SEND_ARG*)data;
    u_int32_t           send_num        = p_send_arg->send_num;
    u_int32_t           gap_time        = p_send_arg->gap_time;
    u_int32_t           repick_times    = p_send_arg->repick_times;
    Pkt_Buf             *p_http_pkt     = p_send_arg->p_http_pkt;
    u_int8_t            *p_eth          = p_send_arg->p_eth;
    u_int32_t           i;
    if (afpacket_init(p_eth, (void **)(&instance)) == 0)
    {
        printf("afpacket_init fail , pkt_recv thread quit!\n");
        return ;
    }
    if (afpacket_start((void *)instance) == -1)
    {
        printf("afpacket_start fail , pkt_send thread quit!\n");
        return ;
    }

    printf("into pkt_send thread\n");
    for(i=0; (i<send_num)||(send_num==0); i++)
    {
        u_int8_t send_success;
        g_repick_time++;
        if ((g_repick_time%repick_times) == 0)
        {
            (((Ip_Header*)(p_http_pkt->p_ip_header))->sourceIP)++;  //sourceip change for test
        }

        send_success = afpacket_send(instance,p_http_pkt);

        if (gap_time != 0)
        {
            usleep(gap_time);
        }

        if (send_success<=0)
        {
            printf("afpcket_send fail!\n");
        }
    }

}

void main(int argc, char* argv[])
{
    AFCtx afctx;
    AFPacketInstance    *instance;
    pthread_t          tid[100];
    Packet             p;
    EtherHdr eh;
    IPHdr iph;
    TCPHdr tcph;
    int  cpu_index;

    p.pkt        = calloc(2000,1);
    memset(&afctx, 0, sizeof(AFCtx));
    memset(&eh, 0, sizeof(EtherHdr));
    memset(&iph, 0, sizeof(IPHdr));
    memset(&tcph, 0, sizeof(TCPHdr));

    parse_cmd_line(argc, argv, &afctx);

    if(afctx.daemon == 1){
        if (daemon_init() == -1){
            printf("can't fork self\n");
            exit(0);
        }
    }

    strcpy(&eh.ether_src, afctx.src_mac);
    strcpy(&eh.ether_dst, afctx.src_mac);

    p.pkt_len    = len;
    printf("len:%d\n", len);


    if (afctx.thread_num > 100)
    {
        printf("thread num >100");
    }
    for(i=0; i<thread_num; i++)
    {
        if (pthread_create(&tid[i], NULL, pkt_send, (void*)&afctx) != 0)
        {
            printf("create pkt_send thread failed!\n");
            return;
        }
        cpu_index   = (i+cpu_start)%(sysconf(_SC_NPROCESSORS_CONF));
        if (thread_set_cpu(tid[i], cpu_index, sysconf(_SC_NPROCESSORS_CONF)) == 0)
        {
            printf("recv thread%d set cpu failed!\n", i);
            return;
        }
    }

    while(1)
    {
        sleep(100);
    }
}
