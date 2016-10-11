/*
 * @file name: util-afpacket.h
 * Created by zhaozhang@yxlink.com
 * on 2016/10/10.
 */

#ifndef _UTIL_AFPACKET_H
#define _UTIL_AFPACKET_H

#include <sys/socket.h>
#include <linux/if_arp.h>
#include "ether-type.h"

#ifdef __cplusplus
extern "C" {
#endif

#define IP_TYPE             (0x0800)
#define TCP_TYPE            (0x06)
#define AF_ERROR             -1

typedef struct _AFPacketInstance
{
    char        *name;
    int         fd;
    int         index;
    struct      sockaddr_ll sll;
    uint8_t     state;
} AFPacketInstance;

typedef struct _Packet
{
    uint8_t    *pkt;
    uint32_t    pktlen;
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

extern uint8_t afpacket_init(const char *dev_name, void **ctxt_ptr);
extern int afpacket_start(void *handle);
extern int afpacket_acquire(void *handle, Packet *p, uint32_t pkt_len);
extern int afpacket_send(void *handle, Packet *p);
extern int afpacket_close(void *handle);
Packet *exchange_for_respond_pkt(Packet *p, uint8_t flag);
int ReCalculateChecksum(Packet *p);
#ifdef __cplusplus
}
#endif

#endif //_UTIL_AFPACKET_H
