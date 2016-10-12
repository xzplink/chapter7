/*
 * @file name: util-afpacket.h
 * Created by zhaozhang@yxlink.com
 * on 2016/10/10.
 */

#ifndef _UTIL_AFPACKET_H
#define _UTIL_AFPACKET_H

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <sys/socket.h>
#include <linux/if_arp.h>
#include <unistd.h>
#include "ether-type.h"

#ifdef __cplusplus
extern "C" {
#endif

#define STATE_STOPPED         0
#define STATE_STARTED         1
#define VLAN_TAG_LEN          4

#define IP_TYPE             (0x0800)
#define TCP_TYPE            (0x06)
#define AF_ERROR             -1
#define AF_SUCCESS           0
#define HTTP_PORT            22

typedef struct _AFPacketInstance
{
    char        *name;
    int          fd;
    uint32_t     index;
    struct       sockaddr_ll sll;
    uint32_t     tp_version;
    uint32_t     tp_hdrlen;

    uint8_t       state;
} AFPacketInstance;

typedef struct _Packet
{
    uint8_t    *pkt;
    uint32_t    pkt_len;
    EtherHdr    *ethh;
    IP4Hdr      *ip4h;
    TCPHdr      *tcph;

    uint8_t    *payload;
    uint32_t    payload_len;
} Packet;

typedef struct _AFCtx{
    int      daemon;
    int      thread_num;
    Packet   *pkt;
    uint8_t  *src_mac;
    uint8_t  *dst_mac;
    uint8_t  *iface;
}AFCtx;

uint8_t afpacket_init(const char *dev_name, void **ctxt_ptr);
int afpacket_start(void *handle);
int afpacket_acquire(void *handle, Packet *p, uint32_t pkt_len);
int afpacket_send(void *handle, Packet *p);
int afpacket_close(void *handle);
Packet *exchange_for_respond_pkt(Packet *p, uint8_t flag);
int ReCalculateChecksum(Packet *p);
int print_packet_info(Packet *p);

#ifdef __cplusplus
}
#endif

#endif //_UTIL_AFPACKET_H
