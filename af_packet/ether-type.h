/*
 * @file name: ether-type.h
 * on 2016/10/10.
 */

#ifndef _ETHER_TYPE_H_H
#define _ETHER_TYPE_H_H

#include <sys/types.h>
#include <arpa/inet.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef unsigned char      uint8_t;
typedef unsigned short     uint16_t;
typedef unsigned int       uint32_t;
//typedef unsigned long long uint64_t;

#define ETHERNET_TYPE_IP         0x0800
#define ETHERNET_TYPE_ARP        0x0806
#define ETHERNET_TYPE_IPV6       0x86dd
#define ETHERNET_TYPE_VLAN       0x8100
#define ETHERNET_HEADER_LEN       14


#define PKT_IS_IPV4(p)      (((p)->ip4h != NULL))
#define PKT_IS_TCP(p)       (((p)->tcph != NULL))
#define PKT_IS_UDP(p)       (((p)->udph != NULL))

#define TH_FIN                               0x01
#define TH_SYN                               0x02
#define TH_RST                               0x04
#define TH_PUSH                              0x08
#define TH_ACK                               0x10
#define TH_URG                               0x20
/** Establish a new connection reducing window */
#define TH_ECN                               0x40
/** Echo Congestion flag */
#define TH_CWR                               0x80

#define IPV4_HEADER_LEN                       20
#define TCP_HEADER_LEN                        20
#define IP_GET_RAW_VER(pkt)                  ((((pkt)[0] & 0xf0) >> 4))
#define IPV4_GET_RAW_IPLEN(ip4h)             ((ip4h)->ip_len)
#define IPV4_GET_IPLEN(p)                    (ntohs(IPV4_GET_RAW_IPLEN((p)->ip4h)))
#define IPV4_GET_RAW_HLEN(ip4h)              ((ip4h)->ip_verhl & 0x0f)
#define IPV4_GET_HLEN(p)                     (IPV4_GET_RAW_HLEN((p)->ip4h) << 2)
#define TCP_GET_RAW_OFFSET(tcph)             (((tcph)->th_offx2 & 0xf0) >> 4)
#define TCP_GET_OFFSET(p)                    TCP_GET_RAW_OFFSET((p)->tcph)
#define TCP_GET_HLEN(p)                      (TCP_GET_OFFSET((p)) << 2)
#define IPV4_GET_RAW_HLEN(ip4h)              ((ip4h)->ip_verhl & 0x0f)

typedef struct _ip {
    int family;
    int bits;

    /* see sfip_size(): these address bytes
     * must be the last field in this struct */
    union
    {
        uint8_t  u6_addr8[16];
        uint16_t u6_addr16[8];
        uint32_t u6_addr32[4];
//        uint64_t    u6_addr64[2];
    } ip;
#define ip8  ip.u6_addr8
#define ip16 ip.u6_addr16
#define ip32 ip.u6_addr32
//    #define ip64 ip.u6_addr64
} sfip_t;

/*
 * Ethernet header
 */

typedef struct _EtherHdr
{
    uint8_t ether_dst[6];
    uint8_t ether_src[6];
    uint16_t ether_type;

}  EtherHdr;

typedef struct _IP4Hdr
{
    uint8_t ip_verhl;      /* version & header length */
    uint8_t ip_tos;        /* type of service */
    uint16_t ip_len;       /* datagram length */
    uint16_t ip_id;        /* identification  */
    uint16_t ip_off;       /* fragment offset */
    uint8_t ip_ttl;        /* time to live field */
    uint8_t ip_proto;      /* datagram protocol */
    uint16_t ip_csum;      /* checksum */
    union {
        struct {
            struct in_addr ip_src;  /* source IP */
            struct in_addr ip_dst;  /* dest IP */
        }ip4_un1;
        uint16_t ip_addrs[4];
    }ip4_hdrun1;
} IP4Hdr;

#define s_ip_src                          ip4_hdrun1.ip4_un1.ip_src
#define s_ip_dst                          ip4_hdrun1.ip4_un1.ip_dst
#define s_ip_addrs                        ip4_hdrun1.ip_addrs

typedef struct _IPv6Hdr
{
    uint32_t vcl;      /* version, class, and label */
    uint16_t len;      /* length of the payload */
    uint8_t  next;     /* next header
                         * Uses the same flags as
                         * the IPv4 protocol field */
    uint8_t  hop_lmt;  /* hop limit */
    sfip_t ip_src;
    sfip_t ip_dst;
} IP6Hdr;

/* IPv6 address */
#ifndef s6_addr
struct in6_addr
{
    union
    {
        uint8_t u6_addr8[16];
        uint16_t u6_addr16[8];
        uint32_t u6_addr32[4];
    } in6_u;
#define s6_addr         in6_u.u6_addr8
#define s6_addr16       in6_u.u6_addr16
#define s6_addr32       in6_u.u6_addr32
};
#endif

/* more macros for TCP offset */
#define TCP_OFFSET(tcph)        (((tcph)->th_offx2 & 0xf0) >> 4)
#define TCP_X2(tcph)            ((tcph)->th_offx2 & 0x0f)

#define TCP_ISFLAGSET(tcph, flags) (((tcph)->th_flags & (flags)) == (flags))

/* we need to change them as well as get them */
#define SET_TCP_OFFSET(tcph, value)  ((tcph)->th_offx2 = (unsigned char)(((tcph)->th_offx2 & 0x0f) | (value << 4)))
#define SET_TCP_X2(tcph, value)  ((tcph)->th_offx2 = (unsigned char)(((tcph)->th_offx2 & 0xf0) | (value & 0x0f)))

typedef struct _TCPHdr
{
    uint16_t th_sport;     /* source port */
    uint16_t th_dport;     /* destination port */
    uint32_t th_seq;       /* sequence number */
    uint32_t th_ack;       /* acknowledgement number */
    uint8_t th_offx2;      /* offset and reserved */
    uint8_t th_flags;
    uint16_t th_win;       /* window */
    uint16_t th_sum;       /* checksum */
    uint16_t th_urp;       /* urgent pointer */

} TCPHdr;

typedef struct _UDPHdr
{
    uint16_t uh_sport;
    uint16_t uh_dport;
    uint16_t uh_len;
    uint16_t uh_chk;

} UDPHdr;

#ifdef __cplusplus
}
#endif

#endif //_ETHER_TYPE_H_H
